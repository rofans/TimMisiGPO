import sys
import remindcommitmentemail
import remindcommitmentsms
import remindcommitmentwa

# NEW clarification modules (filenames as you specified)
import klarifikasiemail
import klarifikasisms

print('argument list:', sys.argv)

if len(sys.argv) < 2:
    raise RuntimeError("Missing module parameter")

module = sys.argv[1]
send_message = "-sendmessage" in sys.argv

print(f"Executed module: {module}")
print(f"send_message = {send_message}")

# Find filePath value safely
def get_arg_value(flag):
    if flag in sys.argv:
        idx = sys.argv.index(flag)
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return None

file_path = get_arg_value("-filePath")

if not file_path:
    raise RuntimeError("Missing -filePath argument")

# -------------------------
# Single reminder modules
# -------------------------
if module == '-remindCommitmentSMS':
    remindcommitmentsms.perform_reminder_sms(file_path, send_message=send_message)

elif module == '-remindCommitmentEmail':
    remindcommitmentemail.perform_reminder_email(file_path, send_message=send_message)

elif module == '-remindCommitmentWA':
    remindcommitmentwa.perform_reminder_wa(file_path, send_message=send_message)

# -------------------------
# Combined reminder modules
# -------------------------
elif module == '-remindCommitmentEmailSMS':
    print("\n=== Running Reminder Email ===")
    remindcommitmentemail.perform_reminder_email(file_path, send_message=send_message)

    print("\n=== Running Reminder SMS ===")
    remindcommitmentsms.perform_reminder_sms(file_path, send_message=send_message)

elif module == '-remindCommitmentAll':
    print("\n=== Running Reminder Email ===")
    remindcommitmentemail.perform_reminder_email(file_path, send_message=send_message)

    print("\n=== Running Reminder SMS ===")
    remindcommitmentsms.perform_reminder_sms(file_path, send_message=send_message)

    print("\n=== Running Reminder WhatsApp ===")
    remindcommitmentwa.perform_reminder_wa(file_path, send_message=send_message)

# -------------------------
# Single clarification modules
# -------------------------
elif module == '-klarifikasiEmail':
    klarifikasiemail.perform_klarifikasi_email(file_path, send_message=send_message)

elif module == '-klarifikasiSMS':
    klarifikasisms.perform_klarifikasi_sms(file_path, send_message=send_message)

# -------------------------
# Combined clarification modules
# -------------------------
elif module == '-klarifikasiEmailSMS':
    print("\n=== Running Klarifikasi Email ===")
    klarifikasiemail.perform_klarifikasi_email(file_path, send_message=send_message)

    print("\n=== Running Klarifikasi SMS ===")
    klarifikasisms.perform_klarifikasi_sms(file_path, send_message=send_message)

else:
    raise RuntimeError(f"Unknown module: {module}")
