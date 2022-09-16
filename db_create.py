from app import app
from app.db import db

db.init_app(app)
db.create_all()