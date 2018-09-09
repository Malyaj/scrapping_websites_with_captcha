# -*- coding: utf-8 -*-
""" Webscraping Assignment"""

from selenium import webdriver
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from bs4 import BeautifulSoup as bs

path_to_chromedriver = r"D:\chromedriver.exe"
download_dir = r"D:\Downloads"

base_url = "http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do"


def crop(image_path, crop_ratios, save_path):
    """
    function to crop image
    
    image_path: path of image to crop
    coords: tuple of x,y coordinates (x1, y1, x2, y2)
        origin (0,0) at the top-left corner
        x value increases towards the right
        y values increases towards dowbwards direction
    saved_location: path to save the cropped image
    """
    image_obj = Image.open(image_path)
    image_width, image_height = image_obj.size
    
    r1, r2, r3, r4 = crop_ratios
    
    coordinates = (int(image_width * r1),
                   int(image_height * r2),
                   int(image_width * r3),
                   int(image_height * r4)
                   )
    
    cropped_image = image_obj.crop(coordinates)
    cropped_image.save(save_path)
    #cropped_image.show()


preferences = {"download.default_directory": download_dir,
               "directory_upgrade": True,
               "safebrowsing.enabled": True
               }

chrome_options.add_experimental_option("prefs", preferences)
chrome_options = webdriver.ChromeOptions()

driver = webdriver.Chrome(chrome_options = chrome_options,
                          executable_path = path_to_chromedriver)

driver.get(base_url)
#size = driver.get_window_size()
#print("window size is {size}".format(size = size))
driver.save_screenshot('screenshot.png')

## crop the screenshot to isolate the captch
image_path = r"D:\EY_assignment\screenshot.png"
## crop ratios found out by iterative trials
crop_ratios = [0.575, 0.7, 0.75, 0.8]
save_path = "D:\EY_assignmnet\cropped.png"

# calling the crop function to crop the captcha
crop(image_path, crop_ratios, save_path)

## read the text from the captcha
captcha_image = Image.open(save_path)
captcha_image = captcha_image.convert("RGBA")
captcha_text = pytesseract.image_to_string(Image.open(captcha_image))

cin = "U45201RJ2012PTC038551"
cin_id="companyID"
cin_field = driver.find_element_by_id(cin_id)
cin_field.send_keys(cin)

captcha_id = "captcha"
captcha_field = driver.find_element_by_id(captcha_id)
captcha_field.send_keys(captcha_text)

#login_button_id is the if of the login button tag
login_button = driver.find_element_by_id(login_button_id)
login_button.click()

## logged into the portal
## write code to extract the details, format, and export to excel

driver.close()
