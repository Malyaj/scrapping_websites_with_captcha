# -*- coding: utf-8 -*-

""" Webscraping Assignment"""

path_to_chromedriver = r"D:\Users\703143501\Anaconda3\chromedriver.exe"

from selenium import webdriver
from bs4 import BeautifulSoup as bs

url = "http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do"

download_dir = r"D:\Users\703143501\Downloads"
chrome_options = webdriver.ChromeOptions()
preferences = {"download.default_directory": download_dir ,
               "directory_upgrade": True,
               "safebrowsing.enabled": True }

chrome_options.add_experimental_option("prefs", preferences)
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=path_to_chromedriver)

#val = "abdg4"


driver.get(url)
size = driver.get_window_size()
print("window size is {size}".format(size = size))
driver.save_screenshot('screenshot.png')



#captcha_id = "captcha"
#captcha_field = driver.find_element_by_id(captcha_id)
##img_src = captcha_field.get_attribute('src')
##print(img_src)
#captcha_field.

#cin_id="companyID"
#cin_field = driver.find_element_by_id(cin_id)
#cin_field.send_keys(val)


#password_field = driver.find_element_by_name("password") # get the password field
#username_field.send_keys(SSO) # enter in your username
#password_field.send_keys(prep([a1, a2, a3, a4])) # enter in your password
#submit_field = driver.find_element_by_name("submitFrm")
#submit_field.click()

#xpath = """//*[@id="divCond_10207783"]/td[2]/a"""
#elem = driver.find_element_by_xpath(xpath)
#href = elem.get_attribute('href')
#download = driver.get(href)
#print(type(download))

#driver.close()



#from selenium import webdriver
#
#download_dir = r"D:\Users\703143501\Downloads"
#chrome_options = webdriver.ChromeOptions()
#preferences = {"download.default_directory": download_dir ,
#               "directory_upgrade": True,
#               "safebrowsing.enabled": True }
#chrome_options.add_experimental_option("prefs", preferences)
#driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'/pathTo/chromedriver')
#
#driver.get("urlFileToDownload");
