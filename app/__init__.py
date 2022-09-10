from os import environ
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

import stripe

from app.db_schema import db, User, dbinit


#-------------------------------- SETUP & CONFIG --------------------------------#

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


# Set up database
db.init_app(app)
resetdb = True
if resetdb:
    with app.app_context():        
        db.drop_all()
        db.create_all()
        dbinit()


from app import routes
