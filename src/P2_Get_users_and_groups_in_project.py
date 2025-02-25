
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


hub_link = 'https://blackduckweb.philips.com'
get_headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Accept': "application/json",
    'cookie': "AUTHORIZATION_BEARER=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJodWJfaWQiOiJkODNmMWU3Zi0zYTViLTQwMDQtODkyZi0wYWI3MGIzN2EyMWUiLCJ1c2VyX25hbWUiOiJyYWpraXJhbi5yQHBoaWxpcHMuY29tIiwic2NvcGUiOlsid3JpdGUiLCJyZWFkIiwiY2xpZW50X21hbmFnZW1lbnQiXSwiY3NyZiI6InVSdVkxaXhod3l5WVJBTFZ2WkNvQWxNenNXQ3pPRGlCT3NrdThXVlJURnV2UlRDd3J5TGNCRlBXMWgzL3lxUHMiLCJleHAiOjE1ODUxNTA0ODQsImF1dGhvcml0aWVzIjpbIkNPTkZJR19DT01NT04iLCJSRUxFQVNFX0xJU1QiLCJQUk9KRUNUX1JFQUQiLCJUQUdfUkVBRCIsIk5PVElGSUNBVElPTl9SRUFEIiwiVlVMTkVSQUJJTElUWVJFTUVESUFUSU9OX1JFQUQiLCJBQ1RJVklUWVNUUkVBTV9SRUFEIiwiU0NBTl9SRUFEIiwiUE9MSUNZX1JVTEVfUkVBRCIsIlNDQU5fREVMRVRFIiwiVlVMTkVSQUJJTElUWV9SRUFEIiwiQ09ORklHX1JFQUQiLCJQUk9KRUNUX1NDSEVEVUxFIiwiU0NBTl9VUERBVEUiLCJUQUdfQ1JFQVRFIiwiTElDRU5TRV9DUkVBVEUiLCJVU0VSTUdNVF9DUkVBVEUiLCJDVVNUT01fQ09NUE9ORU5UX0RFTEVURSIsIkNPTkZJR19DUkVBVEUiLCJQUk9KRUNUX0xJU1QiLCJKT0JfUkVBRCIsIkNPREVMT0NBVElPTl9SRUFEIiwiQ1VTVE9NX0ZJRUxEX1JFQUQiLCJDVVNUT01fQ09NUE9ORU5UX1VQREFURSIsIkxJQ0VOU0VfREVMRVRFIiwiUE9MSUNZX1JVTEVfVVBEQVRFIiwiU0NBTl9DUkVBVEUiLCJTRUFSQ0hfUkVJTkRFWCIsIk9BVVRIX0NMSUVOVF9DUkVBVEUiLCJDVVNUT01fRklFTERfVVBEQVRFIiwiRVhURVJOQUxfRVhURU5TSU9OX0NSRUFURSIsIlBST0pFQ1RfREVMRVRFIiwiUkVWSUVXX0NSRUFURSIsIkJPTUNPTVBPTkVOVElTU1VFX0RFTEVURSIsIkNPTkZJR19VUERBVEUiLCJDVVNUT01fRklFTERfQ1JFQVRFIiwiT0FVVEhfQ0xJRU5UX1JFQUQiLCJSRUxFQVNFX1JFQUQiLCJSRVZJRVdfVVBEQVRFIiwiVEVBTU1FTUJFUl9SRUFEIiwiVVNFUk1HTVRfUkVBRCIsIlJFVklFV19SRUFEIiwiRVhURVJOQUxfRVhURU5TSU9OX1JFQUQiLCJQUk9KRUNUX1NFQVJDSCIsIk9BVVRIX0NMSUVOVF9VUERBVEUiLCJUQUdfREVMRVRFIiwiQ1VTVE9NX0NPTVBPTkVOVF9DUkVBVEUiLCJFWFRFUk5BTF9FWFRFTlNJT05fREVMRVRFIiwiVVNFUk1HTVRfREVMRVRFIiwiVEFHX1VQREFURSIsIkVYVEVSTkFMX0VYVEVOU0lPTl9VUERBVEUiLCJFWFRFUk5BTF9FWFRFTlNJT05fQVVUSEVOVElDQVRFIiwiSk9CX0RFTEVURSIsIk9BVVRIX0NMSUVOVF9ERUxFVEUiLCJSRUxFQVNFX0NSRUFURSIsIkNPREVMT0NBVElPTl9ERUxFVEUiLCJMSUNFTlNFX1JFQUQiLCJVU0VSTUdNVF9VUERBVEUiLCJKT0JfVVBEQVRFIiwiV0FUQ0hJVEVNX0NSRUFURSIsIlBPTElDWV9SVUxFX0NSRUFURSIsIkJPTUNPTVBPTkVOVElTU1VFX0NSRUFURSIsIkNPREVMT0NBVElPTl9VUERBVEUiLCJVU0VSX05PVElGSUNBVElPTl9SRUFEIiwiV0FUQ0hJVEVNX1JFQUQiLCJDVVNUT01fRklFTERfREVMRVRFIiwiUE9MSUNZX1JVTEVfREVMRVRFIiwiTElDRU5TRV9VUERBVEUiLCJXQVRDSElURU1fREVMRVRFIiwiQ09ERUxPQ0FUSU9OX0NSRUFURSIsIkNPTkZJR19ERUxFVEUiLCJCT01fUkVBRCIsIlZVTE5fREJfQ09QWV9DUkVBVEUiLCJCT01DT01QT05FTlRJU1NVRV9VUERBVEUiLCJKT0JfQ1JFQVRFIiwiUFJPSkVDVF9DUkVBVEUiLCJSRVZJRVdfREVMRVRFIiwiVVJMTElOS19SRUFEIl0sImp0aSI6IjBjMWFlODgwLTc1YmQtNGQzMy04MzUzLTNlYjJiN2FkNWMyMSIsImNsaWVudF9pZCI6IjAwMDAwMDAwLTAwMDAtNDAwMC0wMDAwLTAwMDAwMDAwMDAwMSJ9.IGZnWHik3_2nTWAChzXIW8tM-ti2w4UDJscdmq-UQ_jVf_NI4fkx-NLiHoienZqCUxCA92wMaZRpMyW82S8WU4iHFy1SZfIyVl7qQap5Rx3WsxNvIO14a76n6mteV0EWFSogK0XKk6iHIFsCMA0PWVuo33UJ3nKFKAnP7FFz5D_M0D-DQfw7NJs-dw_OSE-_yPGrE_hlTSFMrDum4mdi6mik6YKIqM6MgYvVBpbC8ywWWvQ2U-TmdafVhEG50Nt9pK2f8iXN6Vrpp5gZC8k1NvaZxJ26jOGrvSrThBwzdVeBX9CrvW5_y6J15GjX_izS-fB2y38Fz6wiIyTqzJWGCw; Max-Age=7200; Expires=Wed, 25-Mar-2020 15:34:44 GMT; Path=/; secure; Secure; HttpOnly"
}

