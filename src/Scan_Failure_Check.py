import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import argparse
import sys
from time import sleep


class TestFailed(BaseException):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message


portal = 'https://blackduckweb.philips.com'
headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/javascript, */*; q=0.01",
}


def login(username, password):
    login_url = portal + '/j_spring_security_check'
    payload = 'j_username={}&j_password={}'.format(username, password)
    response = requests.request("POST", url=login_url, data=payload, headers=headers, verify=False)
    if response.status_code != 204:
        try:
            raise TestFailed("Login failed, please provide proper credentials")
        except TestFailed as x:
            print(x)
        sys.exit()
    token = response.headers['Set-Cookie']
    headers.update({'cookie': token})


def scan_failures():
    # scans_url = "{}/api/codelocations?sort=updatedAt%20DESC&offset=0&limit=100&filter=codeLocationStatus%3Ain_progress&filter=codeLocationStatus%3Aerror".format(portal)
    scans_url = "https://blackduckweb.philips.com/api/codelocations?sort=updatedAt%20DESC&offset=0&limit=100&filter=codeLocationStatus%3Aerror&filter=codeLocationStatus%3Ain_progress"
    response = requests.request("GET", url=scans_url, headers=headers, verify=False)
    print(response.json())
    print(response.text)

login("testuser1", "blackduck")
scan_failures()