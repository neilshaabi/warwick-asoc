from os import system
from datetime import date
import pandas as pd
import pywhatkit

today = date.today().strftime("%d-%m-%Y")
filepath = f"~/Desktop/asoc_{today}.csv"

# Retrieve data from heroku postgres db, write to csv file
system(
    f"heroku pg:psql -a warwick-asoc \
        -c \"\copy ( \
        SELECT first_name, last_name, membership, student_id, is_exec, verified  \
        FROM users \
        ORDER BY is_exec desc, membership, first_name \
            ) \
        TO '{filepath}' \
        WITH CSV DELIMITER ',' HEADER;\""
)

# Process data into individual categories
print("\nProcessing data...")
df = pd.read_csv(filepath)
verified = df.query("verified == 't'")
members = verified.query("membership == membership")
exec = verified.query("is_exec == 't'")
nonExec = verified.query("is_exec == 'f'")
execMembers = pd.merge(members, exec, how="inner")
nonExecMembers = pd.merge(members, nonExec, how="inner")

# Format statistics
msg = f"""\n*ASOC User Stats ({today})*
(This is an automated message)\n
Verified users: {len(verified)}
Non-verified users: {len(df) - len(verified)}
Total members: {len(members)}
Exec memberships: {len(execMembers)}/{len(exec)}
Non-exec memberships: {len(nonExecMembers)}/{len(nonExec)}\n"""


# Send stats to ASOC Tech group chat
print("Sending message to ASOC Tech group chat...")
pywhatkit.sendwhatmsg_to_group_instantly("", msg)

# Print message
print("Message sent:")
print(msg)

# Delete CSV file
system(f"rm -rf {filepath}")
