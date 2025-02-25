from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


mail_recepients = ['ENTER_EMAILID'] 	#DL mail
smtp_relay_server = '8.8.8.8'
# smtp_relay_server = 'ENTER_SMTP_SERVER_URL'
smtp_relay_port = 587 # generally, default port is 587


def send_mail(message_body):
    print("Mail Sent: {}".format(message_body))
    sender = 'noreply@bdcommun.com'
    sender = 'ENTER_EMAILID'
    receivers = mail_recepients
    message = MIMEMultipart()
    message["Subject"] = "Subject: BD_Automation Communication Mail"
    body = message_body
    body = MIMEText(body) # convert the body to a MIME compatible string
    message.attach(body)
    try:
        smtpObj = SMTP(smtp_relay_server, smtp_relay_port)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Successfully sent email")
        smtpObj.quit()
    except SMTPException:
        print("Error: unable to send email")

send_mail("This is test mail")