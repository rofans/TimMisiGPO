import sys
import csv
import os
from dotenv import load_dotenv
from twilio.rest import Client
import credentials
import templates

load_dotenv()

def normalize_whatsapp_to(raw: str) -> str:
    """
    Twilio expects: whatsapp:+<E.164>
    Your CSV might store +65..., or already whatsapp:+65...
    """
    raw = (raw or "").strip()
    if not raw:
        raise ValueError("Empty recipient number")
    if raw.startswith("whatsapp:"):
        return raw
    if not raw.startswith("+"):
        raise ValueError(f"Recipient must be E.164 like +65..., got: {raw}")
    return f"whatsapp:{raw}"

def perform_reminder_wa(file_path: str):
    account_sid = credentials.twilio_account_sid
    auth_token = credentials.twilio_auth_token
    wa_from = os.getenv("TWILIO_WHATSAPP_FROM")

    if not account_sid or not auth_token or not wa_from:
        raise RuntimeError("Missing TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN / TWILIO_WHATSAPP_FROM in .env")

    client = Client(account_sid, auth_token)

    print("inside remind commitment whatsapp")
    print(f"file path is: {file_path}")

    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        datareader = csv.reader(csvfile, delimiter=",")
        for row in datareader:
            # Build WhatsApp message body (keep it shorter than email)
            # You can reuse your existing template, or make a WhatsApp-specific one.
            msgbody = templates.commitment_reminder.format(
                row[0], row[2], row[3], row[5], row[4], row[6], row[6], row[0], row[6]
            ).strip()

            to_number = normalize_whatsapp_to(row[-1])

            try:
                message = client.messages.create(
                    body=msgbody,
                    from_=wa_from,
                    to=to_number
                )
                print(f"Sent to {to_number} | SID={message.sid}")
            except Exception as e:
                print(f"FAILED to send to {to_number}: {e}")

if __name__ == "__main__":
    perform_reminder_whatsapp(sys.argv[1])
