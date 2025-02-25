import json
from sys import exit
from re import match
from requests import request, sessions
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from icecream import ic
from os import environ, makedirs, path
import time
import timeit
urllib3.disable_warnings(InsecureRequestWarning)


environ['NO_PROXY'] = 'blackduckweb.philips.com'
environ['NO_PROXY'] = 'ENTER_SERVER_URL'
environ['NO_PROXY'] = '8.8.8.8'


ic.disable()
# server_url = 'https://8.8.8.8/'
# api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here
server_url = 'https://blackduckweb.philips.com/'
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=="  # Enter api token here

if server_url[-1] == "/":
    server_url = server_url[:-1]


def get_request_headers():
    get_header = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json",
        'X-CSRF-TOKEN': csrf_token,
        'Authorization': 'bearer {}'.format(auth_token)
    }
    return get_header


def get_report_list_headers():
    host_url = server_url.split("/")[-1]
    get_report_list_header = {
        # 'Content-Type': "application/json",
        'Host': f'{host_url}',
        'Accept': "application/vnd.blackducksoftware.internal-1+json, application/json, */*;q=0.8",
        'Accept-Encoding': "gzip, deflate",
        'Authorization': 'bearer {}'.format(auth_token)
    }
    return get_report_list_header


def post_report_headers():
    report_create_headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'X-CSRF-TOKEN': csrf_token,
        'Authorization': 'bearer {}'.format(auth_token),
    }
    return report_create_headers


def download_headers():
    download_headers = {
        'Content-Type': "application/zip",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Authorization': 'bearer {}'.format(auth_token),
    }
    return download_headers


def delete_request_headers():
    delete_headers = {
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'Accept-Encoding': "gzip, deflate",
        'X-Requested-With': "XMLHttpRequest",
        'X-CSRF-TOKEN': csrf_token,
        'Authorization': 'bearer {}'.format(auth_token),
    }
    return delete_headers


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


def delete_request(url, headers):
    try:
        print("deleting")
        delete_request_response = request("DELETE", url, headers=headers, verify=False)
        if match('20[0-4]', str(delete_request_response.status_code)):
            return delete_request_response
        else:
            print('request failed')
            print('Response status: %d' % delete_request_response.status_code)
            print('Method: delete_request')
            print('request response: \n %s' % delete_request_response.text)
            exit()
    except Exception as err:
        print(err)
        exit()


## Generate report
def generate_report(lv_version_id):
    reports_url = f"{server_url}/api/versions/{lv_version_id}/reports"
    payload = json.dumps({
        "categories": ["VERSION", "CODE_LOCATIONS", "COMPONENTS", "SECURITY", "FILES"],
        "versionId": f"{lv_version_id}",
        "reportType": "VERSION",
        "reportFormat": "CSV"
    })
    reports_response = post_request(url=reports_url, payload=payload, headers=post_report_headers())
    return reports_response.status_code


## Download the report
def download_report(lv_report_id, lv_file_name):
    if path.exists(lv_file_name):
        print(f"file already exit: {lv_file_name}")
    elif lv_report_id != "":
        report_download_url = f"{server_url}/api/reports/{lv_report_id}"
        download_response = get_request(url=report_download_url, headers=download_headers())
        lv_file_name = f"{lv_file_name}.zip"
        open(lv_file_name, 'wb').write(download_response.content)
    else:
        print("blank Report ID")


def remove_special_chars(ips):  # ips -> input string
    special_characters = ['*', '\\', '|', ':', '<', '>', '?', '/']  # '!', '@', '#', '$', '%', '^', '&', '(', ')',
    for i in ips:
        if i in special_characters:
            ips = ips.replace(i, "_")
    return ips


start = timeit.default_timer()
csrf_token = ''
auth_token = ''
login_headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Authorization': f'token {api_token}'
}
login_url = server_url + '/api/tokens/authenticate'
login_response = post_request(url=login_url, payload={}, headers=login_headers)
auth_token = login_response.json()['bearerToken']
csrf_token = login_response.headers['X-CSRF-TOKEN']


