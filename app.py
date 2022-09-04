import stripe

from os import environ
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from markupsafe import escape
from datetime import date

from db_schema import db, User, dbinit
from utils import isValidID, isValidPassword, sendEmailWithToken, sendContactEmail

app = Flask(__name__)

app.config.update(
    SECRET_KEY = environ["SECRET_KEY"], # Randomly generated with os.urandom(12).hex()
    TEMPLATES_AUTO_RELOAD = True,
    SQLALCHEMY_DATABASE_URI = "sqlite:///asoc.sqlite",
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

# Set up Flask mail
app.config.update(
    MAIL_SERVER = 'smtppro.zoho.eu',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USE_TLS = False,
    MAIL_USERNAME = 'no-reply@warwick-asoc.co.uk',
    MAIL_PASSWORD = environ["MAIL_PASSWORD"],
    MAIL_DEFAULT_SENDER = 'no-reply@warwick-asoc.co.uk',
    MAIL_SUPPRESS_SEND = False
)
mail = Mail(app)

# Instantiate serialiser for email verification
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Set up Stripe payment gateway
app.config.update(
    STRIPE_SECRET_KEY = environ["STRIPE_SECRET_KEY"],
    STRIPE_PUBLISHABLE_KEY = environ["STRIPE_PUBLISHABLE_KEY"],
    STRIPE_ENDPOINT_SECRET = environ["STRIPE_ENDPOINT_SECRET"]
)
stripe.api_key = app.config["STRIPE_SECRET_KEY"]

# Set up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
login_manager.login_message = None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialise the database so it can connect with our app
db.init_app(app)

# Reset database - drop and create all tables, insert test data
resetdb = True
if resetdb:
    with app.app_context():        
        db.drop_all()
        db.create_all()
        dbinit()


# Logs user out
@app.route("/logout")
def logout():
    session.clear()
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
        if (not first_name or first_name.isspace()) or (not last_name or last_name.isspace()):
            error = "Please enter your full name"

        # Ensure email was entered
        elif not email or email.isspace():
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
            sendEmailWithToken(s, mail, user.first_name, user.email, "Email Verification")
            # flash('Success! Email verification instructions sent to {}'.format(email))
            # return url_for('index')
            session["email"] = email
            return url_for('verify_email')
            
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
        email = request.form.get("email").lower()
        password = request.form.get("password")
        
        # Find user with this email
        user = User.query.filter_by(email=email).first()

        # Check if user with this email does not exist or if password is incorrect
        if user is None or not check_password_hash(user.password_hash, password):
            error = "Incorrect email/password"
        
        # Check if user's email has been verified
        elif not user.verified:
            # error = "Email not verified, verification link resent"
            session["email"] = email
            return url_for('verify_email')
        
        # Log user in and redirect to home page
        else:
            login_user(user)
            return url_for('index')

        return jsonify({'error' : error})
    
    # Request method is GET
    else:
        logout_user()
        return render_template("login.html")


# TODO: comment 
@app.route("/verify-email", methods=["GET", "POST"])
def verify_email():

    # TODO: comment    
    user = User.query.filter_by(email=session["email"]).first() if "email" in session else None
    if not user or user.verified:
        return redirect('/')

    # TODO: HAVE A SEPARATE ROUTE WHICH ONLY SENDS THE EMAIL AND REDIRECTS TO THIS PAGE, HAVE THIS PAGE ONLY ACCCEPT GET REQUESTS, STORE THE USER'S NAME IN THE SESSION TOO
    if request.method == 'POST':
        sendEmailWithToken(s, mail, user.first_name, user.email, "Email Verification")
        return ""
    else:
        return render_template("verify-email.html", email=session["email"])
    

# TODO: comment 
@app.route("/email-verification/<token>")
def email_verification(token):
    
    # Get email from token
    try:
        email = s.loads(token, max_age=86400) # Each token is valid for 24 hours
    
        # Mark user as verified
        user = User.query.filter_by(email=email).first()
        user.verified = True
        db.session.commit()

        # Log in user
        login_user(user)
        flash('Success! Your email address has been verified')

    # Invalid/expired token
    except:
        flash("Invalid or expired verification link, please sign in to request a new link")

    return redirect('/')
     

# TODO: comment 
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
                sendEmailWithToken(s, mail, user.first_name, user.email, "Password Reset")
                flash('Password reset instructions sent to {}'.format(email))
                return url_for('index')

            return jsonify({'error' : error})

        # Form submitted to reset password
        elif request.form.get("form-type") == "reset":

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
                user = User.query.filter_by(email=email).first()
                user.password_hash = generate_password_hash(password)
                db.session.commit()

                # Redirect to login page
                flash('Success! Your password has been reset')
                return url_for('index')
            
            return jsonify({'error' : error})
    
    # Request method is GET
    else:
        return render_template("reset-request.html")


# TODO: comment 
@app.route("/reset-password/<token>")
def reset_password(token):

    # Get email from token
    try:
        email = s.loads(token, max_age=86400) # Each token is valid for 24 hours
        return render_template("reset-password.html", email=email)

    # Invalid/expired token
    except:
        flash("Invalid or expired reset link, please request another password reset")
        return redirect('/')


# Displays home page
@app.route("/")
def index():
    return render_template("index.html")


# Allows users to select a membership to purchase
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
                "checkout_public_key" : app.config["STRIPE_PUBLISHABLE_KEY"],
                "checkout_session_id" : checkout_session["id"]
                })

        except Exception as e:
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
    endpoint_secret = app.config["STRIPE_ENDPOINT_SECRET"]

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

        # Retrieve checkout info
        session = event["data"]["object"]
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        membership_type = line_items['data'][0]['description'].split()[0]

        # Update user's membership status in database
        user = User.query.filter_by(id=session['client_reference_id']).first()

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


