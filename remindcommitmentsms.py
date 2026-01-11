import sys
import csv
from twilio.rest import Client
import credentials
import templates


def perform_reminder_sms(file_path):
    print('inside remind commitment sms')
    print('file path is: {}'.format(file_path))
    client = Client(credentials.twilio_account_sid, credentials.twilio_auth_token)
    with open(file_path, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            msgbody = templates.commitment_reminder.format(row[0], row[2], row[3], row[5], row[4], row[6], row[6], row[0], row[6])
            msgsender = 'TimMisiGPO'
            recipient = row[-1]
            message = client.messages \
                .create(
                body=msgbody,
                from_=msgsender,
                to=recipient
            )
            print(message.sid)


if __name__ == '__main__':
    perform_reminder_sms(sys.argv[1])
