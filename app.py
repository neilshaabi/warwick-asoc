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

from utils import isValidPassword, sendVerificationEmail, sendResetEmail

app = Flask(__name__)

# Randomly generated with os.urandom(12).hex()
app.config["SECRET_KEY"] = "538270fea6c657529ee5c3fc"

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Select the database filename
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///asoc.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise the database so it can connect with our app
db.init_app(app)

# Avoid resetting the database every time this app is restarted
resetdb = True

# Drop and create all tables, insert dummy data
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

        # Ensure a valid password was entered
        elif not isValidPassword(password):
            error = "Please enter a valid password"
        
        # Ensure user with same email does not already exist
        elif User.query.filter_by(email=email.lower()).first() is not None:
            error = "This email address is already in use"

        # Successful registration
        else:
            
            # Insert new user into database
            user = User(email.lower(), generate_password_hash(password), first_name.capitalize(), last_name.capitalize(), date.today(), None, None, False)
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
        if user is None or not check_password_hash(user.password_hash, password):
            error = "Incorrect email/password"
        
        # Check if user's email has been verified
        elif not user.verified:
            error = "Email not verified, resending verification link"
            sendVerificationEmail(s, mail, user)
        
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
            email = request.form.get("email")
            
            # Find user with this email
            user = User.query.filter_by(email=email.lower()).first()

            # Check if user with this email does not exist
            if user is None:
                error = "No account found with this email address"
            
            # Send reset email
            else:
                sendResetEmail(s, mail, user)
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
        logout_user()
        return render_template("reset-request.html")


# COMMENT HERE
@app.route("/reset-password/<token>")
def reset_password(token):

    logout_user()

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
def membership_select():

    if request.method == 'POST':
        
        membership_type = request.form.get('membership_type')

        if membership_type == "student":
            student_id = request.form.get('student_id')
            
            print(student_id)
        else:
            print("associate la bro")
        
        return "hello"

    # Request method is GET
    else:
        return render_template("membership.html", authenticated=current_user.is_authenticated)


# Source: https://testdriven.io/blog/flask-stripe-tutorial/
@app.route("/stripe-config")
def get_publishable_key():
    stripe_config = {"public_key" : stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


@app.route("/create-checkout-session")
def create_checkout_session():

    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]

    # Create new Checkout Session for the order
    try:
        # Stripe API docs: https://stripe.com/docs/api/checkout/sessions/create
        checkout_session = stripe.checkout.Session.create(
            mode = "payment",
            payment_method_types = ["card"],
            success_url = domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = domain_url + "cancelled",            
            line_items = [{
                "quantity" : "1",
                "price_data" : {
                    "unit_amount" : "800",
                    "currency" : "gbp",
                    "product_data" : { 
                        "name" : "Student Membership" 
                    },
                }
            }]
        )
        return jsonify({"checkout_session_id" : checkout_session["id"]})

    except Exception as e:
        # render something bro
        return jsonify(error=str(e))