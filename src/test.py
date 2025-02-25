# # import random
# # #Generate 5 random numbers between 10 and 30
# # randomlist = random.sample(range(1, 91), 15)
# # randompositions = random.sample(range(1, 10), 5)
# # print(randomlist)
# # print(randompositions)
#
#
# # C:\Users\code1\Desktop\_temp\Maheshan\a
# pat = r"C:\Users\code1\Desktop\_temp\Maheshan\a"
# dest = r"C:\Users\code1\Desktop\_temp\Maheshan\a\reports"
# from os import walk, path
# for root, dirs, files in walk(pat):
#     # print(path.join(root, files))
#     for file in files:
#         if "security" in file:
#             # print(path.join(root, file))
#             source = path.join(root, file)
#             directory = source.split("\\")
#             directory = directory[7].strip("Docker_Base_Image_Scan-")
#             destination = dest + "\\" + directory + ".xlsx"
#             print(destination)

# from os import system
#
# system("ping blackduckweb.philips.com")




from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


mail_recepients = ['ENTER_EMAILID', 'ENTER_EMAILID'] 	#DL mail
# smtp_relay_server = '8.8.8.8'
smtp_relay_server = 'ENTER_SMTP_SERVER_URL'
smtp_relay_port = 587 # generally, default port is 587


def send_mail(message_body):
    print("Mail Sent: {}".format(message_body))
    # sender = 'noreply@bdcommun.com'
    sender = 'ENTER_EMAILID'
    receivers = mail_recepients
    message = MIMEMultipart()
    message["Subject"] = "TEST: Black Duck Project Business details"
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

# send_mail("This is test mail")
message = '''
We are reaching out to you as we think you are directly/indirectly related to the project "Project_name" in Black duck hub. 
The project has been mapped to the below Business currently. 
Cluster:""
Business: ""
Business Category: ""

As we got an updated business details for the Connected care cluster, we would request you to check the attached PBS deck and let us know the updated Business details of the project "Project_name".
'''

send_mail(message)