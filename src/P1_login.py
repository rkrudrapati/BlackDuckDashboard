#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.


from src.P1_my_requests import post_request
# from src.P1_headers import get_login_headers
# import src.P1_headers as headers
from src.P1_api_headers import get_login_headers
import src.P1_api_headers as headers
from src.P1_gv_variables import server_url
import json
from icecream import ic


ic.disable()
def update_token_in_base_header(bearer_token):
    headers.bearer_token = bearer_token


def update_csrf_token_value(csrf_token):
    headers.csrf_token = csrf_token


def login_to_bd_server(url=server_url, username="", password=""):
    payload = {"j_username": username, "j_password": password}
    login_url = url + '/j_spring_security_check'
    login_headers = get_login_headers()
    response = post_request(url=login_url, payload=payload, headers=login_headers)
    lv_token = response.headers['Set-Cookie']
    update_token_in_base_header(lv_token)
    lv_csrf_token = response.headers['X-CSRF-TOKEN']
    update_csrf_token_value(lv_csrf_token)
    ic("Token: {}".format(lv_token))
    ic("CSRF Token: {}".format(lv_csrf_token))


def login_to_bd_server_via_token(url=server_url):
    payload = {}
    login_url = url + '/api/tokens/authenticate'
    login_headers = get_login_headers()
    response = post_request(url=login_url, payload=payload, headers=login_headers)
    lv_csrf_token = response.headers['X-CSRF-TOKEN']
    update_csrf_token_value(lv_csrf_token)
    try:
        bearer_token = json.loads(response.content.decode('utf-8'))['bearerToken']
    except json.decoder.JSONDecodeError as e:
        raise Exception("Failed to obtain bearer token, check for valid authentication token")
    update_token_in_base_header(bearer_token)
    ic("Token: {}".format(bearer_token))
    ic("CSRF Token: {}".format(lv_csrf_token))


# from os import environ
# environ['NO_PROXY'] = 'blackduckweb.philips.com'
#

# server_url = variables.server_url
# login_to_bd_server(url=server_url, username=variables.username, password=variables.password)
# login_to_bd_server_via_token(url=server_url, authn_token=variables.api_token)

