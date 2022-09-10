from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import date

# Create database interface
db = SQLAlchemy()

# Model of a user for  database
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    date_joined = db.Column(db.Date)
    membership = db.Column(db.Text)
    student_id = db.Column(db.Integer)
    verified = db.Column(db.Boolean)

    def __init__(self, email, password_hash, first_name, last_name, date_joined, membership, student_id, verified):
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.date_joined = date_joined
        self.membership = membership
        self.student_id = student_id
        self.verified = verified

# Insert dummy data into tables
def dbinit():
    user_list = [
        User('neilshaabi@gmail.com', generate_password_hash('n'), 'Neil', 'Shaabi', date.today(), None, None, True)
        # User('neilshaabi@gmail.com', generate_password_hash('n'), 'Neil', 'Shaabi', date.today(), "Student", 2138843, True)
    ]
    db.session.add_all(user_list)
    
    db.session.commit()