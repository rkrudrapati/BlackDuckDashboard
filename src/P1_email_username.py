from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers
from src.P1_my_requests import get_request
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, ENTER_EMAILIDvariables.password)

get_headers = get_request_headers()

url = server_url + '/api/users?limit=9999'
response = get_request(url, headers=get_headers)
for items in response.json()['items']:
    print(items['email'])