# Displays events page
@app.route("/events")
def events():
    return render_template("events.html")


# Displays team page
@app.route("/team")
def team():
    return render_template("team.html")


# Displays contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    
    if request.method == "POST":

        # Get form data
        name = request.form.get("name").title()
        email = request.form.get("email").lower()
        subject = request.form.get("subject").title()
        message = request.form.get("message")

        if not name or name.isspace():
            error = "Please enter your full name"

        elif not email or email.isspace():
            error = "Please enter your email"
        
        elif not subject or subject.isspace():
            error = "Please enter a subject"
        
        elif not message or message.isspace():
            error = "Please enter a message"

        # Successful form submission
        else:
            
            # Send email and redirect to home page
            sendContactEmail(mail, name, email, subject, message)
            flash('Success! Message sent from {}'.format(email))
            return url_for('index')
        
        return jsonify({'error' : error})

    else:
        return render_template("contact.html")


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
        email_confirmation = request.form.get("email_confirmation").lower()
        student_id = request.form.get("student_id")

        if (not first_name or first_name.isspace()) or (not last_name or last_name.isspace()):
            error = "Please enter your full name"

        elif not email or email.isspace():
            error = "Please enter your email"

        elif email != email_confirmation:
            error = "Emails do not match"

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
            user.student_id = int(student_id) if student_id else None
            db.session.commit()
            
            # Send verification email if user changes email
            if email != user.email:
                user.email = email
                user.verified = False
                db.session.commit()
                
                logout_user()
                sendEmailWithToken(s, mail, user.first_name, user.email, "Email Verification")
                # flash('Success! Email verification instructions sent to {}'.format(email))
                # return url_for('index')
                session["email"] = email
                return url_for('verify_email')
            
            # Flash success message and redirect to home page
            else:
                flash('Success! Account details updated')
                return url_for('index')

        return jsonify({'error' : error})
    
    # Request method is GET
    else:
        return render_template("settings.html", user=user)
