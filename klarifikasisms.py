import sys
import csv
import re
from datetime import datetime
from twilio.rest import Client

import credentials
import template_klarifikasi

def is_valid_phone_8digits(phone):
    if not phone:
        return False
    phone = phone.strip()
    return re.fullmatch(r"\d{8}", phone) is not None


def perform_klarifikasi_sms(file_path, send_message=False):
    print('inside klarifikasi sms')
    print(f'file path is: {file_path}')
    print(f'send_message = {send_message}')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log/sms_klarifikasi_{timestamp}.log"

    client = Client(credentials.twilio_account_sid, credentials.twilio_auth_token) if send_message else None
    msgsender = 'TimMisiGPO'

    with open(log_filename, "w", encoding="utf-8") as logfile:
        with open(file_path, 'r', encoding="utf-8") as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')

            for idx, row in enumerate(datareader, start=1):
                if len(row) < 9:
                    print(f"Row {idx} skipped: not enough columns")
                    continue

                phone = row[8].strip()  # column 9 = phone (8 digits)
                if not is_valid_phone_8digits(phone):
                    print(f"Row {idx} skipped: invalid phone '{phone}'")
                    continue

                recipient = f"+65{phone}"

                # Personalised field: 1st column (row[0])
                msgbody = template_klarifikasi.commitment_klarifikasi.format(row[0]).strip()

                # Log final SMS
                logfile.write(f"--- SMS #{idx} ---\nTo: {recipient}\nBody:\n{msgbody}\n{'-'*40}\n\n")

                if send_message:
                    try:
                        message = client.messages.create(
                            body=msgbody,
                            from_=msgsender,
                            to=recipient
                        )
                        print(f"Sent SMS to {recipient} | SID={message.sid}")
                    except Exception as e:
                        print(f"FAILED to send SMS to {recipient}: {e}")
                else:
                    print(f"[PREVIEW] Logged SMS for {recipient}")

    print(f"\n✔ SMS logged to: {log_filename}")


if __name__ == '__main__':
    file_path = sys.argv[1]
    send_flag = "-sendmessage" in sys.argv
    perform_klarifikasi_sms(file_path, send_message=send_flag)
