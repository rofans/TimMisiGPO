# remindcommitmentwa.py

import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
import credentials
import templates

load_dotenv()


def normalize_whatsapp_to(raw: str) -> str:
    """
    Twilio expects: whatsapp:+<E.164>
    Your CSV might store 8 digits, +65..., or already whatsapp:+65...
    """
    raw = (raw or "").strip()
    if not raw:
        raise ValueError("Empty recipient number")

    if raw.startswith("whatsapp:"):
        return raw

    # If it's 8 digits, assume SG and prepend +65
    if raw.isdigit() and len(raw) == 8:
        raw = "+65" + raw

    if not raw.startswith("+"):
        raise ValueError(f"Recipient must be E.164 like +65..., got: {raw}")

    return f"whatsapp:{raw}"


def perform_reminder_wa(file_path: str, send_message: bool = False):
    """
    If send_message=False (default), log messages to a file (preview mode).
    If send_message=True, send via Twilio WhatsApp AND log messages.
    """
    account_sid = credentials.twilio_account_sid
    auth_token = credentials.twilio_auth_token
    wa_from = os.getenv("TWILIO_WHATSAPP_FROM")

    if not account_sid or not auth_token or not wa_from:
        raise RuntimeError("Missing Twilio credentials or TWILIO_WHATSAPP_FROM")

    client = Client(account_sid, auth_token) if send_message else None

    print("inside remind commitment whatsapp")
    print(f"file path is: {file_path}")
    print(f"send_message = {send_message}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log/wa_preview_{timestamp}.log"

    with open(log_filename, "w", encoding="utf-8") as logfile:
        with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
            datareader = csv.reader(csvfile, delimiter=",")
            for idx, row in enumerate(datareader, start=1):
                msgbody = templates.commitment_reminder.format(
                    row[0], row[2], row[3], row[5], row[4], row[6], row[6], row[0], row[6]
                ).strip()

                # Your sample CSV uses last column as phone digits
                to_number = normalize_whatsapp_to(row[-1])

                # Always log final formatted message
                logfile.write(
                    f"--- WA MESSAGE #{idx} ---\n"
                    f"To: {to_number}\n"
                    f"From: {wa_from}\n"
                    f"Body:\n{msgbody}\n"
                    f"{'-'*40}\n\n"
                )

                if send_message:
                    try:
                        message = client.messages.create(
                            body=msgbody,
                            from_=wa_from,
                            to=to_number
                        )
                        print(f"Sent to {to_number} | SID={message.sid}")
                    except Exception as e:
                        print(f"FAILED to send to {to_number}: {e}")
                else:
                    print(f"[PREVIEW] Logged message for {to_number}")

    print(f"\n✔ WhatsApp messages logged to: {log_filename}")
