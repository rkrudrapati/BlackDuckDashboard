#  Copyright (c) 2020. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.


from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers, delete_request_headers
from src.P1_my_requests import get_request, delete_request
import src.P1_gv_variables as variables


server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)


def get_project_link(project_name):
    project_url = server_url + "/api/projects?q=name%3A{}".format(project_name)
    response = get_request(url=project_url, headers=get_request_headers())
    if response.json()["totalCount"] != 0:
        # print(response.json())
        # print(response.text)
        return response.json()["items"][0]["_meta"]["href"]


def get_user_ids(project_users_link, username):
    response = get_request(url=project_users_link, headers=get_request_headers())
    users_id_list = []
    user_name = []
    if response.json()["totalCount"] != 0:
        if username == "All":
            for items in  response.json()["items"]:
                if items["name"] != "ENTER_EMAILID" and items["name"] != "sysadmin":
                    user_name.append(items["name"])
                    users_id_list.append(items["_meta"]["href"])
        else:
            for items in  response.json()["items"]:
                if items["name"] == username:
                    user_name.append(items["name"])
                    users_id_list.append(items["_meta"]["href"])
    return [user_name, users_id_list]


def delete_all_users(project_name, username):
    link = get_project_link(project_name)
    # print(link)
    project_users_link = link + "/users"
    user_name, users_id_list = get_user_ids(project_users_link, username)
    for (each_user_name, each_user_id) in zip(user_name, users_id_list):
        print("deleting username: {}".format(each_user_name))
        delete_request(url=each_user_id,headers=delete_request_headers())



# delete_all_users(project_name="", username="All")
delete_all_users(project_name="HSDP_BDPLite", username="All")