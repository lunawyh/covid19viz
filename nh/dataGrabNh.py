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
import requests
from lxml import html

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
#  Refer to https://pypi.org/project/pytesseract/
#       sudo add-apt-repository ppa:alex-p/tesseract-ocr-devel
#       sudo apt-get update
#
#       sudo apt install tesseract-ocr
#       sudo apt install libtesseract-dev
#
#       sudo pip install pytesseract==0.3.0
#      
import pytesseract
import cv2
#
#       sudo pip install pdfminer==20191010
#       sudo pip install pdfminer.six
from pdfminer.high_level import extract_text
import numpy as np


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
    ###def get_download_path(self):
        """Returns the default downloads path for linux or windows"""

    # page_url,f_data_raw, f_dl_name, s_dl_path
    def downloadAndParseLink(self,link_address,f_data_raw,f_dl_name,s_dl_path):
        print('  download to', s_dl_path, f_dl_name)
        chrome_options1 = webdriver.ChromeOptions()
        prefs = {'download.default_directory': s_dl_path}
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
        #linkclick = siteOpen.find_element_by_css_selector(".suppressClickBusting")
        #linkclick.click()
        #time.sleep(5)

        if os.name == 'nt':
            try:
                os.rename(f_dl_name, f_data_raw)
            except WindowsError:
                os.remove(f_data_raw)
                os.rename(f_dl_name, f_data_raw)
        else:
            os.rename(f_dl_name, f_data_raw)
        print('  saved to ', f_data_raw)
        siteOpen.close()

        datas = self.readDataFromPng(f_data_raw)

        siteOpen.quit()  # close the window
        return datas
    ## read data
    def readDataFromPng(self, f_namea):
        print('  B.readDataFromPng', f_namea)
        # step B: parse and open
        #---------------------------case-------------------------
        img = cv2.imread(f_namea)
        custom_config = r'--oem 3 --psm 6'
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
        #    print('in Windows, the path of tesseract_cmd is set')
        #else: # /usr/bin/tesseract /usr/local/bin/tesseract /usr/include/tesseract /snap/bin/tesseract /usr/share/man/man1/tesseract.1.gz
        #    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        text = ''
        crop_img = img[300:620, 260:560]
        crop_img = cv2.resize(crop_img, (0, 0), fx=5, fy=5)
        #filename = 'C:/Dennis/Covid19/covid19viz/nh/data_raw/savedImage.jpg'
        #cv2.imwrite(filename, crop_img)
        cv2.imshow("readDataFromPng", crop_img)
        key = cv2.waitKeyEx(3000)
        text = pytesseract.image_to_string(crop_img, config=custom_config).encode('utf8')
        #print("  readDataFromPng:",text.splitlines())
        return text.splitlines()

    ## download a website 
    def saveData(self, f_data_raw, f_data_name, f_dl_name, s_dl_path):
        print('  will saveData to ', f_data_raw)
        page_url = self.l_state_config[5][1]
        print('  download4Website ...', page_url)
        alldata = self.downloadAndParseLink(page_url,f_data_raw, f_dl_name, s_dl_path)
        del alldata[5:7]

        allList = []
        countyList = ['Belknap','Carroll','Cheshire','Coos','Grafton','Hillsborough','Merrimack','Rockingham','Strafford','Sullivan','Unknown','Total']
        allList.append(['County','Cases', 'Deaths'])
        i=0
        for d in alldata:
            #print('  saveData 0', d)
            d1 = d.split(' ')

            try:
                while d1.index("|") != -1:
                    d1.remove("|")
            except:
                pass
                #print('  saveData 1', "1")
            #print('  saveData 2', d1)

            j = 0
            for d2 in d1:
                #common replacement
                d2 = d2.replace(',','')
                d2 = d2.replace('s','')
                d1[j] = d2
                j = j + 1
                #print('  saveData 3', d2)

            dLength = len(d1)
            #print('  saveData 6'dLength)
            try:
                allList.append([countyList[i],d1[0],d1[dLength-2]])
            except:
                print('  saveData 4', "1")
            i = i + 1

            print('  saveData 5', d1)

        with open(f_data_name, 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for c in allList:
                wr.writerow(c)
            myfile.close()


        return allList

    ## save to csv
    def get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')


    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name_raw = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_' + self.name_file + '.png'
            if os.name == 'nt':
                dl_path = os.path.abspath("nh\\data_raw\\")
                dl_name = dl_path + "\Map of Cumulative Positive Cases.png"
            else:
                dl_path = self.get_download_path()
                dl_name = dl_path + "/Map of Cumulative Positive Cases.png"
            data_name = self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.saveData(f_name_raw, data_name, dl_name, dl_path)
            print('  total list of cases', len(data_csv))
            return(data_csv, self.name_file, self.now_date)

## end of file
