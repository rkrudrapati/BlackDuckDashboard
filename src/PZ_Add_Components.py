import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json


# portal = '8.8.8.8'
portal = 'blackduckweb.philips.com'

url = 'https://'+portal+'/j_spring_security_check'
payload = 'j_username=ENTER_EMAILID&j_password=ENTER_PASSWORD'
headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/javascript, */*; q=0.01",
}

response = requests.request("POST", url, data=payload, headers=headers, verify=False)
print(response.headers)
token = response.headers['Set-Cookie']
csrf_token = response.headers['X-CSRF-TOKEN']
print(token)
headers.update({'cookie': token})

post_headers = {
    'Content-Type': "application/json",
    'X-CSRF-TOKEN': csrf_token,
    'cookie': token
}


multi_comp = []
skipped_comp =[]
version_not_exit = []
more_versions = []
with open('data.txt', 'r') as data:
    for lines in data.readlines():
        if not "\t" in lines:
            skipped_comp.append(lines)
            continue
        component, version = lines.split()
        if ":" in version:
            version = version.split(":")[1]
        # print(component, version)
        #   https://8.8.8.8/api/autocomplete/component?ownership=1&ownership=3&q=fuse
        record = component + "|" + version
        comp_url = "https://{}/api/autocomplete/component?ownership=1&ownership=3&q={}".format(portal, component)
        response = requests.request("GET", url=comp_url, headers=headers, verify=False)
        comp_id_url = []
        comp_name = ""
        for each_item in response.json():
            if component.lower() == each_item["value"].lower():
                # print(each_item)
                # comp_name = each_item["value"]
                comp_id_url.append(each_item["url"])
        if comp_id_url.__len__() == 1:
            comp_id = comp_id_url[0].split("/")[-1]
            # print(comp_id)
            version_url = "https://{}/api/components/{}/versions?q=versionName:{}&sort=versionName+ASC&limit=200".format(
                portal, comp_id, version)
            response = requests.request("GET", url=version_url, headers=headers, verify=False)
            # print(response.text)
            if "totalCount" in response.json():
                if response.json()["totalCount"] == 1:
                    # version_id_url = []
                    version_id_url = response.json()["items"][0]["_meta"]["href"]
                    print(version_id_url)
                    # print(version_id_url)
                #     post_data = {"component": version_id_url}
                #     post_url = "https://{}/api/projects/aa024496-9ae8-4434-8bf1-3c92e82593d4/versions/39084439-f319-4928-b6c4-c187570ddf6a/components".format(portal)
                #
                #     new_response = requests.request("POST", url=post_url, data=post_data, headers=post_headers, verify=False )
                #     print(new_response.status_code)
                #     if new_response.status_code == 200:
                #         pass
                #     else:
                #         post_failed.append(comp_name)
                else:
                     more_versions.append(record)
            else:
                version_not_exit.append(record)
        elif comp_id_url.__len__() > 1:
            multi_comp.append(record)
        else:
            skipped_comp.append(record)
print(multi_comp)
print(skipped_comp)
print(version_not_exit)
print(more_versions)
