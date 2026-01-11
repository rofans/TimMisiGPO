import sys
import csv
import templates
import smtplib
import ssl
import credentials
from email.header import Header
from email.utils import formataddr


def perform_reminder_email(file_path):
    print('inside remind commitment email')
    print('file path is: {}'.format(file_path))
    context = ssl.create_default_context()
    with open(file_path, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        for row in datareader:
            msgbody = templates.commitment_reminder.format(row[0], row[2], row[3], row[5], row[4], row[6], row[6], row[0], row[6])
            msgsubject = templates.commitment_reminder_template.format(row[1], row[6])
            print('row[1] is {}'.format(row[1]))
            print('row[-2] is {}'.format(row[-2]))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login("timmisi.gpo@gmail.com", credentials.gmail_password)
                server.sendmail(
                    "timmisigpo@gmail.com",
                    row[-2],
                    'From: Tim Misi - ORPC Indonesian Ministry <timmisi.gpo@gmail.com>\n'
                    'Reply-To: Tim Misi - ORPC Indonesian Ministry <gpo.misi@gmail.com>, Rofans Manao <rofans.manao@gmail.com>\n'
                    + msgsubject
                    + msgbody
                )

if __name__ == '__main__':
    perform_reminder_email(sys.argv[1])
