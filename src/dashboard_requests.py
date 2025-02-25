import timeit
import logging
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# import warnings
# warnings.filterwarnings('ignore', category=InsecureRequestWarning)


def generate_token_and_update_cookie():
    url = 'https://' + portal + '/j_spring_security_check'
    payload = 'j_username=ENTER_USERNAME&j_password=ENTER_PASSWORD'
    if log_enable:
        logging.info("Portal: %s" % portal)
        logging.info("Payload: %s" % payload)
        logging.info("Header: %s" % headers)

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    if response.status_code == 200 or response.status_code == 204:
        print("Login Successful")
    else:
        print("Failed to Login")

    # print(type(response))
    # print(response)
    # print(dir(response))

    token = response.headers['Set-Cookie']
    print(token)
    # token = "AUTHORIZATION_BEARER=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9
    headers.update({'cookie': token})
    if log_enable:
        logging.info("Header: %s" % headers)


def get_projects_list():
    lv_project_name_list = []
    lv_project_url_list = []
    # url = 'https://'+portal+':443/api/projects?limit=999'
    url = 'https://' + portal + '/api/projects?limit=999'
    response = requests.request("GET", url, headers=headers, verify=False)
    if response.status_code == 200 or response.status_code == 204:
        if log_enable:
            logging.info("Successfully obtained project info\n")
            logging.info(response.status_code)
    else:
        if response.status_code == 400 or response.status_code == 401:
            if log_enable: logging.info("Error code 400 \nRegenerating token")
            generate_token_and_update_cookie()
            response = requests.request("GET", url, headers=headers, verify=False)
            if response.status_code == 200 or response.status_code == 204:
                if log_enable:
                    logging.info("Successfully obtained project info after regenerating authentication\n")
                    logging.info(response.status_code)
            else:
                if log_enable:
                    logging.error("Failed to obtain project info after regenerating authentication\n")
                    logging.error(response.status_code)
                    # break code here #todo
        else:
            if log_enable:
                logging.info("Failed to obtained project info\n")
                logging.info(response.status_code)

    for project in response.json()['items']:
        if 'test_project' in project['name']:
            continue
        else:
            lv_project_name_list.append(project['name'])
            lv_project_url_list.append(project['_meta']['href'])
    return [lv_project_name_list, lv_project_url_list]


