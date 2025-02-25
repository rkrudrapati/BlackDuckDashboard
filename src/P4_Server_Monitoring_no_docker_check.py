"""
docker health check code is commented
"""

from time import sleep
from smtplib import SMTP, SMTPException
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import subprocess
import os

#from paramiko import SSHClient, AutoAddPolicy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


docker_health_check_flag = False
hub_link = 'https://blackduckweb.philips.com'
ping_link = 'blackduckweb.philips.com'
ssh_ip = '8.8.8.8'
ssh_username = 'code1@philips.com'
ssh_password = 'security@21'
mail_recepients = ['ENTER_EMAILID'] 	#DL mail
smtp_relay_server = 'ENTER_SMTP_SERVER_URL'
smtp_relay_port = 587 # generally, default port is 587
global failure_checks
failure_checks = {
    'system_flag': True,
    'web_server_flag': True,
    'mail_triggered': False
}

if docker_health_check_flag:
    failure_checks.update({'docker_flag': True})


def check_website(bot):
    bot.get(hub_link)
    # print(bot.title)
    print("Checking Website")
    bot.implicitly_wait(20)
    sleep(20)
    if bot.title == "Black Duck":
        # bot.quit()
        return True
    return False


def check_ping():
    flag = False
    print("Checking system status")
    with open(os.devnull, "wb") as limbo:
        result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ping_link], stdout=limbo, stderr=limbo).wait()
        if result:
            print(ping_link, "inactive")
        else:
            print(ping_link, "active")
            flag = True
    return flag


def check_health(line):
    if '(healthy)' in line:
        return True
    return False


def check_docker_healthy(command):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(ssh_ip, username=ssh_username, password=ssh_password)
    # cmd_to_execute = command
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    input, output, error = ssh_stdin, ssh_stdout, ssh_stderr
    unhealthy = []
    for each_item in output:
        if each_item == "":
            continue
        if 'blackducksoftware/blackduck' in each_item:
            if not check_health(each_item):
                unhealthy.append(each_item.split()[1])
    ssh.exec_command("exit")
    return unhealthy


