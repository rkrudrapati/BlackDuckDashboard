from src.P1_login import login_to_bd_server
from src.P1_gv_variables import server_url, username, password, data
from src.P1_my_requests import get_request
from src.P1_headers import get_request_headers
import src.P1_blackduck_utils as bd_utils


login_to_bd_server(url=server_url, username=username, password=password)

projects_url = server_url + "/api/projects?limit=999"
projects_raw_json = get_request(projects_url, headers=get_request_headers())

project_items = bd_utils.items_in_response(response=projects_raw_json)
for items in project_items:
    output = []
    project_link = bd_utils.get_project_link(items)
    project_name = bd_utils.get_project_name(items)
    project_id = project_link.split('/')[-1]
    output.append(project_name)
    level_data_url = server_url + "/api/projects/{}/custom-fields/1".format(project_id)
    level_raw_data = get_request(level_data_url, headers=get_request_headers())
    try:
        level = level_raw_data.json()['values'][0].split("/")[-1]
        if level == '1':
            output.append(1)
            output.append(0)
            output.append(0)
        elif level == '2':
            output.append(0)
            output.append(1)
            output.append(0)
        elif level == '3':
            output.append(0)
            output.append(0)
            output.append(1)
    except Exception:
        output.append('NA')
    print(output)