import sys
import csv
import os
import smtplib
import ssl
from datetime import datetime

import templates
import credentials
from dotenv import load_dotenv

load_dotenv()  # reads .env from current working directory


def perform_reminder_email(file_path, send_message=False):
    print('inside remind commitment email')
    print(f'file path is: {file_path}')
    print(f'send_message = {send_message}')

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))

    smtp_login_email = os.getenv("SMTP_LOGIN_EMAIL", "timmisi.gpo@gmail.com")
    from_email = os.getenv("SMTP_FROM_EMAIL", smtp_login_email)
    reply_to = os.getenv("REPLY_TO", "")

    if not reply_to:
        raise RuntimeError("Missing REPLY_TO in .env")

    context = ssl.create_default_context()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log/email_preview_{timestamp}.log"

    with open(log_filename, "w", encoding="utf-8") as logfile:
        with open(file_path, 'r', encoding="utf-8") as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')
            for idx, row in enumerate(datareader, start=1):
                msgbody = templates.commitment_reminder.format(
                    row[0], row[2], row[3], row[5], row[4], row[6], row[6], row[0], row[6]
                )

                # Your template already includes "Subject: ..." and a blank line
                msgsubject = templates.commitment_reminder_template.format(row[1], row[6])

                recipient = row[-2]
                print(f'row[1] is {row[1]}')
                print(f'recipient is {recipient}')

                # Safety: ensure Subject header exists exactly once
                if not msgsubject.lower().lstrip().startswith("subject:"):
                    msgsubject = "Subject: " + msgsubject.strip() + "\n\n"

                raw_email = (
                    f"From: Tim Misi - ORPC Indonesian Ministry <{from_email}>\n"
                    f"Reply-To: {reply_to}\n"
                    f"To: {recipient}\n"
                    f"{msgsubject}"
                    f"{msgbody}"
                )

                # Always log final formatted email
                logfile.write(f"===== EMAIL #{idx} =====\n")
                logfile.write(raw_email)
                if not raw_email.endswith("\n"):
                    logfile.write("\n")
                logfile.write("\n" + ("-" * 60) + "\n\n")

                # Send only if flag is provided
                if send_message:
                    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
                        server.login(smtp_login_email, credentials.gmail_password)
                        server.sendmail(from_email, recipient, raw_email)
                    print(f"Sent email to {recipient}")
                else:
                    print(f"[PREVIEW] Logged email for {recipient}")

    print(f"\n✔ Emails logged to: {log_filename}")


if __name__ == '__main__':
    file_path = sys.argv[1]
    send_flag = "-sendmessage" in sys.argv
    perform_reminder_email(file_path, send_message=send_flag)
