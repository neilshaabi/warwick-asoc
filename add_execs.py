from app import app
from app.db import db, insertTestData

with app.app_context():
    db.create_all()
    insertTestData()
