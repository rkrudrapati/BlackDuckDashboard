from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers
from src.P1_my_requests import get_request
import src.P1_blackduck_utils as bd_utils
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "/api/risk-profile-dashboard?limit=25"
response = get_request(url=url, headers=get_headers)
print(response.status_code)
print(response.json())
# print(response.text)
project_items = bd_utils.items_in_response(response=response)
# project_items = response.json()["items"]
print(project_items)
