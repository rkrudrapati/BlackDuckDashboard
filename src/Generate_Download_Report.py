import json
from sys import exit
from re import match
from requests import request
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from icecream import ic
urllib3.disable_warnings(InsecureRequestWarning)


# ic.disable()
# Enter project details here
project_name = "SIG_Markets_MOM"
version_name = "2.0"

server_url = 'https://blackduckweb.philips.com/'
api_token = ""  # Enter api token here
if server_url[-1] == "/":
    server_url = server_url[:-1]
    ic(server_url)


def post_report_headers():
    report_create_headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'X-CSRF-TOKEN': csrf_token,
        'cookie': auth_token
        }
    return report_create_headers


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
    project_url = server_url + f"/api/projects?q=name%3A{project_name}"
    project_response = get_request(url=project_url, headers=get_headers)
    all_project_items = project_response.json()["items"]
    project_id = ""
    for each_items in all_project_items:
        if each_items["name"] == project_name:
            project_id_link = each_items["_meta"]["href"]
            project_id = project_id_link.split("/")[-1]
            break
    if project_id == "":
        ic("Project does not exit.")
        exit()
    return project_id


def find_version_id(project_id, version_name):
    version_url = server_url + f"/api/projects/{project_id}/versions?q=versionName%3A{version_name}"#.format(project_id, version_name)
    version_response = get_request(url=version_url, headers=get_headers)
    all_project_items = version_response.json()["items"]
    version_id = ""
    for each_items in all_project_items:
        if each_items["versionName"] == version_name:
            version_id_link = each_items["_meta"]["href"]
            version_id = version_id_link.split("/")[-1]
            break
    if version_id == "":
        ic("Version does not exit.")
        exit()
    return version_id


def get_report_payload(versionID):
    report_payload.update({'versionId': versionID})
    return report_payload


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
report_payload ={
    'categories': ["VERSION", "CODE_LOCATIONS", "COMPONENTS", "SECURITY", "FILES"],
    'reportFormat': "CSV",
    'reportType': "VERSION",
    # 'reportUrl': "string",
    # 'url': "string",
    'versionId': "",
}
get_headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Accept': "application/json",
    'X-CSRF-TOKEN': csrf_token,
    'authorization': 'bearer {}'.format(auth_token)
    }

project_id = find_project_id(project_name)
version_id = find_version_id(project_id, version_name)
report_payload = report_payload.update({'versionId': version_id})
report_create_response = post_request(url=version_report_link, payload=report_payload, headers=post_request_headers())


##################################
# from src.P1_login import login_to_bd_server
# from src.P1_headers import get_request_headers, post_request_headers
# from src.P1_my_requests import get_request, post_request
# import src.P1_blackduck_utils as bd_utils
# import src.P1_gv_variables as variables
#
#
# server_url = variables.server_url
# login_to_bd_server(url=server_url, username=variables.username, password=variables.password)
#
# get_headers = get_request_headers()
# url = server_url + "api/projects?q=name%3A" + "%s" %(variables.key_project_name)
#
# project_response = get_request(url=url, headers=get_headers)
# all_project_items = bd_utils.items_in_response(response=project_response)
#
# for items in all_project_items:
#     project_link = bd_utils.get_project_link(items)
#     project_name = bd_utils.get_project_name(items)
#     project_id = project_link.split('/')[-1]
#     if project_name == variables.key_project_name:
#         versions_link = bd_utils.link_to_select_version(items,variables.key_version_name)
#         versions_response = get_request(url=versions_link, headers=get_headers)
#         count = versions_response.json()['totalCount']
#         if count != 1:
#             print("Msg1: Wrong version name entered")
#             break
#         all_version_items = bd_utils.items_in_response(response=versions_response)
#         for v_items in all_version_items:
#             version_name = v_items['versionName']
#             if version_name != variables.key_version_name:
#                 print("Msg2: Wrong version name entered")
#                 break
#             version_report_link = bd_utils.identify_href_link(v_items, 'versionReport')
#             version_id = v_items["_meta"]["href"].split('/')[-1]
#             report_payload = bd_utils.get_report_payload(version_id)
#             report_create_headers = post_request(url=version_report_link, payload=report_payload, headers=post_request_headers())
