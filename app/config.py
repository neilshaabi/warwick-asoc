from os import environ

# Default config values
class Config(object):
    TESTING = False
    SECRET_KEY = environ["SECRET_KEY"] # Randomly generated with os.urandom(12).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Mail setup
    MAIL_SERVER = "smtppro.zoho.eu"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "no-reply@warwick-asoc.co.uk"
    MAIL_PASSWORD = environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER = "no-reply@warwick-asoc.co.uk"
    MAIL_SUPPRESS_SEND = False
    
    # Stripe Checkout setup
    STRIPE_SECRET_KEY = environ["STRIPE_SECRET_KEY"]
    STRIPE_PUBLISHABLE_KEY = environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_ENDPOINT_SECRET = environ["STRIPE_ENDPOINT_SECRET"]


# Config values for running app in production
class ProductionConfig(Config):
    DEBUG = False
    RESET_DB = False
    SQLALCHEMY_DATABASE_URI = environ["DATABASE_URL"]


# Config values for running app in development
class DevelopmentConfig(Config):
    DEBUG = True
    RESET_DB = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///asoc.sqlite"
    