import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import argparse
import sys

# portal = 'https://blackduckweb.philips.com'
portal = 'https://8.8.8.8'
headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/javascript, */*; q=0.01",
}

def login(username, password):
    login_url = portal + '/j_spring_security_check'
    payload = 'j_username={}&j_password={}'.format(username, password)
    # print(login_url, payload, headers)
    response = requests.request("POST", url=login_url, data=payload, headers=headers, verify=False)
    if response.status_code != 204:
        print("Login failed, please provide proper credentials")
        sys.exit()
    token = response.headers['Set-Cookie']
    headers.update({'cookie': token})


def get_projectID(name):
    if " " in name:
        name.replace(" ","%20")
    project_url = portal +"/api/projects?q=name%3A" + name
    response = requests.request("GET", url=project_url, headers=headers, verify=False)
    if response.status_code != 200:# or response.json()['totalCount'] == 0:
        print(response.json())
        print(response.json()['totalCount'])
        print("Project does not exist")
        sys.exit()
    projectID = response.json()["items"][0]["_meta"]["href"]
    projectID = projectID.split("/")[-1]
    return projectID


def get_versionID(project, version):
    projectID = get_projectID(project)
    if " " in version:
        version.replace(" ","%20")
    version_url = portal +"/api/projects/{}/versions?q=versionName%3A".format(projectID) + version
    response = requests.request("GET", url=version_url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Version does not exist")
        sys.exit()
    versionID = response.json()["items"][0]["_meta"]["href"]
    versionID = versionID.split("/")[-1]
    return projectID, versionID


def main(username, password, project_name, version_name):
    login(username, password)
    id1, id2 = get_versionID(project_name, version_name)
    risk_url = portal+ "/api/projects/{}/versions/{}/risk-profile".format(id1, id2)
    response = requests.request("GET", url=risk_url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Could not get risk report")
        sys.exit()
    print(response.json()["categories"])


def parse_arguments():
    parser = argparse.ArgumentParser(usage='python P1_projectversion_riskprofile.py -u username -p password -e projectName -f versionName',
                                     description='Get the risk profile info of a project version',
                                     epilog="python P1_projectversion_riskprofile.py -u username -p password -e projectName -f versionName")
    parser.add_argument('-u', '--username', type=str, help='Enter the username')
    parser.add_argument('-p', '--password', type=str, help='Enter the password')
    parser.add_argument('-e', '--project_name', type=str, help='Enter the project name')
    parser.add_argument('-f', '--version_name', type=str,  help='Enter the version name')
    args = parser.parse_args()

    if not args.project_name or not args.version_name:
        parser.error("python %(prog)s -h \nUse the above command to know the usage")
        sys.exit()

    return args.username, args.password, args.project_name, args.version_name


if __name__ == '__main__':
    # main(*parse_arguments())
    main(username="ENTER_EMAILID", password="ENTER_PASSWORD", project_name="test_project", version_name="synergy_test")
