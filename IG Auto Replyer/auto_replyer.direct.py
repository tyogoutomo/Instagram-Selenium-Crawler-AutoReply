import time, stdiomask
import getpass
import sys
import selenium
from selenium import webdriver

login_id = 'tyogotest1' #input('Put your IG account here! ')
password = 'username' #getpass.getpass('Put your IG password here! ')

username = 'tyogotest2' #to be use as a variable that contain new follower username(s)
messagetext = "Hello there!"

sendmessage_button = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/button'
searchusername_textbox = '/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input'
findusername_button = '/html/body/div[4]/div/div/div[2]/div[2]/div'
findusername_label = '/html/body/div[4]/div/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div'
findnext_button = '/html/body/div[4]/div/div/div[1]/div/div[2]'
message_textbox = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'
messagesend_button = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'

def login_instagram():
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)

        username_bar = driver.find_element_by_name("username")
        username_bar.send_keys(login_id)

        password_bar = driver.find_element_by_name("password")
        password_bar.send_keys(password)
        time.sleep(2)

        login_button = driver.find_element_by_class_name("L3NKy")
        login_button.click()
    except:
        pass

####################### THIS IS WHERE THE PROGRAM BEGINS #######################
driver = webdriver.Chrome("C:\\Windows\\webdriver\\chromedriver.exe")

login_instagram()
time.sleep(5)
driver.get("https://www.instagram.com/direct/inbox/")
notificationnotnow_button = '/html/body/div[4]/div/div/div/div[3]/button[2]'
time.sleep(1)
driver.find_element_by_xpath(notificationnotnow_button).click()
time.sleep(3)

for i in range(0, 1):
    driver.find_element_by_xpath(sendmessage_button).click()
    time.sleep(1)

    driver.find_element_by_xpath(searchusername_textbox).send_keys(username)
    time.sleep(2)

    findusernametest = driver.find_element_by_xpath(findusername_label).text
    if str(findusernametest) == username:
        driver.find_element_by_xpath(findusername_button).click()
        driver.find_element_by_xpath(findnext_button).click()
    else:
        print('cannot find match username for: ' + findusernametest)
        driver.close()
        sys.exit()
    
    time.sleep(2)
    driver.find_element_by_xpath(message_textbox).send_keys(messagetext)
    time.sleep(2)
    driver.find_element_by_xpath(messagesend_button).click()
    time.sleep(2)
    driver.get("https://www.instagram.com/direct/inbox/")

driver.close()