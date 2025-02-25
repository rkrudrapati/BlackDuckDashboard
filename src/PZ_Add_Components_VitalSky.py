import json
from sys import exit
from re import match
from requests import request, packages
from requests.packages.urllib3.exceptions import InsecureRequestWarning
packages.urllib3.disable_warnings(InsecureRequestWarning)
import urllib.parse

server_url = 'https://8.8.8.8/'
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


filePath = r"C:\Users\code1\Desktop\_Work\SCoE\2670_[Retest]VitalSky_3.1.0\scoe\OpenSource\opensource_2.json"
with open(filePath, 'r') as raw_json_data:
    json_data = json.load(raw_json_data)
    for items in json_data:
        component_name = items['name']
        safe_string = urllib.parse.quote_plus(component_name)
        # component_search_url = f"{server_url}/api/components/autocomplete?limit=200&filter=componentType%3Akb_component&filter=componentType%3Acustom_component&q={safe_string}"
        # component_search_url = "https://8.8.8.8/api/search/kb-components?limit=100&offset=0&q=%40angular%2Fanimation"
        # print(component_search_url)
        # component_search_response = request_method(method="GET", url=component_search_url, headers=get_headers)
        # print(component_search_response.json())
        # if len(items['versions']) > 1:
        #     print(component_name + " | " + str(items['versions']))
        for version_name in items['versions']:
            # getting component search options
            print(component_name + " | " + version_name )