def trigger_to_check_docker_health():
    try:
        unhealthy_containers = check_docker_healthy("docker ps")
        print("Checking docker health")
        if unhealthy_containers != []:
            message = "Some containers are unhealthy"
            send_mail(message)
            with open('docker_health_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy\n")
            return True
        elif unhealthy_containers == []:
            with open('docker_health_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy\n")
            return False
    except Exception as ssh_err:
        message = "Not able to check docker status. Further investigation is needed.\nError:\n" + str(ssh_err)
        send_mail(message)
        return True


def send_mail(message_body):
    print("Mail Sent: {}".format(message_body))
    if failure_checks['mail_triggered']: #already triggered once before
        print("waiting for min time before triggering mail")
        return
    sender = 'noreply@bdcommun.com'
    receivers = mail_recepients
    message = MIMEMultipart()
    message["Subject"] = "Subject: BD_Automation Communication Mail"
    body = message_body
    body = MIMEText(body) # convert the body to a MIME compatible string
    message.attach(body)
    try:
        smtpObj = SMTP(smtp_relay_server, smtp_relay_port)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("Successfully sent email")
        smtpObj.quit()
        failure_checks['mail_triggered'] = True
    except SMTPException:
        print("Error: unable to send email")

    # sleep(60*60*5) #sleep 5 hours


def system_check():
    try:
        system_up = check_ping()
        if not system_up:
            message = "system is not up"
            send_mail(message)
            with open('system_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy\n")
            return True
        elif system_up:
            with open('system_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy\n")
            return False
    except Exception as sys_err:
        message = "system is not up or not able to check system\nError:\n" + str(sys_err)
        send_mail(message)
        return True


# def chrome_count():
#     count = 0
#     for p in psutil.process_iter():
#         if "chrome.exe" in p.name():
#             count += 1
#     print(count)


def post_request(url, payload, headers):
    try:
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        if response.status_code == 204:  # re.match(r'20(0|4)'):    # checks 200 or 204
            # print(response.status_code)
            return response
        else:
            print('request failed')
            print('Response status: %d' % (response.status_code))
            print('Method: post_request')
            print('request response: \n %s' % response.text)
    except Exception as err:
        print(err)


def get_request(url, headers):
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        if response.status_code == 200 or response.status_code == 204:#re.match(r'20[0-9]'):    # check 200 to 209
            return response
        else:
            print('request failed')
            print('Response status: %d' % (response.status_code))
            print('Method: get_request')
            print('request response: \n %s' % response.text)
    except Exception as err:
        print(err)


def web_server_check_through_api():
    payload = {"j_username": "testuser1", "j_password": "blackduck"}
    login_url = hub_link + '/j_spring_security_check'
    login_headers = {
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json, text/javascript, */*; q=0.01"
    }
    response = post_request(url=login_url, payload=payload, headers=login_headers)
    lv_token = response.headers['Set-Cookie']
    get_headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'X-Requested-With': "XMLHttpRequest",
        'Accept': "application/json",
        'cookie': lv_token
    }
    url = hub_link + "/api/projects?limit=999"
    response = get_request(url=url, headers=get_headers)
    project_name = response.json()["items"][0]["name"]
    print(project_name)
    try:
        if project_name == "test_project_3":
            # hub_up = True
            with open('web_server_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy\n")
            return False
        else:
            message = "Hub website is not up"
            send_mail(message)
            with open('web_server_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy\n")
            return True
    except Exception as hub_up_err:
        message = "Unable to check hub up status\nError:\n" + str(hub_up_err)
        send_mail(message)
        return True


def web_server_check():
    options = Options()
    options.add_argument("--headless")
    bot = webdriver.Chrome(options=options, executable_path=r"C:\Users\code1\Libraries\chromedriver_win32\chromedriver.exe")
    # chrome_count()
    try:
        hub_up = check_website(bot)
        bot.quit()
        if not hub_up:
            message = "Hub website is not up"
            send_mail(message)
            with open('web_server_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy\n")
            return True
        elif hub_up:
            with open('web_server_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy\n")
            return False
    except Exception as hub_up_err:
        message = "Unable to check hub up status\nError:\n" + str(hub_up_err)
        send_mail(message)
        bot.quit()
        return True


def reset_failure_check_flags():
    failure_checks['system_flag'] = True
    failure_checks['web_server_flag'] = True
    if docker_health_check_flag:
        failure_checks['docker_flag'] = True


# logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')
# logger = logging.getLogger()
# options = Options()
# options.add_argument("--headless")
# # options.add_argument('--no-sandbox') # Bypass OS security model
# # options.add_argument('--disable-gpu')  # applicable to windows os only
# # options.add_argument('start-maximized') #
# # options.add_argument('disable-infobars')
# options.add_argument("--disable-extensions")
# bot = webdriver.Chrome(options=options,
#                         executable_path='C:/Users/code1/Desktop/Work/Automation_Work/'
#                                         'Server_Monitoring/chromedriver_win32/chromedriver.exe')

counter = 0
trigger_counter = 0
lv_flag = True
while True:
    if failure_checks['mail_triggered']:
        trigger_counter += 1
    if trigger_counter == 20: # waiting for 5 hours #20 = 5hrs * 4 15mins check
        trigger_counter = 0
        failure_checks['mail_triggered'] = False
    while datetime.now().minute not in {0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55}:     #{0, 15, 30, 45}:
        # Wait 60 second until we are synced up with the 'every 15 minutes' clock
        lv_flag = True  # this flag helps to run the below checks only once.
        sleep(60)
    if lv_flag:
        lv_flag = False
        failure_checks['system_flag'] = system_check()
        if not failure_checks['system_flag']:
            # failure_checks['web_server_flag'] = web_server_check()
            failure_checks['web_server_flag'] = web_server_check_through_api()
            # error check not neede, if the system is up & hub is not working, obviously check the docker status
            if docker_health_check_flag:
                counter += 1
                if counter == 4:
                    counter = 0
                    failure_checks['docker_flag'] = True
                    failure_checks['docker_flag'] = trigger_to_check_docker_health()
        # sleep(60)
    # '''
    # -> case where failure is rectified and the mail should be reset
    # -> below cases check where docker health is verified and not verified
    # '''
    if docker_health_check_flag:
        if not failure_checks['system_flag'] and not failure_checks['web_server_flag'] and \
                failure_checks['mail_triggered']:
            trigger_counter = 0
            failure_checks['mail_triggered'] = False
    else:
        if not failure_checks['system_flag'] and not failure_checks['web_server_flag'] and counter < 4 and \
                failure_checks['mail_triggered']:
            trigger_counter = 0
            failure_checks['mail_triggered'] = False
        elif not failure_checks['system_flag'] and not failure_checks['web_server_flag'] and \
                failure_checks['mail_triggered']:# and not failure_checks['docker_flag']: 		# enable this when to check docker health status
            trigger_counter = 0
            failure_checks['mail_triggered'] = False
    # reset the failure checks
    reset_failure_check_flags()

    # if not hub_up and system_up:
    #     trigger_to_check_docker_health()

