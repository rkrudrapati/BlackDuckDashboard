"""
This script will copy the comments from csv file and add them to a particular project version.
Required fields:
    Project Name    ->  Taken from P1_gv_variables
    Project Version Name    ->  Taken from P1_gv_variables
    Report in CSV format    ->  Generated in BD hub and extracted to local

The script will automatically detect the index of 'Component id' , 'Version id' and  'Comments'
Comments sections need to be added in the file. It does not come by default.
Using these details, the script will frame the required URL to post comment.
Comment is the data or payload here.

Todo:
    1. Script should be improved to use the user token instead of using the admin credentials
    2. Check for duplicate comments and try not to repeat them.
"""

from src.P1_login import login_to_bd_server
from src.P1_headers import get_request_headers, post_request_headers
from src.P1_my_requests import get_request, post_request
import src.P1_blackduck_utils as bd_utils
import src.P1_gv_variables as variables
import csv
import json

server_url = variables.server_url
login_to_bd_server(url=server_url, username=variables.username, password=variables.password)

get_headers = get_request_headers()
url = server_url + "/api/projects?q=name%3A" + "%s" %(variables.key_project_name)
response = get_request(url=url, headers=get_headers)
project_items = bd_utils.items_in_response(response=response)

project_id = ""
version_id = ""
component_id = ""
component_version_id = ""
components_file = r"C:\Users\code1\Desktop\_temp\Test_Project1-1.0_2020-09-14_155145\components_2020-09-14_155145.csv"


for items in project_items:
    project_link = bd_utils.get_project_link(items)
    project_name = bd_utils.get_project_name(items)
    project_id = project_link.split('/')[-1]
    if project_name == variables.key_project_name:
        print("Adding the comments in project: %s" % project_name)
        versions_link = project_link + "/versions?q=versionName%3A" + "%s" %(variables.key_version_name)
        versions_response = get_request(url=versions_link, headers=get_headers)
        version_items = bd_utils.items_in_response(response=versions_response)
        for v_items in version_items:
            version_name = v_items['versionName']
            version_link = v_items["_meta"]["href"]
            version_id = version_link.split('/')[-1]
            print("Adding the comments in project version: %s" % version_name)


with open(components_file, 'r') as components_file_data:
    initial = True
    read_csv = csv.reader(components_file_data, delimiter=',')
    try:
        for _realine in read_csv:
            if initial == True:
                component_id_index = _realine.index('Component id')
                component_version_id_index = _realine.index('Version id')
                comment_index = _realine.index('Comments')
                initial = False
            else:
                component_id = _realine[component_id_index]
                component_version_id = _realine[component_version_id_index]
                comment = _realine[comment_index]
                post_data = json.dumps({"comment": comment})
                if comment != "":
                    comments_url = server_url + "/api/projects/{}/versions/{}/components/{}/component-versions/{}/comments".format(project_id, version_id, component_id, component_version_id)
                    comment_response = post_request(url=comments_url, payload=post_data, headers=post_request_headers())
                    # print(comment_response)
    except Exception as err:
        print(err)
        components_file_data.close()


components_file_data.close()