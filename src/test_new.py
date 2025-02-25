# from os import system
#
# system("ping blackduckweb.philips.com")




# from smtplib import SMTP, SMTPException
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
#
# mail_recepients = ['ENTER_EMAILID'] 	#DL mail
# smtp_relay_server = '8.8.8.8'
# # smtp_relay_server = 'ENTER_SMTP_SERVER_URL'
# smtp_relay_port = 587 # generally, default port is 587
#
#
# def send_mail(message_body):
#     print("Mail Sent: {}".format(message_body))
#     # sender = 'noreply@bdcommun.com'
#     sender = 'ENTER_EMAILID'
#     receivers = mail_recepients
#     message = MIMEMultipart()
#     message["Subject"] = "Subject: Black Duck Project Business details"
#     body = message_body
#     body = MIMEText(body) # convert the body to a MIME compatible string
#     message.attach(body)
#     try:
#         smtpObj = SMTP(smtp_relay_server, smtp_relay_port)
#         smtpObj.sendmail(sender, receivers, message.as_string())
#         print("Successfully sent email")
#         smtpObj.quit()
#     except SMTPException:
#         print("Error: unable to send email")
#
# # send_mail("This is test mail")
# message = '''
# We are reaching out to you as we think you are directly/indirectly related to the project "Project_name" in Black duck hub.
# The project has been mapped to the below Business currently.
# Cluster:""
# Business: ""
# Business Category: ""
#
# As we got an updated business details for the Connected care cluster, we would request you to check the attached PBS deck and let us know the updated Business details of the project "Project_name".
# '''
#
# send_mail(message)


# print("Hello World")

a = ""
a = a.lower()
a = a.split(", ")
print(a)