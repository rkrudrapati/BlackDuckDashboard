#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
from src.P1_utils import sanctify_url

prod = True

if prod:
    server_url = 'https://blackduckweb.philips.com/'
    server_url = sanctify_url(server_url)
    # username = ''
    # password = ''
    api_token = 'YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=='
elif not prod:
    # server_url = 'https://ENTER_SERVER_URL/'
    server_url = 'https://8.8.8.8/'
    server_url = sanctify_url(server_url)
    username = 'ENTER_EMAILID'
    password = ''
    api_token = 'YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng=='

ref_date = '2017-01-01'
key_project_name = 'Test_Project'
key_version_name = 'demo'

report_payload ={
    'categories': ["VERSION", "CODE_LOCATIONS", "COMPONENTS", "SECURITY", "FILES"],
    'reportFormat': "CSV",
    'reportType': "VERSION",
    # 'reportUrl': "string",
    # 'url': "string",
    'versionId': "",
}


data ={}
# data = {
# "ACG_HMSP":"3",
# "ACG_LifelineCares_Mobile_App":"1",
# }