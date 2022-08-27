import os
import stripe

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from markupsafe import escape
from datetime import date
from db_schema import db, User, dbinit

from utils import isValidID, isValidPassword, sendVerificationEmail, sendPasswordResetEmail

app = Flask(__name__)

# Randomly generated with os.urandom(12).hex()
app.config["SECRET_KEY"] = "538270fea6c657529ee5c3fc"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///asoc.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise the database so it can connect with our app
db.init_app(app)

# Drop and create all tables, insert dummy data
resetdb = True
if resetdb:
    with app.app_context():        
        db.drop_all()
        db.create_all()
        dbinit()


# Set up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
login_manager.login_message = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Set up flask mail
app.config.update(dict(
    MAIL_SERVER = 'smtppro.zoho.eu',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = 'admin@warwick-congress.org',
    MAIL_PASSWORD = os.environ["MAIL_PASSWORD"],
    MAIL_DEFAULT_SENDER = 'admin@warwick-congress.org',
    MAIL_SUPPRESS_SEND = False
))
mail = Mail(app)

# Instantiate serialiser for email verification
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Set up stripe payment gateway
stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"]
}
stripe.api_key = stripe_keys["secret_key"]


# Logs user out
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


# Allows users to register for an account
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        # Get form data
        first_name = escape(request.form.get("first_name"))
        last_name = escape(request.form.get("last_name"))
        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure full name was entered
        if not first_name or not last_name:
            error = "Please enter your full name"

        # Ensure email was entered
        elif not email:
            error = "Please enter your email"

        # Ensure user with same email does not already exist
        elif User.query.filter_by(email=email.lower()).first() is not None:
            error = "This email address is already in use"

        # Ensure a valid password was entered
        elif not isValidPassword(password):
            error = "Please enter a valid password"

        # Successful registration
        else:
            
            # Insert new user into database
            email = email.lower()
            user = User(email, generate_password_hash(password), first_name.capitalize(), last_name.capitalize(), date.today(), None, None, False)
            db.session.add(user)
            db.session.commit()

            # Send verification email and redirect to home page
            sendVerificationEmail(s, mail, user)
            flash('Email verification link sent to {}'.format(email))
            return url_for('index')
            
        return jsonify({'error' : error})
    
    # Request method is GET
    else:
        logout_user()
        return render_template("register.html")


# Logs user in if credentials are valid
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Get form data
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Find user with this email
        user = User.query.filter_by(email=email.lower()).first()

        # Check if user with this email does not exist or if password is incorrect
        if user is None:
            error = "Incorrect email address"
        
        # Check if user's email has been verified
        elif not user.verified:
            error = "Email not verified, verification link resent"
            sendVerificationEmail(s, mail, user)

        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password"
        
        # Log user in and redirect to home page
        else:
            login_user(user)
            return url_for('index')

        return jsonify({'error' : error})
    
    # Request method is GET
    else:
        logout_user()
        return render_template("login.html")


# COMMENT HERE
@app.route("/verify-email/<token>")
def verify_email(token):

    logout_user()
    
    # Get email from token
    try:
        email = s.loads(token, max_age=86400) # Each token is valid for 24 hours
    
        # Mark user as verified
        user = User.query.filter_by(email=email).first()
        user.verified = True
        db.session.commit()

        # Log in user
        login_user(user)
        flash('Success! Your email address has been verified.')

    # Invalid/expired token
    except:
        flash("Invalid or expired verification link, please sign in to request a new link")

    return redirect('/')
     

# COMMENT HERE
@app.route("/reset-password", methods=["GET", "POST"])
def reset_request():

    if request.method == "POST":

        # Form submitted to request a password reset
        if request.form.get("form-type") == "request":
        
            # Get form data
            email = request.form.get("email").lower()
            
            # Find user with this email
            user = User.query.filter_by(email=email).first()

            # Check if user with this email does not exist
            if user is None:
                error = "No account found with this email address"
            
            # Send reset email
            else:
                sendPasswordResetEmail(s, mail, user)
                flash('Password reset instructions sent to {}'.format(email))
                return url_for('index')

            return jsonify({'error' : error})

        # Form submitted to reset password
        else:
            
            # Get form data
            email = request.form.get("email")
            password = request.form.get("password")
            password_confirmation = request.form.get("password_confirmation")
            
            # Ensure a valid password was entered
            if not isValidPassword(password):
                error = "Please enter a valid password"

            # Ensure password and confirmation match
            elif password != password_confirmation:
                error = "Passwords do not match"
            
            # Successful reset
            else:

                # Update user's password in database
                user = User.query.filter_by(email=email.lower()).first()
                user.password = generate_password_hash(password)
                db.session.commit()

                # Redirect to login page
                flash('Success! Your password has been reset')
                return url_for('index')
            
            return jsonify({'error' : error})
    
    # Request method is GET
    else:
        return render_template("reset-request.html")


