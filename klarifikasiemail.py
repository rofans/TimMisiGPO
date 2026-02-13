import sys
import csv
import os
import smtplib
import ssl
import re
from datetime import datetime

import template_klarifikasi
import credentials
from dotenv import load_dotenv

load_dotenv()


def is_valid_email(email):
    if not email:
        return False
    email = email.strip()
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None


def perform_klarifikasi_email(file_path, send_message=False):
    print('inside klarifikasi email')
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
    log_filename = f"log/email_klarifikasi_{timestamp}.log"

    with open(log_filename, "w", encoding="utf-8") as logfile:
        with open(file_path, 'r', encoding="utf-8") as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')

            for idx, row in enumerate(datareader, start=1):
                # Ensure enough columns (need at least 9 cols: 0..8)
                if len(row) < 9:
                    print(f"Row {idx} skipped: not enough columns")
                    continue

                recipient = row[7].strip()  # column 8 = email

                if not is_valid_email(recipient):
                    print(f"Row {idx} skipped: invalid email '{recipient}'")
                    continue

                # Personalised fields: 2nd (row[1]), 7th (row[6]), 1st (row[0])
                msgsubject = template_klarifikasi.commitment_klarifikasi_template.format(row[1], row[6])
                msgbody = template_klarifikasi.commitment_klarifikasi.format(row[0])

                # Ensure Subject header exists exactly once
                if not msgsubject.lower().lstrip().startswith("subject:"):
                    msgsubject = "Subject: " + msgsubject.strip() + "\n\n"

                raw_email = (
                    f"From: Tim Misi - ORPC Indonesian Ministry <{from_email}>\n"
                    f"Reply-To: {reply_to}\n"
                    f"To: {recipient}\n"
                    f"{msgsubject}"
                    f"{msgbody}"
                )

                # Log final formatted email
                logfile.write(f"===== EMAIL #{idx} =====\n")
                logfile.write(raw_email)
                logfile.write("\n" + ("-" * 60) + "\n\n")

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
    perform_klarifikasi_email(file_path, send_message=send_flag)
