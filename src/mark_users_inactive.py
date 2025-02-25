import json
from sys import exit
from re import match
from requests import request, packages
from requests.packages.urllib3.exceptions import InsecureRequestWarning
packages.urllib3.disable_warnings(InsecureRequestWarning)


server_url = 'https://blackduckweb.philips.com/'
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here
if server_url[-1] == "/":
    server_url = server_url[:-1]


def request_method(method, url, headers, payload=""):
    try:
        if method == "POST" or method == "PUT":
            request_response = request(method, url, data=payload, headers=headers, verify=False)
        elif method == "GET":
            request_response = request(method, url, headers=headers, verify=False)

        if match('20[0-4]', str(request_response.status_code)):
            return request_response
        else:
            print('request failed')
            print(f'Response status: {request_response.status_code}')
            print(f'Method: {method}')
            print(f'request response: \n {request_response.text}')
            exit()
    except Exception as err:
        print(err)
        exit()


def mark_user_inactive(user_items={}):
    # print(user_items)
    user_details_link = user_items["_meta"]["href"]
    username = user_items["userName"]
    type = user_items["type"]
    if type == "INTERNAL":
        return 0
    externalusername = user_items["externalUserName"]
    firstname = user_items["firstName"]
    lastname = user_items["lastName"]
    email = user_items["email"]
    data = {"userName": username, "externalUserName": externalusername, "firstName": firstname, "lastName": lastname,
            "email": email, "type": type, "active": False}  # {items["active"]
    new_data = json.dumps(data)
    request_method(method="PUT", url=user_details_link, payload=new_data, headers=get_headers)
    print(f"user marked inactive: {username}")
    return 0


csrf_token = ''
auth_token = ''
login_headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Authorization': 'token {}'.format(api_token),
}

login_url = server_url + '/api/tokens/authenticate'
response = request_method(method="POST", url=login_url, payload={}, headers=login_headers)
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

ex_employee = [""] # Add employee details here

# get the ex_exployee list from the P1_Username.py file
''' 
The below activity should be done manually:
use the following url to get the dormant user details: https://blackduckweb.philips.com/api/dormant-users?sinceDays=365&offset=0&limit=2500&sort=userName%20ASC
Note: Sometimes the limit can only be 1000 max value. In this case, we have to do it multiple times by increasing the offset by value of 1000's  Eg: 0,1000, 2000 etc.,
Save this data in file(say 'dormant_users_365.txt')
'''
with open('dormant_users_365.txt', 'r') as dormant_raw_data:   #    dormant_users_365      stage_inactive
    dormant_json_data = json.load(dormant_raw_data)
    for dormant_users in dormant_json_data['items']:
        dormant_username = dormant_users['username'].lower()
        if dormant_username not in ex_employee:
            ex_employee.append(dormant_username)

ex_employee.sort()
count = 1

for offset_value in range(0, 5000, 1000):
    user_list_url = server_url + f'/api/users?filter=userStatus%3Atrue&sort=userName%20ASC&offset={offset_value}&limit=1000'
    user_details_response = request_method(method="GET", url=user_list_url, headers=get_headers)
    for items in user_details_response.json()['items']:
        if items['email'] != "":
            if str(items['email']).lower() in ex_employee and items['active']:
                mark_user_inactive(items)
                # print(f"Mark the user {items['email']} as inactive")
            else:
                pass

