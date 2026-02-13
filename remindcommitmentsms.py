import sys
import csv
import re
from twilio.rest import Client
import credentials
import templates


def is_valid_phone(phone):
    """
    Valid phone format:
    - Exactly 8 digits
    - Numbers only
    """
    if not phone:
        return False
    phone = phone.strip()
    return bool(re.fullmatch(r"\d{8}", phone))


def perform_reminder_sms(file_path, send_message=False):
    print('inside remind commitment sms')
    print(f'file path is: {file_path}')
    print(f'send_message = {send_message}')

    if send_message:
        client = Client(
            credentials.twilio_account_sid,
            credentials.twilio_auth_token
        )

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')

        for row_num, row in enumerate(datareader, start=1):

            # Column 9 (index 8) = phone number
            if len(row) < 9:
                print(f"Row {row_num} skipped: not enough columns")
                continue

            phone = row[8].strip()

            # Validate phone number
            if not is_valid_phone(phone):
                print(f"Row {row_num} skipped: invalid phone number '{phone}'")
                continue

            recipient = "+65" + phone  # prepend country code

            #msgbody = templates.commitment_reminder.format(
            #    row[0], row[2], row[3],
            #    row[5], row[4],
            #    row[6], row[6],
            #    row[0], row[6]
            #)

            msgbody = templates.commitment_reminder.format(
                row[0],
                row[2],
                row[3],
                row[5],
                row[4],
                row[6],
                row[6],
                row[6],
            )

            msgsender = 'TimMisiGPO'

            if send_message:
                try:
                    message = client.messages.create(
                        body=msgbody,
                        from_=msgsender,
                        to=recipient
                    )
                    print(f"Sent to {recipient} | SID={message.sid}")
                except Exception as e:
                    print(f"FAILED to send to {recipient}: {e}")
            else:
                print(f"[PREVIEW] Valid number {recipient} — message prepared")


if __name__ == '__main__':
    file_path = sys.argv[1]
    send_flag = "-sendmessage" in sys.argv
    perform_reminder_sms(file_path, send_message=send_flag)
