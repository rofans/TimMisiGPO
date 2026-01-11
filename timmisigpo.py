import sys
import remindcommitmentemail
import remindcommitmentsms
import remindcommitmentwa

print('argument list', sys.argv)

module = sys.argv[1]

print("Executed module: {}".format(module))

if module == '-remindCommitmentSMS':
    remindcommitmentsms.perform_reminder_sms(sys.argv[3])

if module == '-remindCommitmentEmail':
    remindcommitmentemail.perform_reminder_email(sys.argv[3])

if module == '-remindCommitmentWA':
    remindcommitmentwa.perform_reminder_wa(sys.argv[3])
