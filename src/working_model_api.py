"""
Gives vulnerability information for all the latest versions in the projects
Covered:
    1. Security Vulnerable components count
    2. Security Vulnerabilities/Issues count
    3. Remove duplicates issues in the count
    4. Issues are categorized on the basis of severity
"""

from os import system
from os import getcwd
import json
import logging
import xlsxwriter
import sys
import timeit

commands_count = 0
"""
Disable the 'logs_enable' flag when logs are not required.
"""
start = timeit.default_timer()
logs_enable = True
test = True
if logs_enable:
    system("rm -rf logs_file.log")
    if test == True: print("rm -rf logs_file.log")
    logging.basicConfig(filename='logs_file.log', level=logging.DEBUG)

workbook = xlsxwriter.Workbook('dashboard_latest_version.xlsx')
worksheet = workbook.add_worksheet()


# list the items that will be displayed in the dashboard report
def initialize_result_list_buffer():
    if logs_enable: logging.info("Initializing the result buffer")
    result.append(0) #excel row count
    result.append("Project Name")
    result.append("Version Name")
    result.append("High Vuln Components")
    result.append("Medium Vuln Components")
    result.append("Low Vuln Components")
    result.append("High Vuln Issues")
    result.append("Medium Vuln Issues")
    result.append("Low Vuln Issues")
    if logs_enable:
        logging.info(result)
        logging.info("result buffer initialized")
    #return result


""" 
    Initilize workbook with headings
    Required parameters:    result buffer
"""
def write_to_workbook():
    limit = len(result)
    for i in range(limit-1):
        worksheet.write(chr(65 + i) + str(result[0]+1), result[i+1])
        #worksheet.
    print(result)
    progress_bar()
    result[0] += 1

"""
    Executes the command.
    Need to import system from os
    cmd: from os import system
"""



def progress_bar():
    num_of_projects = 150
    max_percent = 100
    progress_percent = (result[0])*(max_percent/num_of_projects)
    show_progress = ""
    for i in range(max_percent):
        if(i <= progress_percent):
            show_progress = show_progress+"#"
        else:
            show_progress = show_progress + " "
    show_progress = show_progress + "%d percent completed" % progress_percent
    print(show_progress)


def execute_command(command):
    try:
        #commands_count += 1
        system(command)
        print(command)
        if test == True: print(result)
        #progress_bar()
    except Exception as error:
        if type(error) == str:
            logging.error(error)
            sys.exit()
        else:
            print(error)
            print(type(error))
            sys.exit()



def risk_profile_info():
    try:
        project_name = name_sanitization(str(result[1]))
        version_name = name_sanitization(str(result[2]))
        risk_profile_file = getcwd() + "/resource/risk_profile/" + project_name+"_" + version_name + ".json"
        with open(risk_profile_file, 'r') as risk_profile_info:
            risk_data = json.load(risk_profile_info)
            high = risk_data["categories"]["VULNERABILITY"]["HIGH"]
            medium = risk_data["categories"]["VULNERABILITY"]["MEDIUM"]
            low = risk_data["categories"]["VULNERABILITY"]["LOW"]
            result[3] = high
            result[4] = medium
            result[5] = low
        risk_profile_info.close()
    except Exception as err_data:
        risk_profile_info.close()
        #for debug purpose write the above logs code here
        logging.error("Function: vulnerable_bom_info")
        logging.error(result)
        logging.error(err_data)

def vulnerable_bom_info():
    check_duplicate_CVE = []
    duplicate_issues = []
    issues_count = [0, 0, 0]
    filename = result[1]+result[2]+".csv"
    csvfile = open(filename,'w')
    try:
        project_name = name_sanitization(str(result[1]))
        version_name = name_sanitization(str(result[2]))
        vuln_bom_file = getcwd() + "/resource/BOM/" + project_name+"_" + version_name + ".json"
        with open(vuln_bom_file, 'r') as security_vuln_info:
            vuln_data = json.load(security_vuln_info)
            num_of_vuln = vuln_data["totalCount"]
            for each_vuln in range(num_of_vuln):
                CVE_ID = vuln_data["items"][each_vuln]["vulnerabilityWithRemediation"]["vulnerabilityName"]
                remediationStatus = vuln_data["items"][each_vuln]["vulnerabilityWithRemediation"]["remediationStatus"]
                componentName = vuln_data["items"][each_vuln]["componentName"]
                componentVersionName = vuln_data["items"][each_vuln]["componentVersionName"]
                vulnerabilityName = vuln_data["items"][each_vuln]["vulnerabilityWithRemediation"]["vulnerabilityName"]
                if CVE_ID in check_duplicate_CVE:
                    duplicate_issues.append(CVE_ID)
                else:
                    check_duplicate_CVE.append(CVE_ID)
                    if remediationStatus == "NEW":
                        severity = vuln_data["items"][each_vuln]["vulnerabilityWithRemediation"]["severity"]
                        if severity == "HIGH":
                            issues_count[0] += 1
                        if severity == "MEDIUM":
                            issues_count[1] += 1
                        if severity == "LOW":
                            issues_count[2] += 1
                        csvfile.write(result[1]+","+result[2]+","+
                            componentName + "," + componentVersionName + "," + vulnerabilityName + "," + remediationStatus + "," + severity + "\n")
                    else:
                        if logs_enable: logging.info("New remediation status: %s" % remediationStatus)
        security_vuln_info.close()
        csvfile.close()
        if logs_enable:
            logging.info("Total number of issues in json: " + str(num_of_vuln))
            logging.info("High, Medium, Low issues count after removing duplicates: \n" + str(issues_count))
            logging.info("Number of duplicate issues: " + str(len(duplicate_issues)))
            logging.info("Duplicate issues: ")
            logging.info(duplicate_issues)
        return issues_count
    except Exception as err_data:
        security_vuln_info.close()
        csvfile.close()
        #for debug purpose write the above logs code here
        if logs_enable:
            logging.error("Function: vulnerable_bom_info")
            logging.error(result)
            logging.error(err_data)
            logging.info("Total number of issues in json: " + str(num_of_vuln))
            logging.info("High, Medium, Low issues count after removing duplicates: \n" + str(issues_count))
            logging.info("Number of duplicate issues: " + str(len(duplicate_issues)))
            logging.info("Duplicate issues: ")
            logging.info(duplicate_issues)
    return issues_count

