'''
This script delete the versions mentioned in the input file
Required input: project name -> to be entered in gv_project_name
Enter the user token -> to be entered in api_token
'''

from sys import exit
from re import match
from requests import request
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from os import environ

urllib3.disable_warnings(InsecureRequestWarning)

environ['NO_PROXY'] = 'blackduckweb.philips.com'
environ['NO_PROXY'] = '8.8.8.8'

gv_project_name = "Test_Project"
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here
server_url = 'https://8.8.8.8/'

if server_url[-1] == "/":
    server_url = server_url[:-1]


def get_request_headers():
    get_header = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': 'bearer {}'.format(auth_token)
    }
    return get_header


def post_put_request_headers():
    post_put_request_header = get_request_headers()
    post_put_request_header.update({'X-CSRF-TOKEN': csrf_token})
    return post_put_request_header


def method_request(method, url, payload, headers):
    try:
        if method == "GET" or method == "DELETE":
            method_response = request(f"{method}", url, headers=headers, verify=False)
        elif method == "POST" or method == "PUT":
            method_response = request(f"{method}", url, data=payload, headers=headers, verify=False)
        if match('20[0-4]', str(method_response.status_code)):
            return method_response
        else:
            print('request failed')
            print('Response status: %d' % method_response.status_code)
            print('Method: post_request')
            print('request response: \n %s' % method_response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


data_list =[]
with open('input', 'r') as delete_list:
    print("Formatting the input file")
    for lines in delete_list.readlines():
        data_list.append(lines.strip())
        print(lines.strip())
    # print(data_list)
    delete_list.close()
    print("****************")


csrf_token = ''
auth_token = ''
login_headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Authorization': 'token {}'.format(api_token),
}
login_url = server_url + '/api/tokens/authenticate'
login_response = method_request(method="POST", url=login_url, payload={}, headers=login_headers)
auth_token = login_response.json()['bearerToken']
csrf_token = login_response.headers['X-CSRF-TOKEN']

project_name_url = server_url + f"/api/projects?q=name%3A{gv_project_name}"
project_response = method_request(method="GET", url=project_name_url, payload={}, headers=get_request_headers())
for items in project_response.json().__getitem__("items"):
    project_link = items["_meta"]["href"]
    project_name = items["name"]
    project_id = project_link.split('/')[-1]
    if project_name == gv_project_name:
        versions_link = project_link + "/versions?limit=999"
        versions_response = method_request(method="GET", url=versions_link, payload={}, headers=get_request_headers())
        for v_items in versions_response.json().__getitem__("items"):
            version_name = v_items.__getitem__('versionName')
            if version_name in data_list:
                version_link = v_items["_meta"]["href"]
                print(version_name)
                version_id = version_link.split('/')[-1]
                print(f"Deleting version '{version_name}' in project '{project_name}'")
                delete_url = server_url + f'/api/projects/{project_id}/versions/{version_id}'
                method_request(method="DELETE", url=delete_url, payload={}, headers=post_put_request_headers())
