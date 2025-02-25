"""
This is the POC to retrieve the comments from the components dashboard page.
The POC will only retrieve comments from a particular component which is hardcoded in this case
Project id: Test_Project1
aa024496-9ae8-4434-8bf1-3c92e82593d4
Version id: test_1
a6f09d62-98a9-43e1-b497-bf82cf8348bf
Component_Name: a connector factory
6f7fa552-2e95-4664-8b7b-ad6ca07253fd
Component_Version_Name: 0.0.7
3b8d2a3e-36a9-43ef-8f54-54e50adb68b5

Enter the password to run this POC
"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


portal = 'https://8.8.8.8'
url = portal + '/j_spring_security_check'
payload = 'j_username=ENTER_USERNAME&j_password=ENTER_PASSWORD'

headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/javascript, */*; q=0.01",
}

response = requests.request("POST", url, data=payload, headers=headers, verify=False)
if response.status_code == 200 or response.status_code == 204:
    print("Login Successful")
else:
    print("Failed to Login")

token = response.headers['Set-Cookie']
# print(token)
headers.update({'cookie': token})

comments_url_poc = portal + "/api/projects/aa024496-9ae8-4434-8bf1-3c92e82593d4/versions/a6f09d62-98a9-43e1-b497-bf82cf8348bf/components/6f7fa552-2e95-4664-8b7b-ad6ca07253fd/component-versions/3b8d2a3e-36a9-43ef-8f54-54e50adb68b5/comments"
# print(headers)
response = requests.get(url=comments_url_poc, headers=headers, verify=False)
# print(response.json()["items"][i]["comment"])
for items in response.json()["items"]:
    comment = items["comment"]
    user = items["user"]["email"]
    # user = str(user).split("@")[0]
    print("{}: {}".format(user, comment))