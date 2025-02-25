import requests
import csv
from sys import exit
from re import match
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from os import environ
environ['NO_PROXY'] = 'blackduckweb.philips.com'


#################


def post_request(url, payload, headers):
    try:
        post_response = requests.request("POST", url=url, data=payload, headers=headers, verify=False)
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


class Generate_CVSS_Report:
    def __init__(self, api_token, project_name, version_name):
        self.api_token = api_token
        self.project_name = project_name
        self.version_name = version_name
        self.auth_token = ""
        self.csrf_token = ""
        self.get_headers = {}
        self.portal = "https://blackduckweb.philips.com"
        self.project_id = ""
        self.version_id = ""

    def login(self):
        login_url = self.portal + '/api/tokens/authenticate'
        login_headers = {
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Authorization': 'token {}'.format(self.api_token),
        }
        response = requests.request("POST", url=login_url, data={}, headers=login_headers, verify=False)
        if not match('20[0-4]', str(response.status_code)):
            print('request failed')
            print('Response status: %d' % response.status_code)
            print('Method: post_request')
            print('request response: \n %s' % response.text)
            exit()
        auth_token = response.json()['bearerToken']
        csrf_token = response.headers['X-CSRF-TOKEN']
        self.get_headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'X-Requested-With': "XMLHttpRequest",
            'Accept': "application/json",
            'X-CSRF-TOKEN': csrf_token,
            'authorization': 'bearer {}'.format(auth_token)
        }

    def get_project_id(self):
        project_name = self.project_name
        if " " in self.project_name:
            project_name.replace(" ", "%20")
        project_url = f"{self.portal}/api/projects?limit=300&q=name%3A{project_name}"
        response = requests.request("GET", url=project_url, headers=self.get_headers, verify=False)
        if not match('20[0-4]', str(response.status_code)):  # or response.json()['totalCount'] == 0:
            print("Project does not exist")
            exit()
        project_id_href = response.json()["items"][0]["_meta"]["href"]
        self.project_id = project_id_href.split("/")[-1]

    def get_version_id(self):
        url = f"{self.portal}/api/projects/{self.project_id}/versions?q=versionName%3A{self.version_name}"
        version_response = requests.request("GET", url=url, headers=self.get_headers, verify=False)
        if not match('20[0-4]', str(version_response.status_code)):  # or response.json()['totalCount'] == 0:
            print("Version does not exist")
            exit()
        for version_items in version_response.json()['items']:
            name = version_items['versionName']
            if name == self.version_name:
                version_url = version_items["_meta"]["href"]
                self.version_id = version_url.split("/")[-1]
                break
        if self.version_id == '':
            print("Version does not exist")
            exit()

    def vulnerabilities(self):
        vuln_url = f"{self.portal}/api/projects/{self.project_id}/versions/{self.version_id}/vulnerability-bom?limit=5000"
        print(vuln_url)
        print("$$$$$$$$$$$$$$$")
        # print(self.get_headers)
        # print("$$$$$$$$$$$$$$$")
        response = requests.request("GET", url=vuln_url, headers=self.get_headers, verify=False)
        print(response.json())
        print("$$$$$$$$$$$$$$$")
        file = self.project_name + "_" + self.version_name + ".csv"
        with open(file, 'w', newline='') as file:
            fieldnames = ['Component_Name', 'Version', 'CVE_ID', 'Source', 'Remidiation_Status', 'CVSSV2_SCORE',
                          'CVSSV2_Severity', 'CVSSV3_SCORE', 'CVSSV3_Severity']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for each_item in response.json()["items"]:
                Name = each_item["componentName"]
                Version = each_item["componentVersionName"]
                Origin = each_item["componentVersionOrigin"]
                Origin = Origin.split("https://blackduckweb.philips.com/api/")[-1]
                vuln_url = self.version_id + "/" + Origin + "/vulnerabilities"
                res = requests.request("GET", url=vuln_url + "?limit=1000", headers=self.get_headers, verify=False)
                # vuln_count = res.json()["totalCount"]
                for items in res.json()["items"]:
                    cve = items["id"]
                    Source = items["source"]
                    rem_status = items["remediationStatus"]
                    cvss2_score = items["cvss2"]["baseScore"]
                    cvss2_severity = items["cvss2"]["severity"]
                    try:
                        cvss3_score = items["cvss3"]["baseScore"]
                        cvss3_severity = items["cvss3"]["severity"]
                    except:
                        cvss3_score = "NA"
                        cvss3_severity = "NA"
                    if rem_status == "NEW":
                        writer.writerow(
                            {'Component_Name': Name, 'Version': Version, 'CVE_ID': cve, 'Source': Source,
                             'Remidiation_Status': rem_status,
                             'CVSSV2_SCORE': cvss2_score, 'CVSSV2_Severity': cvss2_severity,
                             'CVSSV3_SCORE': cvss3_score, 'CVSSV3_Severity': cvss3_severity})

##### for single project. Comment the above code and uncomment the below one
lv_api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="
bd_repoter = Generate_CVSS_Report(api_token=lv_api_token, project_name="test_project",
                                  version_name="Sahar_Test_change_order_no_bom_agg")
bd_repoter.login()
bd_repoter.get_project_id()
bd_repoter.get_version_id()
bd_repoter.vulnerabilities()

##### for single project. Comment the above code and uncomment the below one
project_name = "HSDP_Clinical_DnI"
version_name = "LogSubsystem_19.7"

vuln(project_name, version_name)