def post_request(url, payload, headers):
    try:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        if response.status_code == 204:  # re.match(r'20(0|4)'):    # checks 200 or 204
            print(response.status_code)
            return response
        else:
            print('request failed')
            print('Response status: %d' % (response.status_code))
            print('Method: post_request')
            print('request response: \n %s' % response.text)
    except Exception as err:
        print(err)


def get_request(url, headers):
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if response.status_code == 200 or response.status_code == 204:  # re.match(r'20[0-9]'):    # check 200 to 209
            return response
        else:
            print('request failed')
            print('Response status: %d' % (response.status_code))
            print('Method: get_request')
            print('request response: \n %s' % response.text)
    except Exception as err:
        print(err)

def login():
    payload = {"j_username": "ENTER_EMAILID", "j_password": ""}
    login_url = hub_link + '/j_spring_security_check'
    login_headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json, text/javascript, */*; q=0.01"
    }
    response = post_request(url=login_url, payload=payload, headers=login_headers)
    lv_token = response.headers['Set-Cookie']
    get_headers.update({'cookie': lv_token})
    print(lv_token)


def users_list(project_id):
    url = "https://blackduckweb.philips.com/api/projects/{}/users?limit=999".format(project_id)
    response = get_request(url=url, headers=get_headers)
    for each_item in response.json()["items"]:
        print(each_item["name"])


def user_groups(project_id):
    url = "https://blackduckweb.philips.com/api/projects/{}/usergroups?limit=999".format(project_id)
    response = get_request(url=url, headers=get_headers)
    for each_item in response.json()["items"]:
        print(each_item["name"])


def runner(project_id):
    # login()
    users_list(project_id)
    user_groups(project_id)


id = "3dc8f5bd-583f-4b08-91c3-b5f241ad62d5"
runner(id)