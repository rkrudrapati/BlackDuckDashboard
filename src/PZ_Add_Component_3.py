import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json

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
        # if not "\t" in lines:
        #     skipped_comp.append(lines)
        #     continue
        component, version = lines.split()
        if ":" in version:
            version = version.split(":")[1]
        if ":" in component:
            component = component.split(":")[1]
        if "+" in version:
            version = version.split("+")[1]
        record = component + "|" + version
        comp_url = "https://{}/api/autocomplete/component?ownership=1&ownership=3&q={}".format(portal, component)
        response = requests.request("GET", url=comp_url, headers=headers, verify=False)
        comp_id_url = []
        comp_name = ""
        break_free = False
        for each_item in response.json():
            if break_free:
                break
            if component.lower() == each_item["value"].lower():
                comp_id_url.append(each_item["url"])
                comp_id = comp_id_url[0].split("/")[-1]
                # print(comp_id)
                version_url = "https://{}/api/components/{}/versions?q=versionName:{}&sort=versionName+ASC&limit=200".format(
                portal, comp_id, version)
                new_response = requests.request("GET", url=version_url, headers=headers, verify=False)
                for versions_info in new_response.json()["items"]:
                    if version.lower() == versions_info["versionName"]:
                        version_id_url = new_response.json()["items"][0]["_meta"]["href"]
                        print(each_item["value"].lower())
                        print(versions_info["versionName"])
                        print(version_id_url)
                        break_free = True
print(multi_comp)
print(skipped_comp)
print(version_not_exit)
print(more_versions)
