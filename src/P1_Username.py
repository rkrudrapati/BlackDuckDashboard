from src.P1_api_headers import get_request_headers
from src.P1_my_requests import get_request
import src.P1_gv_variables as variables
from src.P1_login import login_to_bd_server_via_token
from os import environ
environ['NO_PROXY'] = 'blackduckweb.philips.com'


send_no_mail = [''] # Enter details here
ex_exployee = ['']  # Enter details here
new_emails = send_no_mail.append(ex_exployee)
if new_emails != "":
    new_emails = new_emails.lower()
    new_emails = new_emails.split(",")
    ex_exployee.extend(new_emails)

# update the ex_employee list once the new_emails are added. this has to be done manually, by printing the ex_employee and replace the variable/value
# this activity need to be done after every communication mail.

send_no_mail.extend(ex_exployee)
# print(send_no_mail)
server_url = variables.server_url
login_to_bd_server_via_token()
get_headers = get_request_headers()
# url = server_url + '/api/users?sort=userName%20ASC&offset=0&limit=1000'
# url = server_url + '/api/users?q=userName:ENTER_EMAILID'
# url = server_url + '/api/users?filter=userStatus%3Atrue&q=internal%3AENTER_EMAILID'
for offset_value in range(0, 5000, 1000):
    url = server_url + f'/api/users?filter=userStatus%3Atrue&sort=userName%20ASC&offset={offset_value}&limit=1000'
    response = get_request(url, headers=get_headers)
    # print(response.json())
    for items in response.json()['items']:
        if items['email'] != "":
            if str(items['email']).lower() in send_no_mail:
                pass
            else:
                # pass
                print(items['email'])
