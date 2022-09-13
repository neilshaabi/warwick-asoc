from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

from app.db import db, User, insertTestData

app = Flask(__name__)
app.config.from_object("app.config.DevelopmentConfig")

# Set up database
db.init_app(app)
if app.config["RESET_DB"]:
    with app.app_context():
        db.drop_all()
        db.create_all()
        insertTestData()

# Instantiate mail object and serialiser for email verification
mail = Mail(app)
serialiser = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Set up flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/"
login_manager.login_message = None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import routes
from app import membership_routes
