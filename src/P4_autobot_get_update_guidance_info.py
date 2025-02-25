from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys

project_name = 'H2H_Motiva'
version_name = 'atos_test3'
bot = webdriver.Firefox(executable_path=r'C:\Users\code1\AppData\Local\Programs\Python\Python36\geckodriver.exe')
bot.implicitly_wait(60)
# bot.get('https://blackduckweb.philips.com')
bot.get('https://8.8.8.8')
username = bot.find_element_by_xpath('//*[@id="username"]')
username.send_keys('ENTER_EMAILID')
password = bot.find_element_by_xpath('//*[@id="password"]')
password.send_keys('Thunder$torm')
bot.find_element_by_xpath('/html/body/div[1]/section/div/div[3]/div/form/div[3]/div/button[2]').click()

wait = WebDriverWait(bot, 60)
try:
    wait.until(EC.presence_of_element_located(By.XPATH, '/html/body/div[2]/section/div/div/nav/ul/li[1]/a'))
except Exception as err:
    print("Project Dashboard not loaded")
    print(err)


bot.find_element_by_xpath('/html/body/div[2]/section/div/div/nav/ul/li[1]/a').click()
search_input = bot.find_element_by_xpath('//*[@id="defaultFilterInput"]')
search_input.send_keys(project_name)
search_input.send_keys(Keys.ENTER)
bot.implicitly_wait(60)
var1 = bot.find_element_by_xpath('/html/body/div[2]/section/div/section/div/div/div[2]/div[2]/div/div[1]/table/tbody')
var_list1 = var1.find_elements_by_tag_name('tr')
for td in var_list1:
    print(td.text)
    if project_name in td.text:
        try:
            td.find_element_by_tag_name('a').click()
        except Exception as err:
            print(err)
search_input = bot.find_element_by_xpath('//*[@id="defaultFilterInput"]')
search_input.send_keys(version_name)
search_input.send_keys(Keys.ENTER)
bot.implicitly_wait(60)
#/html/body/div[2]/section/div/section/div/div/div[1]/div[2]/div[2]/div/div[1]/table/tbody/tr/td[2]/a
var1 = bot.find_element_by_xpath('/html/body/div[2]/section/div/section/div/div/div[1]/div[2]/div[2]/div/div[1]/table/tbody')
var_list1 = var1.find_elements_by_tag_name('tr')
for td in var_list1:
    print(td.text)
    if version_name in td.text:
        try:
            td.find_element_by_tag_name('a').click()
        except Exception as err:
            print(err)

#version
bot.find_element_by_xpath('/html/body/div[2]/section/div/div/nav/ul/li[2]/a').click()
time.sleep(10)
vuln_comp_table = bot.find_element_by_xpath('/html/body/div[2]/section/div/section/div/div/div[1]/div[3]/div/div[1]/table/tbody')
vuln_comp_column_list = vuln_comp_table.find_elements_by_tag_name('tr')

for td in vuln_comp_column_list:
    temp = td.find_element_by_class_name('project-version')
    print(temp.find_element_by_class_name('project-name').text)
    print(temp.find_element_by_class_name('version-name no-link').text)
    temp.click()



#/html/body/div[2]/section/div/section/div/div/div[1]/div[3]/div/div[1]/table/tbody/tr[1]
#Update Guidance: /html/body/div[2]/section/div/section/div/div/div[2]/div[1]/div[2]/div/h4
#Update to : /html/body/div[2]/section/div/section/div/div/div[2]/div[1]/div[2]/div/div[1]/div[1]
