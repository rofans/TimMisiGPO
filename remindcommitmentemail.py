import sys
import csv
import os
import templates
import smtplib
import ssl
import credentials
from dotenv import load_dotenv

load_dotenv()  # reads .env from current working directory


def perform_reminder_email(file_path):
    print('inside remind commitment email')
    print('file path is: {}'.format(file_path))

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))

    smtp_login_email = os.getenv("SMTP_LOGIN_EMAIL", "timmisi.gpo@gmail.com")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_login_email)

    reply_to = os.getenv("REPLY_TO", "")

    if not reply_to:
        raise RuntimeError("Missing REPLY_TO in .env")

    context = ssl.create_default_context()

    with open(file_path, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            msgbody = templates.commitment_reminder.format(
                row[0], row[2], row[3], row[5], row[4], row[6], row[6], row[0], row[6]
            )
            msgsubject = templates.commitment_reminder_template.format(row[1], row[6])

            recipient = row[-2]
            print('row[1] is {}'.format(row[1]))
            print('recipient is {}'.format(recipient))

            # Ensure Subject header exists (your template might already include it)
            if not msgsubject.lower().startswith("subject:"):
                msgsubject = "Subject: " + msgsubject

            raw_email = (
                f"From: Tim Misi - ORPC Indonesian Ministry <{from_email}>\n"
                f"Reply-To: {reply_to}\n"
                f"To: {recipient}\n"
                f"{msgsubject}\n"
                f"{msgbody}"
            )

            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
                server.login(smtp_login_email, credentials.gmail_password)
                server.sendmail(from_email, recipient, raw_email)


if __name__ == '__main__':
    perform_reminder_email(sys.argv[1])