def version_info():
    try:
        project_name = name_sanitization(str(result[1]))
        version_file = getcwd()+"/resource/versions/"+project_name+".json"
        if logs_enable: logging.info("Version directory: \n %s" % version_file)
        with open(version_file, 'r') as all_version_info:
            issues_count = [0, 0, 0]
            version_data = json.load(all_version_info)
            num_of_versions = version_data["totalCount"]
            result[2] = version_data["items"][num_of_versions-1]["versionName"]
            version_name = name_sanitization(str(result[2]))
            risk_profile_url = version_data["items"][num_of_versions - 1]["_meta"]["links"][2]["href"]
            risk_profile_command = "curl -b cookie.txt -X GET --header 'Accept: application/json' '" + \
                                   risk_profile_url + "' --insecure > resource/risk_profile/"+project_name+"_"+version_name+".json"
            vulnerable_bom_components_url = version_data["items"][num_of_versions - 1]["_meta"]["links"][5]["href"]
            if logs_enable:
                logging.info("Number of versions in project - %s: %s" % (result[1], num_of_versions))
                logging.info("Gathering info for version: " + result[2])
                logging.info("Risk profile url: \n" + risk_profile_url)
                logging.info("Risk profile command: \n" + risk_profile_command)
            execute_command(risk_profile_command)
            risk_profile_info()
            ############################
            if result[3] != 0 or result[4] != 0 or result[5] != 0:
                vulnerable_bom_components_command = "curl -b cookie.txt -X GET --header 'Accept: application/json' '" \
                                                + vulnerable_bom_components_url + \
                                                "?limit=9999' --insecure >  resource/BOM/"+project_name+"_"+version_name+".json"
                if logs_enable:
                    logging.info("Vulnerable components url: \n" + vulnerable_bom_components_url)
                    logging.info("Vulnerable components command: \n" + vulnerable_bom_components_command)
                execute_command(vulnerable_bom_components_command)
                issues_count = vulnerable_bom_info()
            else:
                if logs_enable: logging.info("Contains no issues in the risk report.")
                pass
            result[6] = issues_count[0]
            result[7] = issues_count[1]
            result[8] = issues_count[2]
            all_version_info.close()
            write_to_workbook()
            result[2] = "Version Name" #TODO: change later
            result[3] = 0
            result[4] = 0
            result[5] = 0
            result[6] = 0
            result[7] = 0
            result[8] = 0

    except Exception as err_data:
        logging.error(err_data)
        logging.error(result)


def projects_info():
    get_projects_info = 'curl -b cookie.txt -X GET --header "Accept: application/json" ' \
                        '"https://blackduckweb.philips.com:443/api/projects?limit=999" --insecure > resource/projects.json'
    if logs_enable: logging.info("command to get projects info: \n"+get_projects_info)
    execute_command(get_projects_info)
    try:
        projects_list_file = getcwd()+"/resource/projects.json"
        with open(projects_list_file,'r') as all_projects_name_info:
            project_data = json.load(all_projects_name_info)
            num_of_projects = project_data["totalCount"]
            if logs_enable: logging.info("Number of Projects: %s" % num_of_projects)
            for each_project in range(num_of_projects):
                result[1] = project_data["items"][each_project]["name"]
                project_name = name_sanitization(str(result[1]))
                each_project_url = project_data["items"][each_project]["_meta"]["href"]
                version_url = each_project_url.strip(" ") + "/versions?limit=999"
                version_command = "curl -b cookie.txt -X GET --header 'Accept: application/json' '" + \
                                  version_url + "' --insecure > resource/versions/"+project_name+".json"
                if logs_enable:
                    logging.info("Project Name: %s" % result[1])
                    #logging.info(each_project_url)#todo: not required
                    logging.info("Version URL: \n" + version_url)
                execute_command(version_command)
                version_info()
                # result[1] = "Project Name"
        all_projects_name_info.close()

    except Exception as err_data:
        logging.error(err_data)
        logging.error(result)
        sys.exit()


def pilot():
    projects_info()


def name_sanitization(name):
    if " " in name:
        name = name.replace(" ", "_")
    if "/" in name:
        name = name.replace("/", "_")
    if "(" in name:
        name = name.replace("(", "_")
    if ")" in name:
        name = name.replace(")", "")
    if "&" in name:
        name = name.replace("&", "_")
    return name


result = []
def main():
    initialize_result_list_buffer()
    write_to_workbook()  # initilize workbook with headings
    # username =
    # password =
    login_cookie_command = "curl -X POST --data 'j_username=testuser1&j_password=blackduck' -i " \
                           "https://blackduckweb.philips.com/j_spring_security_check --insecure -c cookie.txt"
    # JSESSION ID will be stored in cookie which will be used for login purpose in other commands
    execute_command(login_cookie_command)  # TODO: add exception handle if login is not successful.

    pilot()
    #workbook.close()

try:
    main()
except Exception as err:
    print(err)
workbook.close()
stop = timeit.defaulttimer()
print(stop - start)