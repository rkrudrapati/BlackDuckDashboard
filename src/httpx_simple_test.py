"""
this program is to check how much time the httpx library is taking without using any advance methods.
This program enumerates the risk profile of all the project versions.
"""
import httpx
import time

start = time.time()
# server_url = 'https://blackduckweb.philips.com/'
server_url = 'https://8.8.8.8/'
api_token = "YzljZjFhYjktMDJlhYmVmLTk3MTEyZjg5ODQ4Ng==" \
    # Enter api token here

if server_url[-1] == "/":
    server_url = server_url[:-1]

# csrf_token = ''
# auth_token = ''
login_headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Authorization': 'token {}'.format(api_token),
}
login_url = server_url + '/api/tokens/authenticate'
login_response = httpx.post(url=login_url, json={}, headers=login_headers, verify=False)
auth_token = login_response.json()['bearerToken']
csrf_token = login_response.headers['X-CSRF-TOKEN']

get_header = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'X-Requested-With': "XMLHttpRequest",
    'Accept': "application/json",
    'X-CSRF-TOKEN': csrf_token,
    'Authorization': 'bearer {}'.format(auth_token)
}

projects_url = f"{server_url}/api/projects"
projects_request_response = httpx.get(url=projects_url, headers=get_header, verify=False)
for each_project in projects_request_response.json()["items"]:
    print("Project Name: ", each_project['name'])
    version_link = each_project['_meta']['links'][0]['href']
    version_request_response = httpx.get(url=version_link + "/", headers=get_header, verify=False)
    for each_version in version_request_response.json()['items']:
        print("Version name : ", each_version['versionName'])
        for attributes in each_version['_meta']['links']:
            if attributes['rel'] == 'riskProfile':
                # print(attributes['href'])
                risk_url = attributes['href']
                riskProfiles = httpx.get(url=risk_url, headers=get_header, verify=False)
                for profileRisk in riskProfiles.json()['categories']:
                    print(profileRisk + " : ", riskProfiles.json()['categories'][profileRisk])
                break
        print("-" * 100)
    print("=" * 150)
# e_time = datetime.datetime.now()
stop = time.time()
print(stop - start)

# 9 0r 10 sec
