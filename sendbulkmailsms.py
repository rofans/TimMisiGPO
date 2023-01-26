# Download the helper library from https://www.twilio.com/docs/python/install
import os
import csv
from twilio.rest import Client
import smtplib
import ssl

port = 465  # For SSL
password = "************"
context = ssl.create_default_context()
sender_email = "**********@gmail.com"
msgsubjecttemplate="""\
Subject: Komitmen Janji Iman 2023 ({}, {})

"""

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
msgtemplate = """Shalom Sdr/i {},

Terima kasih telah mengambil bagian dalam Janji Iman 2023 sebagai berikut:
1. Dukungan Dana: {} - ${}
2. Dukungan Doa: {}
3. Dukungan Daya: {}

Nomor amplop / Kode Janji Iman anda adalah {}.

Dana janji iman dapat disalurkan melalui: 
1) Kotak persembahan di gereja, dengan menuliskan "Janji Iman, [Kode Janji Iman]". Contoh: "Janji Iman, {}"
atau
2) Interbank/ATM Transfer: 
Beneficiary: Orchard Rd Presbyterian Church
Bank: ***/****/***
Account No: ***-***-***-*
Mohon menuliskan di bagian "Comments": Mission Indo [Nama] atau [Kode Janji Iman]". Contoh: "Mission Indo {} {}"
Setelah transfer, mohon info Nama Lengkap & Kode Janji Iman kepada Dkn. ****** ********** (*******).

Terima kasih dan Tuhan Yesus memberkati.

Salam,


Sekretariat Tim Misi """

filename = '********.csv'

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',')
    for row in datareader:
        msgbody = msgtemplate.format(row[0], row[2], row[3], row[4], row[5], row[6], row[6], row[0], row[6])
        # send Email
        msgsubject = msgsubjecttemplate.format(row[1], row[6])
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("**********@gmail.com",password)
            server.sendmail(sender_email, row[-2], msgsubject+msgbody)
        # send SMS
        msgsender = 'TimMisiGPO'
        recipient = row[-1]
        message = client.messages \
            .create(
            body=msgbody,
            from_=msgsender,
            to=recipient
        )
        print(message.sid)



