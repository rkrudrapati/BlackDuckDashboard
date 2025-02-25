from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers, delete_request_headers
from src.P1_my_requests import get_request, delete_request
import src.P1_blackduck_utils as bd_utils
# from src.blackduck_utils import identify_href_link, delete_version
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "/api/projects?limit=999"
# url = "https://blackduckweb.philips.com/api/projects?q=name%3ADI_DINxGen_UserWorkflow"

response = get_request(url=url, headers=get_headers)
project_items = bd_utils.items_in_response(response=response)
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
        response1 = get_request(url=versions_link, headers=get_headers)
        count = response1.json()['totalCount']

        version_items = bd_utils.items_in_response(response=response1)
        ref_date = variables.ref_date
        # print(version_items)
        latest_version_name = ""
        for v_items in version_items:
            version_name = v_items['versionName']
            createdAt = v_items['createdAt'].split('T')[0]
            version_link = v_items["_meta"]["href"]
            ## print(version_items)
            # print(version_name)
            # print(createdAt)
            if ref_date < createdAt:
                ref_date = createdAt
                latest_version_name = version_name
        output.append(latest_version_name)
        output.append(count)
        output.append(ref_date)
        print(output)