# import json
# from sys import exit
# from re import match
# from requests import request, packages
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# packages.urllib3.disable_warnings(InsecureRequestWarning)
#
#
# server_url = 'https://blackduckweb.philips.com/'
# api_token = "M2E4ZjViYTQtYmNhNy00YzM0LTgzY2ItNmYwODU4ZWIzMmM2OjdlYjAyY2E1LWNhYzMtNDY3MS1hNDY1LTAxYzBmMjEwYWY5Mw=="  # Enter api token here
# if server_url[-1] == "/":
#     server_url = server_url[:-1]
#
#
# def request_method(method, url, headers, payload=""):
#     try:
#         if method == "POST" or method == "PUT":
#             request_response = request(method, url, data=payload, headers=headers, verify=False)
#         elif method == "GET":
#             request_response = request(method, url, headers=headers, verify=False)
#
#         if match('20[0-4]', str(request_response.status_code)):
#             return request_response
#         else:
#             print('request failed')
#             print(f'Response status: {request_response.status_code}')
#             print(f'Method: {method}')
#             print(f'request response: \n {request_response.text}')
#             exit()
#     except Exception as err:
#         print(err)
#         exit()
#
#
# csrf_token = ''
# auth_token = ''
# login_headers = {
#     'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
#     'Authorization': 'token {}'.format(api_token),
# }
#
# login_url = server_url + '/api/tokens/authenticate'
# response = request_method(method="POST", url=login_url, payload={}, headers=login_headers)
# auth_token = response.json()['bearerToken']
# csrf_token = response.headers['X-CSRF-TOKEN']
# get_headers = {
#     'Content-Type': "application/json",
#     'cache-control': "no-cache",
#     'X-Requested-With': "XMLHttpRequest",
#     'Accept': "application/json",
#     'X-CSRF-TOKEN': csrf_token,
#     'authorization': 'bearer {}'.format(auth_token)
# }
#
# user_roles_details = f"{server_url}/api/users/b520df32-4413-41be-b6f8-5c2f8c65ac30/roles?limit=1000"
# user_roles_details_response = request_method(method="GET", url=user_roles_details, headers=get_headers)
# # print(user_roles_details_response.json())
# for items in user_roles_details_response.json()['items']:
#     print(items)
#     if items['roleKey'] == "projectcodescanner" or items['roleKey'] == "projectviewer":
#         pass
#     else:
#         print(items['roleKey'])
#         print(items['scope'])
import json

with open(r"C:\Users\code1\Desktop\_temp\_delete\tajenkinsroles.txt", 'r') as tajenkinsroles:
     tajenkinsroles_json_data = json.load(tajenkinsroles)
     for items in tajenkinsroles_json_data["items"]:
         # print(items)
         if items['roleKey'] == "projectcodescanner" or items['roleKey'] == "projectviewer":
             pass
         else:
             print(items['roleKey'])
             print(items['scope'])

