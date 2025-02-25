from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


bot = webdriver.Firefox(executable_path=r'C:\Users\code1\AppData\Local\Programs\Python\Python36\geckodriver.exe')
bot.implicitly_wait(60)
# bot.get('https://blackduckweb.philips.com')
bot.get('https://blackduckweb.philips.com/')
username = bot.find_element_by_xpath('//*[@id="username"]')
username.send_keys('ENTER_EMAILID')
password = bot.find_element_by_xpath('//*[@id="password"]')
password.send_keys('ENTER_PASSWORD')
bot.find_element_by_xpath('/html/body/div[1]/section/div/div[3]/div/form/div[3]/div/button[2]').click()

for i in range(2,75):
    projectName = 'test_project' + str(i)
    bot.find_element_by_xpath('//*[@id="createProjectButton"]').click()
    bot.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/form/div[3]/div/div[1]/div/input').send_keys(projectName)
    bot.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/form/div[3]/div/div[4]/div/input').send_keys('1.0')
    bot.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/form/div[4]/div/button[2]').click()
    #bot.('/html/body/div[2]/div[1]/nav[1]/div/div[1]/a/div/img').click()
    time.sleep(5)



bot.quit()
#field_584