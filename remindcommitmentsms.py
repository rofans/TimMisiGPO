import sys
import csv
from datetime import datetime
from twilio.rest import Client
import credentials
import templates


def perform_reminder_sms(file_path, send_message=False):
    print('inside remind commitment sms')
    print(f'file path is: {file_path}')
    print(f'send_message = {send_message}')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log/sms_preview_{timestamp}.log"

    if send_message:
        client = Client(
            credentials.twilio_account_sid,
            credentials.twilio_auth_token
        )

    with open(log_filename, "w", encoding="utf-8") as logfile:
        with open(file_path, 'r', encoding="utf-8") as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')

            for idx, row in enumerate(datareader, start=1):
                msgbody = templates.commitment_reminder.format(
                    row[0], row[2], row[3],
                    row[5], row[4],
                    row[6], row[6],
                    row[0], row[6]
                )

                msgsender = 'TimMisiGPO'
                recipient = row[-1]

                # Always log final message
                logfile.write(
                    f"--- MESSAGE #{idx} ---\n"
                    f"To: {recipient}\n"
                    f"From: {msgsender}\n"
                    f"Body:\n{msgbody}\n"
                    f"{'-'*40}\n\n"
                )

                # Send ONLY if flag is present
                if send_message:
                    message = client.messages.create(
                        body=msgbody,
                        from_=msgsender,
                        to=recipient
                    )
                    print(f"Sent to {recipient} | SID={message.sid}")
                else:
                    print(f"[PREVIEW] Logged message for {recipient}")

    print(f"\n✔ Messages logged to: {log_filename}")


if __name__ == '__main__':
    file_path = sys.argv[1]
    send_flag = "-sendmessage" in sys.argv

    perform_reminder_sms(file_path, send_message=send_flag)