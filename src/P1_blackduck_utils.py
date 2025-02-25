from src.P1_headers import delete_request_headers, get_request_headers, post_report_headers
from src.P1_my_requests import delete_request, get_request, post_request
import src.P1_gv_variables as variables
import json


def identify_href_link(project_items, key):
    # print(project_items)
    # for items in project_items:
    #     print(items)
    for links in project_items["_meta"]["links"]:
        # lv_key = links['rel']
        # print(lv_key)
        if key in links['rel']:
            return links["href"]
    return None


def identify_name_href_link(response):
    for items in response.json()["items"]:
        for links in items["_meta"]:
            return links["href"]
    return None


def delete_version(project_id, version_id):  # deletes single version
    print("Deleting:\nProject_ID: %s\nVersion_ID: %s" % (project_id, version_id))
    delete_headers = delete_request_headers()
    delete_url = variables.server_url + '/api/projects/{}/versions/{}'.format(project_id, version_id)
    response = delete_request(url=delete_url, headers=delete_headers)
    print(response)
    print("deleted")


def delete_version_new(version_id):
    print("Deleting:\nVersion_ID: %s" % version_id)
    delete_headers = delete_request_headers()
    print(delete_headers)
    # url : DELETE /api/projects/29193d4e-0184-4494-8189-7bd3490045bb/versions/cd42b893-05ac-4487-adc2-70493967d35d
    delete_url = variables.server_url + '/api/v1/releases/%s' % version_id
    print(delete_url)
    response = delete_request(url=delete_url, headers=delete_headers)
    print(response)
    print("deleted")


def items_in_response(response):
    return response.json()["items"]


def construct_all_version_link(project_items):
    versions_link = identify_href_link(project_items, key='versions')
    versions_link = versions_link + "?limit=999"
    return versions_link


def link_to_select_version(project_items, versionName):
    versions_link = identify_href_link(project_items, key='versions')
    versions_link = versions_link + "?q=versionName%3A" + "%s" % versionName
    return versions_link


def get_project_link(items):
    return items["_meta"]["href"]


def get_project_name(items):
    return items["name"]


def get_project_id(items):
    # return items[]
    pass


def get_codelocation_count(response):
    count = response.json()["totalCount"]
    return count


def get_codelocation_link(items):
    link = items["_meta"]["href"]
    link = link + "/codelocations"
    return link
    # for rels in items["_meta"]["links"]["rel"]:
    #     if rels =="codelocations":
    #         return items[]


def get_report_payload(versionID):
    report_payload = variables.report_payload
    report_payload.update({'versionId': versionID})
    return report_payload


def generate_version_report(server_url, key_project_name, key_version_name):
    get_headers = get_request_headers()
    url = server_url + "/api/projects?q=name%3A{}".format(key_project_name)
    project_response = get_request(url=url, headers=get_headers)
    all_project_items = items_in_response(response=project_response)
    for items in all_project_items:
        project_link = get_project_link(items)
        project_name = get_project_name(items)
        project_id = project_link.split('/')[-1]
        versions_link = link_to_select_version(items, key_version_name)
        versions_response = get_request(url=versions_link, headers=get_headers)
        all_version_items = items_in_response(response=versions_response)
        for v_items in all_version_items:
            version_name = v_items['versionName']
            version_id = v_items["_meta"]["href"].split('/')[-1]
            if version_name == key_version_name:
                payload = json.dumps(get_report_payload(version_id))
                report_url = "{}/api/versions/{}/reports".format(server_url, version_id)
                report_response = post_request(url=report_url, payload=payload, headers=post_report_headers())
                if report_response.status_code == 201:
                    print("Report created for - \nproject: {} \nversion name:{}".format(project_name, version_name))
                break


