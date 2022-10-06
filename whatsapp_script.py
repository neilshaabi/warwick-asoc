from os import system
from datetime import date
from pywhatkit import sendwhatmsg_to_group_instantly
import pandas as pd

today = date.today().strftime("%d-%m-%Y")
filename = f"asoc_{today}.csv"
filepath = f"~/Desktop/{filename}"

# Retrieve data from heroku postgres db, write to csv file
system(
    f"heroku pg:psql -a warwick-asoc \
        -c \"\copy ( \
        SELECT first_name, last_name, membership, student_id, is_exec, verified  \
        FROM users \
        WHERE verified \
        ORDER BY is_exec desc, membership, first_name \
            ) \
        TO '{filepath}' \
        WITH CSV DELIMITER ',' HEADER;\""
)

# Process data into individual categories
print("\nProcessing data...")
df = pd.read_csv(filename)
members = df.query("membership == membership")
exec = df.query("is_exec == 't'")
nonExec = df.query("is_exec == 'f'")
execMembers = pd.merge(members, exec, how="inner")
nonExecMembers = pd.merge(members, nonExec, how="inner")

# Format statistics
msg = f"""\n*ASOC User Stats ({today})*\n
(Note: this is an automated message)
Total accounts: {len(df)}
Total members: {len(members)}
Exec memberships: {len(execMembers)}/{len(exec)}
Non-exec memberships: {len(nonExecMembers)}/{len(nonExec)}\n"""

# Send stats to ASOC Tech group chat
print("Sending message to ASOC Tech group chat...")
sendwhatmsg_to_group_instantly("", msg)
print("Message sent!\n")

# Delete CSV file
system(f"rm -rf {filepath}")
