from app import app
from app.db import db

with app.app_context():
    db.create_all()
