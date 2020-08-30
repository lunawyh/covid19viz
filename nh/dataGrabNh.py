#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabOh.py
#
#	grab data from OH state websites
#
#

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
from __future__ import print_function
import os
from os.path import isfile, join
import pandas as pd
import csv
import datetime
import urllib
import ssl
import requests
from lxml import html
import zipfile
import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import PyPDF2
<<<<<<< HEAD
import pytesseract
from PIL import Image, ImageEnhance
import cv2
from pdfminer.high_level import extract_text

=======
#from pdfminer.high_level import extract_text
import numpy as np
import pytesseract 
import cv2
>>>>>>> a05e568f17e0b8f0ecef36412d2e479fe5d10eaa
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabNh(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''
    ## save to csv 
    def save2File(self, l_data, csv_name):
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        # make sure the 1st row is colum names
        if('County' in str(l_data[0][0])): pass
        else: csvwriter.writerow(['County', 'Cases', 'Deaths'])
        for a_row in l_data:
            csvwriter.writerow(a_row)
        csv_data_f.close()
        print('  save2File', csv_name)
    ## save downloaded data to daily or overal data 
    def saveLatestDate(self, l_raw_data, fname):
        l_overall = []
        
        l_overall.append(['County', 'Cases', 'Deaths'])
        total_case = 0
        total_death = 0
        for a_item in l_raw_data:
            l_overall.append(a_item)
            total_case += int(a_item[1])
            total_death += int(a_item[2])
        l_overall.append(['Total', total_case, total_death])
        self.save2File(l_overall, fname)
        return l_overall
    ## save to csv
    ###def get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        """if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')"""

    def downloadAndParseLink(self,link_address,fRaw,o_Raw):
        chrome_options1 = webdriver.ChromeOptions()
        prefs = {'download.default_directory': 'C:\Dennis\Covid19\covid19viz\\nh\data_raw'}
        chrome_options1.add_experimental_option('prefs', prefs)
        siteOpen = webdriver.Chrome(chrome_options=chrome_options1)

        siteOpen.get(link_address)
        time.sleep(5)
        iframe = siteOpen.find_element_by_xpath("//iframe[@id='cases']")
        siteOpen.switch_to.frame(iframe)
        buttons = siteOpen.find_elements_by_css_selector("[role=button]")
        buttons[len(buttons) - 2].click()
        time.sleep(1)
        buttons2 = siteOpen.find_elements_by_css_selector("button")
        buttons2[len(buttons2) - 6].click()
        time.sleep(4)
        linkclick = siteOpen.find_element_by_css_selector(".suppressClickBusting")
        linkclick.click()
        time.sleep(4)
        try:
            os.rename(o_Raw, fRaw)
        except WindowsError:
            os.remove(fRaw)
            os.rename(o_Raw, fRaw)
        siteOpen.close()

        i = 0
        j=0
        im = Image.open(fRaw).convert('L')
        while i < 2:
            while j < 2:
                left = 265 + (200 * i)
                right = 310 + (190 * i)
                top = 300 + (150 * j)
                bottom = 450 + (150 * j)
                im1 = im.crop((left, top, right, bottom))
                im1 = im1.resize((2 * (right-left),2 * (bottom-top)),Image.ANTIALIAS)
                im1 = im1.resize((4 * (right-left), 4 * (bottom-top)), Image.ANTIALIAS)
                im1 = im1.resize((6 * (right - left), 6 * (bottom - top)), Image.ANTIALIAS)
                enhancer = ImageEnhance.Contrast(im1)
                enhancer.enhance(2000000)
                im1.show()
                im1.save("C:/Dennis/Covid19/covid19viz/nh/data_raw/img" + str(i+j+1) + ".png", "PNG")

                pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
                text = pytesseract.image_to_string(im1,  config='-c tessedit_char_whitelist=0123456789').encode('utf8')
                with open("C:/Dennis/Covid19/covid19viz/nh/data_raw/out" + str(i+j+1) + ".txt", 'w') as f:
                    f.write(text)
                    f.close()
                j = j+1
            i = i + 1

        siteOpen.quit()  # close the window
        return os.getcwd() + fRaw[1:]
    ## read data
    def readDataFromPng(self, f_namea):
        print('  B.readDataFromPng', f_namea)
        # step B: parse and open
        #---------------------------case-------------------------
        img = cv2.imread(f_namea)
        delay = 0
        while(delay < 10):
            crop_img = img[300:620, 0:560]  # from 1080x650
            cv2.imshow("readDataFromPng", crop_img)
            key = cv2.waitKeyEx(1000)
            if(key == 27 or key == 1048603):
                break
            delay += 1
 
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(crop_img, config=custom_config)
 
        print("  readDataFromPng:",text) 
        return []

    ## download a website
    def saveData(self, fRaw, sRaw, oRaw):
        page_url = self.l_state_config[5][1]
        print('  download4Website ...', page_url)
        if(not isfile(fRaw) ):
            fRaw = self.downloadAndParseLink(page_url,fRaw, oRaw)
        #scan and detect text	
        fRaw = './nh/data_raw/nh_covid19_20200830.png'
        data_info = self.readDataFromPng(fRaw)	

        if(len(data_info) < 1): return []
        data_csv = self.saveLatestDate(data_info, sRaw)
        
        return data_csv

    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_' + self.name_file + '.png'
            d_path = 'C:/Dennis/Covid19/covid19viz/nh/data_raw'
            o_name = d_path + "/Map of Cumulative Positive Cases.png"
            s_name = self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.saveData(f_name, s_name, o_name)
            print('  total list of cases', len(data_csv))
            return(data_csv, self.name_file, self.now_date)

## end of file
