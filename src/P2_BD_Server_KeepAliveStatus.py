from time import sleep
from os import system
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from smtplib import SMTP, SMTPException
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
from logging import INFO, DEBUG, ERROR


def check_website(bot):
    bot.get("https://blackduckweb.philips.com")
    # print(bot.title)
    print("Checking Website")
    if bot.title == "Black Duck":
        # bot.quit()
        return True
    return False


def check_ping():
    system('ping blackduck.philip.com > ping.txt')
    print("Checking system status")
    with open('ping.txt', 'r') as ping_reply:
        if "Reply from 8.8.8.8:" in ping_reply:
            return True
        return False
    # print("check")


def check_health(line):
    if '(healthy)' in line:
        return True
    return False


def check_docker_healthy(command):
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect("ENTER_SERVER_URL", username="ENTER_EMAILID", password="ENTER_PASSWORD")
    # cmd_to_execute = command
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    input, output, error = ssh_stdin, ssh_stdout, ssh_stderr
    # system('docker ps > docker_ps_output.txt')
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
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy")
        elif unhealthy_containers == []:
            with open('docker_health_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy")
    except Exception as ssh_err:
        message = "Not able to check docker status. Further investigation is needed.\nError:\n" + ssh_err
        send_mail(message)


def send_mail(message):
    sender = 'noreply@bdcommun.com'
    receivers = ['ENTER_EMAILID', 'ENTER_EMAILID', 'preet.parida@philips.com', 'ravi.sogi@philips.com']
    message = "Subject: BD_Automation Communication Mail\n" + message
    try:
        smtpObj = SMTP('ENTER_SMTP_SERVER_URL', 587)
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")
    sleep(60*60*5) #sleep 5 hours


def system_check():
    try:
        system_up = check_ping()
        if not system_up:
            message = "system is not up"
            send_mail(message)
            with open('system_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy")
        elif system_up:
            with open('system_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy")
    except Exception as sys_err:
        message = "system is not up or not able to check system\nError:\n" + sys_err
        send_mail(message)


def web_server_check():
    try:
        hub_up = check_website(bot)
        if not hub_up:
            message = "Hub website is not up"
            send_mail(message)
            with open('web_server_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Unhealthy")
        elif hub_up:
            with open('web_server_check.txt', 'a+') as f:
                f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": Healthy")
    except Exception as hub_up_err:
        message = "Unable to check hub up status\nError:\n" + hub_up_err
        send_mail(message)


counter = 0
options = Options()
options.add_argument("--headless")
# options.add_argument('--no-sandbox') # Bypass OS security model
# options.add_argument('--disable-gpu')  # applicable to windows os only
# options.add_argument('start-maximized') #
# options.add_argument('disable-infobars')
# options.add_argument("--disable-extensions")
bot = webdriver.Chrome(options=options,
                       executable_path='C:/Users/code1/Desktop/Work/Automation_Work/Server_Monitoring/chromedriver_win32/chromedriver.exe')

while True:
    while datetime.now().minute not in {0, 15, 30,45}:  # Wait 60 second until we are synced up with the 'every 15 minutes' clock
        sleep(60)
    system_check()
    web_server_check()
    counter += 1
    if counter == 4:
        counter = 0
        trigger_to_check_docker_health()
    # if not hub_up and system_up:
    #     trigger_to_check_docker_health()
