import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from sys import exit


# re.match(r'20(0|1|2|3|4|5|6|7|8|9)')
def post_request(url, payload, headers):
    try:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        # if response.status_code == 204 or response.status_code == 201:  # re.match(r'20(0|4)'):    # checks 200 or 204
        if re.match('20[0-4]', str(response.status_code)):
            # print(response.status_code)
            return response
        else:
            print('request failed')
            print('Response status: %d' % response.status_code)
            print('Method: post_request')
            print('request response: \n %s' % response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


def put_request(url, payload, headers):
    try:
        response = requests.request("PUT", url, data=payload, headers=headers, verify=False)
        if re.match('20[0-4]', str(response.status_code)):
            return response
        else:
            print('request failed')
            print('Response status: %d' % response.status_code)
            print('Method: put_request')
            print('request response: \n %s' % response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


def get_request(url, headers):
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if re.match('20[0-4]', str(response.status_code)):
            return response
        else:
            print('request failed')
            print('Response status: %d' % response.status_code)
            print('Method: get_request')
            print('request response: \n %s' % response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


def delete_request(url, headers):
    try:
        print("deleting")
        response = requests.request("DELETE", url, headers=headers, verify=False)
        if re.match('20[0-4]', str(response.status_code)):
            return response
        else:
            print('request failed')
            print('Response status: %d' % response.status_code)
            print('Method: delete_request')
            print('request response: \n %s' % response.text)
            exit()
    except Exception as err:
        print(err)
        exit()