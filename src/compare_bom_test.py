from sys import exit
from re import match
from requests import request
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


from os import environ
environ['NO_PROXY'] = 'blackduckweb.philips.com'


# Enter project details here
base_project_name = "RadOnc_auth-service"
base_version_name = "2.0.21222.38820"
new_project_name = "test_project_3"
new_version_name = "radonc_centos_base"

server_url = 'https://blackduckweb.philips.com/'
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here
if server_url[-1] == "/":
    server_url = server_url[:-1]
print(server_url)


mail_recepients = [''] 	#DL mail    # Enter mail ID here
smtp_relay_server = '' # Relay server details
smtp_relay_port = 587 # generally, default port is 587


def send_mail(file):
    # print("Mail Sent: {}".format(message_body))
    sender = 'noreply_automation@philips.com'
    receivers = mail_recepients
    message = MIMEMultipart()
    message["Subject"] = "Subject: BD_Automation Comparison Mail"
    # body = message_body
    # body = MIMEText(body) # convert the body to a MIME compatible string
    # message.attach(body)
    try:
        # open and read the CSV file in binary
        with open(file, 'rb') as file_input:
            # Attach the file with filename to the email
            message.attach(MIMEApplication(file_input.read(), Name=file))
            print(message)
        # smtpObj = SMTP(smtp_relay_server, smtp_relay_port)
        # smtpObj.sendmail(sender, receivers, message.as_string())
        # print("Successfully sent email")
        # smtpObj.quit()

    except SMTPException:
        print("Error: unable to send email")


def post_request(url, payload, headers):
    try:
        post_response = request("POST", url, data=payload, headers=headers, verify=False)
        if match('20[0-4]', str(post_response.status_code)):
            return post_response
        else:
            print('request failed')
            print('Response status: %d' % post_response.status_code)
            print('Method: post_request')
            print('request response: \n %s' % post_response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


def get_request(url, headers):
    try:
        get_response = request("GET", url, headers=headers, verify=False)
        if match('20[0-4]', str(get_response.status_code)):
            return get_response
        else:
            print('request failed')
            print('Response status: %d' % get_response.status_code)
            print('Method: get_request')
            print('request response: \n %s' % get_response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


def find_project_id(project_name):
    project_url = server_url + "/api/projects?q=name%3A" + "%s" % project_name
    project_response = get_request(url=project_url, headers=get_headers)
    all_project_items = project_response.json()["items"]
    project_id = ""
    for each_items in all_project_items:
        if each_items["name"] == project_name:
            project_id_link = each_items["_meta"]["href"]
            project_id = project_id_link.split("/")[-1]
            break
    if project_id == "":
        print("Project does not exit.")
        exit()
    return project_id


def find_version_id(version_name, project_id):
    version_url = server_url + f"/api/projects/{project_id}/versions?q=name%3A{version_name}"
    version_response = get_request(url=version_url, headers=get_headers)
    print(version_response.json()["items"])
    all_project_items = version_response.json()["items"]
    version_id = ""
    for each_items in all_project_items:
        if each_items["versionName"] == version_name:
            version_id_link = each_items["_meta"]["href"]
            version_id = version_id_link.split("/")[-1]
            break
    if version_id == "":
        print("Version does not exit.")
        exit()
    return version_id


csrf_token = ''
auth_token = ''
login_headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Authorization': 'token {}'.format(api_token),
}


login_url = server_url + '/api/tokens/authenticate'
response = post_request(url=login_url, payload={}, headers=login_headers)
auth_token = response.json()['bearerToken']
csrf_token = response.headers['X-CSRF-TOKEN']
get_headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Accept': "application/json",
    'X-CSRF-TOKEN': csrf_token,
    'authorization': 'bearer {}'.format(auth_token)
    }
base_project_id = find_project_id(base_project_name)
if base_project_name != new_project_name:
    new_project_id = find_project_id(new_project_name)
else:
    new_project_id = base_project_id

base_version_id = find_version_id(base_version_name, base_project_id)
new_version_id = find_version_id(new_version_name, new_project_id)

# url = server_url + "/api/risk-profile-dashboard?limit=25"
# url: old or base version / next comes / new or latest version
# eg: 1.0 compared to 2.0
# 1.0 id will come 1st and then 2.0 will come
# compare_url = server_url + f"/api/projects/{base_project_id}/versions/{base_version_id}/compare/projects/{new_project_id}/versions/{new_version_id}/components?limit=1000&sortField=component.securityRiskProfile&ascending=false&offset=0"
newly_url = server_url + f"/api/projects/{base_project_id}/versions/{base_version_id}/compare/projects/{new_project_id}/versions/{new_version_id}/components?filter=componentState%3AADDED&limit=1000&sortField=component.securityRiskProfile&ascending=false&offset=0"
changed_url = server_url + f"/api/projects/{base_project_id}/versions/{base_version_id}/compare/projects/{new_project_id}/versions/{new_version_id}/components?filter=componentState%3ACHANGED&limit=1000&sortField=component.securityRiskProfile&ascending=false&offset=0"
removed_url = server_url + f"/api/projects/{base_project_id}/versions/{base_version_id}/compare/projects/{new_project_id}/versions/{new_version_id}/components?filter=componentState%3AREMOVED&limit=1000&sortField=component.securityRiskProfile&ascending=false&offset=0"

with open('comparision_output.csv', 'w') as file:
    print("Component Name,Version Name,Change")
    file.writelines("Component Name,Version Name,Change")
    newly_added_response = get_request(url=newly_url, headers=get_headers)
    for items in newly_added_response.json()["items"]:
        output_data = ""
        component = items["component"]["componentName"]
        version = items["component"]["componentVersionName"]
        output_data = "{},{},Added".format(component, version)
        if output_data != "":
            print(output_data)
            file.writelines(output_data)
    changed_response = get_request(url=changed_url, headers=get_headers)
    for items in changed_response.json()["items"]:
        output_data = ""
        component = items["component"]["componentName"]
        version = items["component"]["componentVersionName"]
        output_data = "{},{},Modified".format(component, version)
        if output_data != "":
            print(output_data)
            file.writelines(output_data)
    removed_response = get_request(url=removed_url, headers=get_headers)
    for items in removed_response.json()["items"]:
        output_data = ""
        component = items["component"]["componentName"]
        version = items["component"]["componentVersionName"]
        output_data = "{},{},Deleted".format(component, version)
        if output_data != "":
            print(output_data)
            file.writelines(output_data)

send_mail('comparision_output.csv')
file.close()
