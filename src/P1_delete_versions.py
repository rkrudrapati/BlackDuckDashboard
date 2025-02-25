'''
This script delete the versions mentioned in the input file
Required input: project name -> to be entered in P1_gv_variables -> key_project_name

'''


from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers
from src.P1_my_requests import get_request
import src.P1_blackduck_utils as bd_utils
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "/api/projects?q=name%3A" + "%s" %(variables.key_project_name)
# url = "https://blackduckweb.philips.com/api/projects?q=name%3ARadiology_Solutions_PMT"

project_response = get_request(url=url, headers=get_headers)
all_project_items = bd_utils.items_in_response(response=project_response)
data_list = []
with open('input', 'r') as delete_list:
    for lines in delete_list.readlines():
        data_list.append(lines.strip())
    print(data_list)
    delete_list.close()

for items in all_project_items:
    project_link = bd_utils.get_project_link(items)
    project_name = bd_utils.get_project_name(items)
    project_id = project_link.split('/')[-1]
    if project_name == variables.key_project_name:
        print("Deleting mentioned version in project: %s" % project_name)
        versions_link = bd_utils.construct_all_version_link(items)
        versions_response = get_request(url=versions_link, headers=get_headers)
        count = versions_response.json()['totalCount']
        all_version_items = bd_utils.items_in_response(response=versions_response)
        for v_items in all_version_items:
            version_name = v_items['versionName']
            if version_name in data_list:
                version_link = v_items["_meta"]["href"]
                print(version_name)
                version_id = version_link.split('/')[-1]
                # bd_utils.delete_version_new(version_id)
                bd_utils.delete_version(project_id, version_id)
