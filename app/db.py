from datetime import date
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# Model of a user for database
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    date_joined = db.Column(db.Date)
    membership = db.Column(db.Text)
    student_id = db.Column(db.Integer)
    verified = db.Column(db.Boolean)
    is_exec = db.Column(db.Boolean)

    def __init__(
        self,
        email,
        password_hash,
        first_name,
        last_name,
        date_joined,
        membership,
        student_id,
        verified,
        is_exec,
    ):
        self.email = email
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.date_joined = date_joined
        self.membership = membership
        self.student_id = student_id
        self.verified = verified
        self.is_exec = is_exec


# Model of a team member (exec/frep) for database
class TeamMember(db.Model):
    __tablename__ = "teamMember"
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    memberType = db.Column(db.Text)
    name = db.Column(db.Text)
    role = db.Column(db.Text)
    bio = db.Column(db.Text)
    img = db.Column(db.Text)
    def __init__(
        self,
        order,
        memberType,
        name,
        role,
        bio,
        img,
    ):
        self.order = order
        self.memberType = memberType
        self.name = name
        self.role = role
        self.bio = bio
        self.img = img


# Insert dummy data into tables
def insertTestData():
    
    # # Sample list of users
    # users = [
    #     User(
    #         "neilshaabi@gmail.com",
    #         generate_password_hash("n"),
    #         "Neil",
    #         "Shaabi",
    #         date.today(),
    #         "Student",
    #         2138843,
    #         True,
    #         True,
    #     ),
    #     User(
    #         "neil.shaabi@warwick.ac.uk",
    #         generate_password_hash("n"),
    #         "John",
    #         "Doe",
    #         date.today(),
    #         "Associate",
    #         None,
    #         True,
    #         False,
    #     ),
    # ]
    # db.session.add_all(users)

    # List of exec members
    execs = [
        TeamMember(
            1,
            "exec",
            "Rishi Jobanputra",
            "Co-President",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "rishi.jpeg"
        ),
        TeamMember(
            2,
            "exec",
            "Vishali Poojara",
            "Co-President",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "vishali.jpeg"
        ),
        TeamMember(
            3,
            "exec",
            "Bela Bhagata",
            "Vice-President and Secretary",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "bela.jpeg"
        ),
        TeamMember(
            4,
            "exec",
            "Ish Mann",
            "Ball Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "ish.jpeg"
        ),
        TeamMember(
            5,
            "exec",
            "Meera Thakrar",
            "Ball Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "meera.jpeg"
        ),
        TeamMember(
            6,
            "exec",
            "Kush Nathwani",
            "Careers Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "kush.jpeg"
        ),
        TeamMember(
            7,
            "exec",
            "Tanisha Anand",
            "Careers Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "tanisha.jpeg"
        ),
        TeamMember(
            8,
            "exec",
            "Aashni Thakrar",
            "Charities Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "aashni.jpeg"
        ),
        TeamMember(
            9,
            "exec",
            "Saiesha Suri",
            "Charities Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "saiesha.jpeg"
        ),
        TeamMember(
            10,
            "exec",
            "Sahil Gupta",
            "Diversity and Inclusion Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "sahil.jpeg"
        ),
        TeamMember(
            11,
            "exec",
            "Shivam Depala",
            "Events Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "shivam.jpeg"
        ),
        TeamMember(
            12,
            "exec",
            "Surina Rumpal",
            "Events Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "surina.jpeg"
        ),
        TeamMember(
            13,
            "exec",
            "Neil Mitra",
            "Marketing Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "neilm.jpeg"
        ),
        TeamMember(
            14,
            "exec",
            "Pranav Mattipalli",
            "Marketing Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "pranav.jpeg"
        ),
        TeamMember(
            15,
            "exec",
            "Rohan Patel",
            "Marketing Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "rohan.jpeg"
        ),
        TeamMember(
            16,
            "exec",
            "Avi Modi",
            "Speakers Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "avi.jpeg"
        ),
        TeamMember(
            17,
            "exec",
            "Rhia Shah",
            "Sports Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "rhia.jpeg"
        ),
        TeamMember(
            18,
            "exec",
            "Khush Pau",
            "Sports Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "khush.jpeg"
        ),
        TeamMember(
            19,
            "exec",
            "Neil Shaabi",
            "Technology Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "neils.jpeg"
        ),
        TeamMember(
            20,
            "exec",
            "Adam Syed",
            "Technology Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "adam.jpeg"
        ),
        TeamMember(
            21,
            "exec",
            "Arjav Vora",
            "Tour Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "arjav.jpeg"
        ),
        TeamMember(
            22,
            "exec",
            "Lyla Younis",
            "Tour Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "lyla.jpeg"
        ),
        TeamMember(
            23,
            "exec",
            "Gaurav Pant",
            "Treasurer",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "gaurav.jpeg"
        ),
        TeamMember(
            24,
            "exec",
            "Jai Tapuria",
            "Welfare Coordinator",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "jai.jpeg"
        ),
    ]
    db.session.add_all(execs)


    # List of freps
    freps = [
        TeamMember(
            1,
            "frep",
            "Riki Bains",
            "Careers Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "riki.jpeg"
        ),
        TeamMember(
            2,
            "frep",
            "Priya Shah",
            "Charities Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "priya.jpeg"
        ),
        TeamMember(
            3,
            "frep",
            "Zoey Jaffri",
            "Diversity and Inclusion Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "zoey.jpeg"
        ),
        TeamMember(
            4,
            "frep",
            "Maanya Gupta",
            "Events Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "maanya.jpeg"
        ),
        TeamMember(
            5,
            "frep",
            "Nikisha Patel",
            "Marketing Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "nikisha.jpeg"
        ),
        TeamMember(
            6,
            "frep",
            "Krish Mamtora",
            "Speakers Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "krish.jpeg"
        ),
        TeamMember(
            7,
            "frep",
            "Aaren Patel",
            "Sports Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "aaren.jpeg"
        ),
        TeamMember(
            8,
            "frep",
            "Parth S. Poudel",
            "Technology Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "parth.jpeg"
        ),
        TeamMember(
            9,
            "frep",
            "Jai Saha",
            "Tour Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "jai.jpeg"
        ),
        TeamMember(
            10,
            "frep",
            "Jay Masani",
            "Welfare Representative",
            "sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo donec enim diam vulputate ut pharetra sit amet aliquam id diam maecenas ultricies mi eget mauris pharetra et ultrices neque ornare aenean euismod elementum nisi quis eleifend quam adipiscing",
            "jay.jpeg"
        ),   
    ]
    db.session.add_all(freps)

    db.session.commit()
