from smtplib import SMTP_SSL
from os import system
from email.message import EmailMessage

# Sender email credentials
SEND_FROM = "no-reply@warwick-asoc.co.uk"
EMAIL_PASSWORD = "<password>"

FILEPATH = f"asoc_emails.csv"

# Retrieve data from heroku postgres db, write to csv file
system(
    f"heroku pg:psql -a warwick-asoc \
        -c \"\copy \
        (SELECT email FROM users WHERE membership IS NOT NULL ORDER BY email) \
        TO '{FILEPATH}' \
        WITH CSV DELIMITER ',' HEADER;\""
)
# Create message object
msg = EmailMessage()
msg["From"] = SEND_FROM
msg["To"] = "neilshaabi@gmail.com"
msg["Subject"] = "ASOC Member Email Addresses"
msg.set_content(
    """
Hi Tanisha,\n
As requested, attached please find the email addresses of all current ASOC members, correct as of the time of sending this email.\n
Note: this is an automated message, please do not reply to this address.\n
Regards,
Neil"""
)

# Attach csv file
with open(FILEPATH, "rb") as f:
    msg.add_attachment(f.read(), maintype="csv", subtype="csv", filename=FILEPATH)

# Create server with SSL option to login and send email
server = SMTP_SSL("smtppro.zoho.eu", 465)
server.login(SEND_FROM, EMAIL_PASSWORD)
server.send_message(msg)
server.quit()

# Delete csv file
system(f"rm -rf {FILEPATH}")
