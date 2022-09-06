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
    else:   
        return True


# Returns if a given string of a student ID is valid
def isValidID(id_str):
    try:
        student_id = int(id_str)
        if (student_id < 1000000) or (student_id > 2200000):
            return False
        else:
            return True
    except:
        return False


# Sends an email with a token-generated link
def sendEmailWithToken(serialiser, mail, name, email, subject):

    print("\n " + subject + " " + email + "\n")
    
    # Generate email contents based on subject
    token = serialiser.dumps(email)
    msgInfo = getMsg(token, subject)

    msg = Message(subject, recipients=[email])
    msg.html = render_template("email.html", name=name, body=msgInfo[0], btn_link=msgInfo[1], btn_text=msgInfo[2])
    mail.send(msg)


# Returns a dictionary with text to include in an email depending on the subject
def getMsg(token, subject):

    if subject == "Email Verification":
        body = "Thanks for joining the Warwick ASOC community! To access your account, please verify your email address using the link below."
        route = "email_verification"
        btn_text = "Verify Email"

    elif subject == "Password Reset":
        body = "Please use the link below to reset your account password."
        route = "reset_password"
        btn_text = "Reset Password"

    link = url_for(route, token=token, _external=True)
    return [body, link, btn_text]


# Sends an email with a token-generated link
def sendContactEmail(mail, name, email, subject, body):

    msg = Message(("Contact Form Submission: " + subject), recipients=[email], bcc=["officialwarwickasiansociety@gmail.com"])
    msg.html = render_template("email.html", name=name, body=body, contact=True)
    mail.send(msg)
