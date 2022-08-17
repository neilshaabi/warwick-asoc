from flask import render_template, url_for
from flask_mail import Message

# Returns whether a given password meets the security requirements
def isValidPassword(password):

    # Password must be at least 8 characters and contain at least one digit, uppercase and lowercase letter
    if (len(password) < 8) or (
        not any(char.isdigit() for char in password)) or (
        not any(char.isupper() for char in password)) or (
        not any(char.islower() for char in password)):
        return False
        
    return True


def sendVerificationEmail(s, mail, user):
    
    # Generate email verification link
    token = s.dumps(user.email)
    link = url_for('verify_email', token=token, _external=True)

    # Send email with verification link
    msg = Message("Email Verification", recipients=[user.email])
    msg.html = render_template('mails/verify-email.html', first_name=user.first_name, verification_link=link)
    mail.send(msg)


def sendPasswordResetEmail(s, mail, user):
    
    # Generate email verification link
    token = s.dumps(user.email)
    link = url_for('reset_password', token=token, _external=True)

    # Send email with verification link
    msg = Message("Password Reset", recipients=[user.email])
    msg.html = render_template('mails/reset-password-email.html', first_name=user.first_name, reset_link=link)
    mail.send(msg)


def isValidID(id_str):

    try:
        student_id = int(id_str)
        
        if (student_id < 1000000) or (student_id > 2200000):
            return False
        else:
            return True
    
    except:
        return False