# COMMENT HERE
@app.route("/reset-password/<token>")
def reset_password(token):

    logout_user()

    # Get email from token
    try:
        email = s.loads(token, max_age=86400) # Each token is valid for 24 hours
        return render_template("reset-password.html", email=email)

    # Invalid/expired token©
    except:
        flash("Invalid or expired reset link, please request another password reset")
        return redirect('/')


# Displays home page
@app.route("/")
def index():
    return render_template("index.html")


# Displays team page
@app.route("/team")
def team():
    return render_template("team.html")


# Allows users to select a membership to purchase
@app.route("/membership", methods=["GET", "POST"])
def membership():

    if request.method == "POST":
    
        membership_type = request.form.get("membership_type")
        student_id = request.form.get("student_id") or "none"
        stripe.api_key = stripe_keys["secret_key"]

        if membership_type == "Student" and not isValidID(student_id):
            return jsonify(error="Invalid Student ID")

        # Create new Checkout Session to handle membership purchases
        try:
            
            # See Stripe API docs: https://stripe.com/docs/api/checkout/sessions/create
            checkout_session = stripe.checkout.Session.create(
                mode = "payment",
                payment_method_types = ["card"],
                success_url = (url_for("success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}" + "&membership=" + membership_type),
                cancel_url = url_for("cancelled", _external=True),
                client_reference_id = current_user.id,
                line_items = [{
                    "quantity" : "1",
                    "price_data" : {
                        "unit_amount" : "500",
                        "currency" : "gbp",
                        "product_data" : { 
                            "name" : membership_type + " Membership"
                        },
                    }
                }],
                metadata = {
                    "student_id" : student_id
                }
            )
            return jsonify({
                "checkout_public_key" : stripe_keys["publishable_key"],
                "checkout_session_id" : checkout_session["id"]
                })

        except Exception as e:
            print(e)
            return jsonify(error=str(e))

    # Request method is GET
    else:
        if current_user.is_authenticated:
            membership = User.query.filter_by(id=current_user.id).first().membership
        else:
            membership = None

        return render_template("membership.html", authenticated=current_user.is_authenticated, membership=membership)


# Endpoint to handle successful payments
@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = stripe_keys["endpoint_secret"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except ValueError as e:
        return "Invalid payload", 400

    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    # If checkout was successful
    if event["type"] == "checkout.session.completed":
        
        print("\nSUCCESSFUL PAYMENT:")

        # Retrieve checkout info
        session = event["data"]["object"]
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        membership_type = line_items['data'][0]['description'].split()[0]

        # Update user's membership status in database
        user = User.query.filter_by(id=session['client_reference_id']).first()

        print("\nUSER: " + user.first_name)

        user.membership = membership_type
        if membership_type == 'Student':
            user.student_id = session['metadata']['student_id']
        db.session.commit()
 
    return "Success", 200


# Successful payments
@app.route("/success")
@login_required
def success():
    membership_type = request.args.get("membership")
    flash("Success! " + membership_type + " membership purchased")
    return redirect('/')


# Cancellation of payments
@app.route("/cancelled")
def cancelled():
    flash("Membership purchase request cancelled")
    return redirect('/')


# View and edit account details
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    user = User.query.filter_by(id=current_user.id).first()

    if request.method == "POST":

        # Get form data
        first_name = escape(request.form.get("first_name"))
        last_name = escape(request.form.get("last_name"))
        email = request.form.get("email").lower()
        student_id = request.form.get("student_id")

        # Ensure full name was entered
        if not first_name or not last_name:
            error = "Please enter your full name"

        # Ensure email was entered
        elif not email:
            error = "Please enter your email"

        # Ensure a valid student ID was entered if the user holds a student membership
        elif (user.membership == 'Student') and (not isValidID(student_id)):
            error = "Invalid student ID"
        
        # Ensure a different user with same email does not already exist
        elif (email != user.email) and (User.query.filter_by(email=email.lower()).first() is not None):
            error = "This email address is already in use"

        # Successful update
        else:
            
            # Update user's info into database
            user.first_name = first_name
            user.last_name = last_name
            user.student_id = int(student_id)
            db.session.commit()
            
            # Send verification email if user changes email
            if email != user.email:
                user.email = email
                user.verified = False
                db.session.commit()
                sendVerificationEmail(s, mail, user)
                flash('Email verification link sent to {}'.format(email))
                return url_for('index')
            
            else:
                flash('Success! Account details updated')
                return url_for('index')

        return jsonify({'error' : error})
    
    # Request method is GET
    else:
        return render_template("settings.html", user=user)
