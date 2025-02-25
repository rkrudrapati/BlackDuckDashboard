"""
This script delete the versions mentioned in the input file
"""

from sys import exit
from re import match
from requests import request, packages
from requests.packages.urllib3.exceptions import InsecureRequestWarning
packages.urllib3.disable_warnings(InsecureRequestWarning)


def request_method(method, url, headers, payload=""):
    try:
        if method == "POST" or method == "PUT":
            request_response = request(method, url, data=payload, headers=headers, verify=False)
        elif method == "GET":
            request_response = request(method, url, headers=headers, verify=False)
        elif method == "DELETE":
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


key_project_name = "test_delete"
server_url = 'https://8.8.8.8/'
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here
if server_url[-1] == "/":
    server_url = server_url[:-1]

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

project_url = f"{server_url}/api/projects?q=name%3A{key_project_name}"
# url = "https://blackduckweb.philips.com/api/projects?q=name%3ARadiology_Solutions_PMT"
data_list = []
with open('input', 'r') as delete_list:
    for lines in delete_list.readlines():
        data_list.append(lines.strip())
    print(data_list)
    delete_list.close()

project_request_response = request_method(method="GET", url=project_url, headers=get_headers)
for items in project_request_response.json()["items"]:
    print(items)
    project_name = items["name"]
    project_link = items["_meta"]["href"]
    project_id = project_link.split('/')[-1]
    if project_name == key_project_name:
        print("Deleting mentioned version in project: %s" % project_name)
        versions_link = f"{project_link}/versions?limit=999"
        versions_request_response = request_method(method="GET", url=versions_link, headers=get_headers)
        count = versions_request_response.json()['totalCount']
        all_version_items = versions_request_response.json()["items"]
        for v_items in all_version_items:
            version_name = v_items['versionName']
            if version_name in data_list:
                version_link = v_items["_meta"]["href"]
                version_id = version_link.split('/')[-1]
                print(f"Deleting version: {version_name})")
                # print(f"Project_ID: {project_id}\nVersion_ID: {version_id}")
                delete_url = f"{server_url}/api/projects/{project_id}/versions/{version_id}"
                delete_request_response = request_method(method="DELETE", url=delete_url, headers=get_headers)
                print(f"Deleted version '{version_name}' in project '{project_name}' \n")
