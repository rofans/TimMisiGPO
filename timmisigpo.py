import sys
import remindcommitmentemail
import remindcommitmentsms
import remindcommitmentwa

print('argument list:', sys.argv)

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

if module == '-remindCommitmentSMS':
    remindcommitmentsms.perform_reminder_sms(
        file_path,
        send_message=send_message
    )

elif module == '-remindCommitmentEmail':
    remindcommitmentemail.perform_reminder_email(
        file_path,
        send_message=send_message
    )

elif module == '-remindCommitmentWA':
    remindcommitmentwa.perform_reminder_whatsapp(
        file_path,
        send_message=send_message
    )
