from src.P1_login import login_to_bd_server
from src.P1_gv_variables import server_url, username, password, data
from src.P1_my_requests import post_request
from src.P1_headers import post_request_headers
import json

login_to_bd_server(url=server_url, username=username, password=password)

create_project_url = server_url + '/api/projects'
# data = {
#   "name": "test_project2",
#   "versionName": "test"
#   }

for i in range(3, 76): # 3 to 75
    project = 'test_project_' + str(i)
    data = {
        "name": project,
        "versionName": "test"
    }
    post_request(url=create_project_url, payload=json.dumps(data), headers=post_request_headers())
    print(data)
