from flask import Flask

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config.from_object("app.config.DevelopmentConfig")

from app import views
from app import membership_views