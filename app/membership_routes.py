import stripe
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required

from app import app
from app.db import db, User
from app.utils import isValidID

membership_prices = {"Student": 5.00, "Associate": 5.00}

# Handles membership selection, uses Stripe API to accept payments
@app.route("/membership", methods=["GET", "POST"])
def membership():

    if request.method == "POST":

        # Get form data
        membership_type = request.form.get("membership_type")
        student_id = request.form.get("student_id") or "none"

        # Validate student ID
        if membership_type == "Student" and not isValidID(student_id):
            return jsonify(error="Invalid Student ID")

        # Create new Checkout Session to handle membership purchases
        try:

            stripe.api_key = app.config["STRIPE_SECRET_KEY"]

            # See Stripe API docs: https://stripe.com/docs/api/checkout/sessions/create
            checkout_session = stripe.checkout.Session.create(
                mode="payment",
                payment_method_types=["card"],
                success_url=(
                    url_for("success", _external=True)
                    + "?session_id={CHECKOUT_SESSION_ID}"
                    + "&membership="
                    + membership_type
                ),
                cancel_url=url_for("cancelled", _external=True),
                client_reference_id=current_user.id,
                line_items=[
                    {
                        "quantity": "1",
                        "price_data": {
                            "unit_amount": int(
                                100 * (membership_prices[membership_type])
                            ),
                            "currency": "gbp",
                            "product_data": {"name": membership_type + " Membership"},
                        },
                    }
                ],
                metadata={"student_id": student_id},
            )
            return jsonify(
                {
                    "checkout_public_key": app.config["STRIPE_PUBLISHABLE_KEY"],
                    "checkout_session_id": checkout_session["id"],
                }
            )

        except Exception as e:
            return jsonify(error=str(e))

    # Request method is GET
    else:
        if current_user.is_authenticated:
            membership = User.query.filter_by(id=current_user.id).first().membership
        else:
            membership = None

        return render_template(
            "membership.html",
            authenticated=current_user.is_authenticated,
            membership=membership,
            membership_prices=membership_prices,
        )


# Endpoint to handle successful payments
@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = app.config["STRIPE_ENDPOINT_SECRET"]

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

    except ValueError as e:
        return "Invalid payload", 400

    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    # If checkout was successful
    if event["type"] == "checkout.session.completed":

        # Retrieve checkout info
        session = event["data"]["object"]
        line_items = stripe.checkout.Session.list_line_items(session["id"], limit=1)
        membership_type = line_items["data"][0]["description"].split()[0]

        # Update user's membership status in database
        user = User.query.filter_by(id=session["client_reference_id"]).first()

        user.membership = membership_type
        if membership_type == "Student":
            user.student_id = session["metadata"]["student_id"]
        db.session.commit()

    return "Success", 200


# Successful payments
@app.route("/success")
@login_required
def success():
    membership_type = request.args.get("membership")
    flash("Success! " + membership_type + " membership purchased")
    return redirect("/")


# Cancellation of payments
@app.route("/cancelled")
def cancelled():
    flash("Membership purchase request cancelled")
    return redirect("/")
