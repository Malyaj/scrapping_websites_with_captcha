# -*- coding: utf-8 -*-
""" Webscraping Assignment"""

from selenium import webdriver
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np


path_to_chromedriver = r"D:\Anaconda3\chromedriver.exe"
download_dir = r"D:\Downloads"

base_url = "http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do"

preferences = {"download.default_directory": download_dir,
               "directory_upgrade": True,
               "safebrowsing.enabled": True
               }

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", preferences)


driver = webdriver.Chrome(chrome_options = chrome_options,
                          executable_path = path_to_chromedriver)


def crop(image_path, crop_ratios, save_path):
    """
    function to crop image
    
    image_path: path of image to crop
    crop_ratios: tuple of ratios in which image is to be cropped
        origin (0,0) at the top-left corner
        x value increases towards the right
        y values increases towards dowbwards direction
    saved_path: path to save the cropped image
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




driver.get(base_url)
#size = driver.get_window_size()
#print("window size is {size}".format(size = size))
driver.save_screenshot('screenshot.png')

## crop the screenshot to isolate the captch
image_path = r"D:\EY\screenshot.png"
## crop ratios found out by trial
crop_ratios = [0.575, 0.7, 0.75, 0.8]
save_path = r"D:\cropped.png"

crop(image_path, crop_ratios, save_path)

## read the text from the captcha
captcha_image = Image.open(save_path)
captcha_image = captcha_image.convert("RGBA")
#captcha_text = pytesseract.image_to_string(Image.open(captcha_image))
captcha_text = str(input("Enter Captcha: "))


cin = "U45201RJ2012PTC038551"
cin_id="companyID"
cin_field = driver.find_element_by_id(cin_id)
cin_field.send_keys(cin)

captcha_id = "userEnteredCaptcha"
captcha_field = driver.find_element_by_id(captcha_id)
captcha_field.send_keys(captcha_text)


login_button_id = "companyLLPMasterData_0"
login_button = driver.find_element_by_id(login_button_id)
login_button.click()


## logged into the portal
## write code to extract the details, format, and export to excel

#driver.close()

html = driver.page_source
soup = bs(html, 'lxml')



# description_list = []
description_list = ['CIN',
                    'Company Name',
                    'ROC Code',
                    'Registration Number',
                    'Company Category',
                    'Company SubCategory',
                    'Class of Company',
                    'Authorised Capital(Rs)',
                    'Paid up Capital(Rs)',
                    'Number of Members(Applicable in case of company without Share Capital)',
                    'Date of Incorporation',
                    'Registered Address',
                    'Address other than R/o where all or any books of account and papers are maintained',
                    'Email Id',
                    'Whether Listed or not',
                    'Suspended at stock exchange',
                    'Date of last AGM',
                    'Date of Balance Sheet',
                    'Company Status(for efiling)',
                    ]

def extract_LLP_Master_Data(description_list, soup, tag_id = 'resultTab1'):
    """
    Extract the html table and return as pandas dataframe
    """
    table = soup.find('table', {'id' : tag_id})
    all_rows = table.find_all('tr')
    
    value_list = []
    for row in all_rows:
        cols = row.find_all('td')
        value_list.append(cols[1].text)
    
    df = pd.DataFrame({'description' : description_list,
                       'value' : value_list})
    return df


charges_headers = ['Assets under charge', 
                   'Charge Amount',
                   'Date of Creation', 
                   'Date of Modification',
                   'Status',
                   ]

def extract_charges(headers, soup, tag_id = 'resultTab5' ):
    values = []
    
    table = soup.find('table', {'id' : tag_id})
    
    all_rows = table.find_all('tr')
    rows_except_headers = all_rows[1:]
    
    if len(rows_except_headers) == 1:
        ## no data in table i.e No Charges Exists for Company/LLP
        #df = pd.DataFrame(np.array())
        pass
    else:
        for each_row in rows_except_headers:
            sublist = [x.text for x in each_row.find_all('td')]
            values.extend(sublist)
    
    no_of_columns = 5
    no_of_rows = int(len(values) / no_of_columns)
    
    df = pd.DataFrame(np.array(values).reshape(no_of_rows, no_of_columns),
                      columns = headers)
    return df
    
    
directors_headers = ["DIN/PAN",
                     "Name",
                     "Begin date",
                     "End date",
                     "Surrendered DIN",
                     ]


def extract_directors(headers, soup, tag_id = 'resultTab6'):
    ## similarly extract directors data as well
    ## return as dataframe
    pass


path_to_excel_file = r"D:\Users\703143501\Documents\Genpact Internal\EY\output.xls"

first_table = extract_LLP_Master_Data(description_list, soup)
first_table.to_excel(path_to_excel_file, index = False)
#second_table = extract_charges(charges_headers, soup, 'resultTab5')
#third_table = extract_directors(directors_headers, soup, 'resultTab6')

### combine the three table in a single dataframe
### export to excel, currently doing for the first table only

driver.close()
print("Scraping finished")
