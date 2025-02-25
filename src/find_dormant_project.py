#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.


try:
    from .P1_headers import get_request_headers
    from .P1_my_requests import get_request
    from .P1_login import login_to_bd_server
except:
    from headers import get_request_headers
    from my_requests import get_request
    from login import login_to_bd_server


portal = 'https://8.8.8.8'
login_to_bd_server(url=portal, username='ENTER_USERNAME', password='ENTER_PASSWORD')

# projects_url = 'https://blackduckweb.philips.com/api/projects?limit=999'
projects_url = 'https://blackduckweb.philips.com/api/projects'
headers = get_request_headers()
response = get_request(url=projects_url, headers=headers)
print(response.status_code)