iteration = 0
while True:
    # ToDo:  Generate reports
    # projects_url = server_url + "/api/projects?limit=999"  # offset=6&limit=1"
    projects_url = server_url + "/api/projects?q=name%3ASCOE_Test_ChinaOP"  # offset=6&limit=1"
    project_request_response = get_request(url=projects_url, headers=get_request_headers())
    for each_project_request_response_items in project_request_response.json()["items"]:
        project_name = each_project_request_response_items["name"]
        # if project_name != "Coffee_Xelsis2_UI":
        #     # pass
        #     continue
        version_url = each_project_request_response_items["_meta"]["href"] + "/versions?limit=999"
        version_request_response = get_request(url=version_url, headers=get_request_headers())
        for each_version_request_response_items in version_request_response.json()["items"]:
            iteration += 1
            if iteration % 500 == 0:
                login_response = post_request(url=login_url, payload={}, headers=login_headers)
                auth_token = login_response.json()['bearerToken']
                csrf_token = login_response.headers['X-CSRF-TOKEN']
                iteration += 1
            version_name = each_version_request_response_items["versionName"]
            each_version_url = each_version_request_response_items["_meta"]["href"]
            version_id = each_version_url.split("/")[-1]
            print("report will be generated here")
            status = generate_report(version_id)
            if status == 201:
                print(f"{project_name}|{version_name}|Report creation triggered")
    time.sleep(300)
    print("#########################################################")
    # ToDo:  download reports
    for each_project_request_response_items in project_request_response.json()["items"]:
        project_name = each_project_request_response_items["name"]
        version_url = each_project_request_response_items["_meta"]["href"] + "/versions?limit=999"
        version_request_response = get_request(url=version_url, headers=get_request_headers())
        for each_version_request_response_items in version_request_response.json()["items"]:
            version_name = each_version_request_response_items["versionName"]
            each_version_url = each_version_request_response_items["_meta"]["href"]
            version_id = each_version_url.split("/")[-1]
            reports_list_url = f"{each_version_url}/reports?limit=100"
            # print(reports_list_url)
            # print(get_report_list_headers())
            reports_list_request_response = get_request(url=reports_list_url, headers=get_report_list_headers())
            for reports_list_request_response_items in reports_list_request_response.json()["items"]:
                iteration += 1
                if iteration % 500 == 0:
                    login_response = post_request(url=login_url, payload={}, headers=login_headers)
                    auth_token = login_response.json()['bearerToken']
                    csrf_token = login_response.headers['X-CSRF-TOKEN']
                    iteration += 1
                # if project_name != "Coffee_Xelsis2_UI":
                #     # pass
                #     continue
                if reports_list_request_response_items["createdBy"]["userName"] == "ENTER_EMAILID":
                    if reports_list_request_response_items["status"] == "COMPLETED":
                        if reports_list_request_response.json()["totalCount"] == 1:
                            report_id = reports_list_request_response_items["_meta"]["href"].split("/")[-1]
                        elif reports_list_request_response.json()["totalCount"] == 0:
                            print(f"{project_name}|{version_name}|No report to show")
                            report_id = ""
                        else:
                            # ToDO: more than 1 reports - compare updatedAt date and pick the latest
                            report_id = reports_list_request_response_items["_meta"]["href"].split("/")[-1]
                            pass
                        new_project_name = remove_special_chars(project_name)
                        new_version_name = remove_special_chars(version_name)
                        file_name = f"{new_project_name}__{new_version_name}"
                        if not path.exists(f"C:/temp/BD_Reports/{new_project_name}"):
                            makedirs(f"C:/temp/BD_Reports/{new_project_name}")
                        updated_file_name = path.join(f"C:/temp/BD_Reports/{new_project_name}", file_name)
                        download_report(report_id, updated_file_name)
                        delete_report_url = f"{server_url}/api/versions/{version_id}/reports/{report_id}"
                        delete_request(url=delete_report_url, headers=delete_request_headers())
                        break
                    else:
                        print(f"{project_name}|{version_name}|{reports_list_request_response_items['status']}")
    break
# DELETE /api/versions/9920ecdb-4e57-4e6c-a491-1a69806a7ce2/reports/3ffcd56c-482d-4fe1-8f5f-1b3ad037f18a
stop = timeit.default_timer()
print(stop - start)