def mainloop():
    regenerate_token = True
    for i in range(project_name_list.__len__()):
        output = ""
        output = project_name_list[i] + ","
        url = project_url_list[i] + "/versions?limit=999"
        # print(url)
        if log_enable: logging.info(output + "\n" + url)
        response = requests.request("GET", url, headers=headers, verify=False)
        if response.status_code == 200 or response.status_code == 204:
            if log_enable:
                logging.info("Successfully obtained versions info\n")
                logging.info(response.status_code)
        else:
            if response.status_code == 400 or response.status_code == 401:
                if log_enable:
                    logging.error("Failed to obtain versions info")
                    logging.info("Error code 400 \nRegenerating token")
                generate_token_and_update_cookie()
                response = requests.request("GET", url, headers=headers, verify=False)
                if response.status_code == 200 or response.status_code == 204:
                    if log_enable:
                        logging.info("Successfully obtained versions info after regenerating authentication\n")
                        logging.info(response.status_code)
                else:
                    if log_enable:
                        logging.error("Failed to obtain versions info after regenerating authentication\n")
                        logging.error(response.status_code)
                        break
            else:
                if log_enable:
                    logging.error("Failed to obtain versions info after regenerating authentication\n")
                    logging.error(response.status_code)

        version_details = ["", "", "", ""]
        created_date = ""
        try:
            for each_version in response.json()['items']:
                temp = each_version['createdAt']
                temp = temp[:temp.index('T')]
                if temp > created_date:  # same dates then check bom updated needs to be implemented
                    version_details[0] = each_version['versionName']
                    version_details[1] = temp  # each_version['createdAt']
                    version_details[2] = each_version['settingUpdatedAt']
                    version_details[3] = each_version['_meta']
            output = output + "'" + version_details[0] + ","
        except Exception as err:
            if log_enable:
                logging.error("Failed while checking for latest version\n")
                logging.error(err)
                logging.error("How and why did I reach here")
                # logging.error(version_details, '\n', created_date)
            if regenerate_token:
                generate_token_and_update_cookie()
                i -= 1
                regenerate_token = False
            else:
                output = output + 'NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA'
                dashboard.writelines(output + "\n")
                print(output)
            continue

        if log_enable: logging.info(
            "Latest Version: " + version_details[0] + "\ncreatedAt: " + version_details[1] + "\nsettingUpdatedAt: " +
            version_details[2])

        for items in version_details[3]['links']:
            if items['rel'] == 'riskProfile':
                riskURL = items['href']
                # print(riskURL)
                if log_enable: logging.info("Risk URL: %s" % riskURL)
                response = requests.request("GET", url=riskURL, headers=headers, verify=False)
                if response.status_code == 200 or response.status_code == 204:
                    if log_enable:
                        logging.info("Successfully obtained risk profile info\n")
                        logging.info(response.status_code)
                else:
                    if log_enable:
                        logging.error("Failed to obtain versions risk profile\n")
                        logging.error(response.status_code)
                    output = output + 'NA,NA,NA,NA,NA,NA,NA,NA,NA,'
                    continue
                try:
                    licenseRiskComponents = list(response.json()['categories']['LICENSE'].values())
                    for values in range(3):
                        output = output + str(licenseRiskComponents[values]) + ","
                except Exception as err:
                    if log_enable:
                        logging.error("Failed to get license risk info\n")
                        logging.error(err)
                    output = output + 'NA,NA,NA,'
                try:
                    operationalRiskComponents = list(response.json()['categories']['OPERATIONAL'].values())
                    for values in range(3):
                        output = output + str(operationalRiskComponents[values]) + ","
                except Exception as err:
                    if log_enable:
                        logging.error("Failed to get operational risk info\n")
                        logging.error(err)
                    output = output + 'NA,NA,NA,'
                try:
                    securityRiskComponents = list(response.json()['categories']['VULNERABILITY'].values())
                    for values in range(3):
                        output = output + str(securityRiskComponents[values]) + ","
                except Exception as err:
                    if log_enable:
                        logging.error("Failed to get security risk info\n")
                        logging.error(err)
                    output = output + 'NA,NA,NA,'

            if items['rel'] == 'vulnerable-components':
                vuln_comp_URL = items['href']
                vuln_comp_URL = vuln_comp_URL + "?limit=999"
                if log_enable: logging.info("Vuln Components URL: %s" % vuln_comp_URL)
                high, medium, low = 0, 0, 0
                response = requests.request("GET", url=vuln_comp_URL, headers=headers, verify=False)
                if response.status_code == 200 or response.status_code == 204:
                    if log_enable:
                        logging.info("Successfully obtained security vulnerability profile info\n")
                        logging.info(response.status_code)
                else:
                    if log_enable:
                        logging.error("Failed to obtain security vulnerability risk profile\n")
                        logging.error(response.status_code)
                try:
                    for issues in response.json()['items']:
                        severity = issues['vulnerabilityWithRemediation']['severity']
                        remediationStatus = issues['vulnerabilityWithRemediation']['remediationStatus']
                        # if remediationStatus != 'NEW':
                        #     print("New remediationStatus: \n %s" % remediationStatus)
                        if severity == 'HIGH' and remediationStatus == 'NEW':
                            high += 1
                        elif severity == 'MEDIUM' and remediationStatus == 'NEW':
                            medium += 1
                        elif severity == 'LOW' and remediationStatus == 'NEW':
                            low += 1
                except Exception as err:
                    if log_enable:
                        logging.info(response.json())
                        logging.error("Failed to get security vuln info\n")
                        logging.error(err)

                output = output + str(high) + ',' + str(medium) + ',' + str(low)
                if log_enable: logging.info(output)

        dashboard.writelines(output + "\n")
        print(output)


##################################################################################

start = timeit.default_timer()
log_enable = True
if log_enable: logging.basicConfig(filename='logs_file.log', level=logging.DEBUG)
# portal = '8.8.8.8'
# portal = '8.8.8.8' #Atos
portal = 'blackduckweb.philips.com'
headers = {
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Accept': "application/json, text/javascript, */*; q=0.01",
}

generate_token_and_update_cookie()

project_name_list = []
project_url_list = []
[project_name_list, project_url_list] = get_projects_list()

dashboard = open('result.csv', 'w')
dashboard.writelines('Project Name,Project Version, License Risk High, License Risk Medium, License Risk Low,'
                     'Operational Risk High, Operational Risk Medium, Operational Risk Low,'
                     'Security Vuln High, Security Vuln Medium, Security Vuln Low,'
                     'High Security Issues, Medium Security Issues, Low Security Issues\n')

mainloop()
dashboard.close()
stop = timeit.default_timer()
print(stop - start)
