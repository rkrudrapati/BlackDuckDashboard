"""
P1_dormant_projects is the base.
This script will identify the latest or last scanned date of a project.
The script will verify the code locations and their respective scan time
Based on this, it will give the last scanned date of a project
If any version has no or zero code locations, then it will be presumed as empty version and therefore deleted.
"""

from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers, delete_request_headers
from src.P1_my_requests import get_request, delete_request
import src.P1_blackduck_utils as bd_utils
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "/api/projects?limit=999"
response = get_request(url=url, headers=get_headers)
project_items = bd_utils.items_in_response(response=response)
# project_items = response.json()["items"]

versions_count = 0
deleted_versions_count = 0
for items in project_items:
    output = []
    project_link = bd_utils.get_project_link(items)
    project_name = bd_utils.get_project_name(items)
    project_id = project_link.split('/')[-1]
    # if project_name != variables.key_project_name:
    #     continue
    # print("break here")
    """Enabled this block of code if you want to list out all the project names"""
    # print(project_name)
    # continue
    """Enabled this block of code if you want to list out all the project names"""
    output.append(project_name)
    if project_id != '':
        versions_link = bd_utils.construct_all_version_link(items)
        version_response = get_request(url=versions_link, headers=get_headers)
        # count = version_response.json()['totalCount']

        version_items = bd_utils.items_in_response(response=version_response)
        # version_items = version_response.json()["items"]
        ref_date = variables.ref_date
        # print(version_items)
        latest_version_name = ""
        final_count = 0
        for v_items in version_items:
            version_name = v_items['versionName']
            createdAt = v_items['createdAt'].split('T')[0]  # date
            each_version_link = v_items["_meta"]["href"]
            # codelocationlink = bd_utils.get_codelocation_link()
            codelocationlink = each_version_link + "/codelocations"
            # print(versions_link, version_name)
            codelocation_response = get_request(url=codelocationlink, headers=get_headers)
            count = codelocation_response.json()["totalCount"]
            if count == 0:
                print("deleting the following:")
                print(project_name, version_name)
                print(each_version_link)
                print(count)
                delete_headers = delete_request_headers()
                response = delete_request(url=each_version_link, headers=delete_headers)
                print(response)
                print("deleted")
            else:
               pass