"""
P1_dormant_projects is the base.
This script will identify the latest or last scanned date of a project.
The script will verify the code locations and their respective scan time
Based on this, it will give the last scanned date of a project
"""

from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers
from src.P1_my_requests import get_request
import src.P1_blackduck_utils as bd_utils
import src.P1_gv_variables as variables


server_url = variables.server_url
# login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "/api/projects?limit=999"
response = get_request(url=url, headers=get_headers)
project_items = bd_utils.items_in_response(response=response)
# project_items = response.json()["items"]

versions_count = 0
for items in project_items:
    output = []
    project_link = bd_utils.get_project_link(items)
    project_name = bd_utils.get_project_name(items)
    project_id = project_link.split('/')[-1]
    # if project_name != variables.key_project_name:
    #     continue
    # print("break here")
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
            # print(v_items)
            # print(type(v_items))
            versions_count += 1
            version_name = v_items['versionName']
            createdAt = v_items['createdAt'].split('T')[0]  # date
            each_version_link = v_items["_meta"]["href"]
            # codelocationlink = bd_utils.get_codelocation_link()
            codelocationlink = each_version_link + "/codelocations"
            codelocation_response = get_request(url=codelocationlink, headers=get_headers)
            # print(codelocation_response.json())
            count = codelocation_response.json()["totalCount"]
            if count == 0:
                continue
            else:
                updatedAt = codelocation_response.json()["items"][0]["updatedAt"].split('T')[0]
            componentslink = each_version_link + "/components"
            components_response = get_request(url=componentslink, headers=get_headers)
            # print(components_response.json())
            # count = components_response.json()["totalCount"]
            # sys.exit()
            ## print(version_items)
            # print(version_name)
            # print(createdAt)
            if ref_date < updatedAt:
                ref_date = updatedAt
                latest_version_name = version_name
                final_count = count
        output.append(latest_version_name)
        output.append(final_count)
        output.append(ref_date)
        print(output)
