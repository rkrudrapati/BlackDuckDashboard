from sys import exit
from re import match
from requests import request


server_url = 'https://blackduckweb.philips.com/'
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here
if server_url[-1] == "/":
    server_url = server_url[:-1]


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


