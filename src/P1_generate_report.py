from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers, post_request_headers
from src.P1_my_requests import get_request, post_request
import src.P1_blackduck_utils as bd_utils
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "api/projects?q=name%3A" + "%s" %(variables.key_project_name)

project_response = get_request(url=url, headers=get_headers)
all_project_items = bd_utils.items_in_response(response=project_response)

for items in all_project_items:
    project_link = bd_utils.get_project_link(items)
    project_name = bd_utils.get_project_name(items)
    project_id = project_link.split('/')[-1]
    if project_name == variables.key_project_name:
        versions_link = bd_utils.link_to_select_version(items,variables.key_version_name)
        versions_response = get_request(url=versions_link, headers=get_headers)
        count = versions_response.json()['totalCount']
        if count != 1:
            print("Msg1: Wrong version name entered")
            break
        all_version_items = bd_utils.items_in_response(response=versions_response)
        for v_items in all_version_items:
            version_name = v_items['versionName']
            if version_name != variables.key_version_name:
                print("Msg2: Wrong version name entered")
                break
            version_report_link = bd_utils.identify_href_link(v_items, 'versionReport')
            version_id = v_items["_meta"]["href"].split('/')[-1]
            report_payload = bd_utils.get_report_payload(version_id)
            report_create_headers = post_request(url=version_report_link, payload=report_payload, headers=post_request_headers())
