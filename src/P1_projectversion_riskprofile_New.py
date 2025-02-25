import argparse
from sys import exit
from re import match
from os import environ
from requests import request, sessions
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


environ['NO_PROXY'] = 'blackduckweb.philips.com'
environ['NO_PROXY'] = '8.8.8.8/'

# server_url = 'https://8.8.8.8/'
server_url = 'https://blackduckweb.philips.com/'
# api_token =

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
            print(url)
            if post_response.status_code == 412:
                return post_response
            exit()
    except Exception as err:
        print(err)
        exit()


def get_projectID(project_name, headers):
    if " " in project_name:
        project_name.replace(" ","%20")
    project_url = f"{server_url}/api/projects?q=name%3A{project_name}"
    response = request("GET", url=project_url, headers=headers, verify=False)
    if response.status_code != 200:     # or response.json()['totalCount'] == 0:
        print(response.json())
        print(response.json()['totalCount'])
        print("Project does not exist")
        exit()
    projectID = response.json()["items"][0]["_meta"]["href"]
    projectID = projectID.split("/")[-1]
    return projectID


def get_versionID(project, version, headers):
    projectID = get_projectID(project, headers)
    if " " in version:
        version.replace(" ", "%20")
    version_url = f"{server_url}/api/projects/{projectID}/versions?q=versionName%3A{version}"
    response = request("GET", url=version_url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Version does not exist")
        exit()
    versionID = response.json()["items"][0]["_meta"]["href"]
    versionID = versionID.split("/")[-1]
    return projectID, versionID


def main(project_name, version_name, api_token):
    login_headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Authorization': f'token {api_token}'
    }
    login_url = server_url + '/api/tokens/authenticate'
    login_response = post_request(url=login_url, payload={}, headers=login_headers)
    get_header = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json",
        'X-CSRF-TOKEN': login_response.headers['X-CSRF-TOKEN'],
        'Authorization': 'bearer {}'.format(login_response.json()['bearerToken'])
    }
    id1, id2 = get_versionID(project_name, version_name, get_header)
    risk_url = f"{server_url}/api/projects/{id1}/versions/{id2}/risk-profile"
    response = request("GET", url=risk_url, headers=get_header, verify=False)
    if response.status_code != 200:
        print("Could not get risk report")
        exit()
    print(response.json()["categories"])


def parse_arguments():
    parser = argparse.ArgumentParser(usage='python P1_projectversion_riskprofile_New.py -p projectName -v versionName -t api_token',
                                     description='Get the risk profile info of a project version',
                                     epilog="python P1_projectversion_riskprofile_New.py -p projectName -v versionName -t api_token")
    parser.add_argument('-p', '--project_name', type=str, help='Enter the project name')
    parser.add_argument('-v', '--version_name', type=str,  help='Enter the version name')
    parser.add_argument('-t', '--password', type=str, help='Enter the api_token')
    args = parser.parse_args()
    if not args.project_name or not args.version_name:
        parser.error("python %(prog)s -h \nUse the above command to know the usage")
        exit()

    return args.username, args.password, args.project_name, args.version_name


if __name__ == '__main__':
    main(project_name="test_project_3", version_name="Jenkins_Test", api_token="YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng==")
