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

import pytesseract
from PIL import Image, ImageEnhance
import cv2
from pdfminer.high_level import extract_text


#from pdfminer.high_level import extract_text
import numpy as np
import pytesseract 
import cv2

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


    def downloadAndParseLink(self,link_address,fRaw,o_Raw,d_path):
        print(d_path)
        chrome_options1 = webdriver.ChromeOptions()
        prefs = {'download.default_directory': d_path}
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
        time.sleep(5)
        try:
            os.rename(o_Raw, fRaw)
        except WindowsError:
            os.remove(fRaw)
            os.rename(o_Raw, fRaw)
        siteOpen.close()

        datas = self.readDataFromPng(fRaw)

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
        text = ''
        crop_img = img[300:620, 260:560]
        crop_img = cv2.resize(crop_img, (0, 0), fx=5, fy=5)
        #filename = 'C:/Dennis/Covid19/covid19viz/nh/data_raw/savedImage.jpg'
        #cv2.imwrite(filename, crop_img)
        cv2.imshow("readDataFromPng", crop_img)
        key = cv2.waitKeyEx(1000)
        text = pytesseract.image_to_string(crop_img, config=custom_config).encode('utf8')
        #print("  readDataFromPng:",text)
        return text.splitlines()

    ## download a website
    def saveData(self, fRaw, sRaw, oRaw, dRaw):
        print(dRaw)
        page_url = self.l_state_config[5][1]
        print('  download4Website ...', page_url)
        alldata = self.downloadAndParseLink(page_url,fRaw, oRaw, dRaw)
        del alldata[5:8]

        allList = []
        countyList = ['Belknap','Carroll','Cheshire','Coos','Grafton','Hillsborough','Merrimack','Rockingham','Strafford','Sullivan','Unknown','Total']
        allList.append(['County','Cases', 'Deaths'])
        i=0
        for d in alldata:
            d1 = d.split(' ')

            try:
                while d1.index("|") != -1:
                    d1.remove("|")
            except:
                print("1")
            print(d1)

            j = 0
            for d2 in d1:
                #common replacement
                d2 = d2.replace(',','')
                d2 = d2.replace('s','')
                d1[j] = d2
                j = j + 1
                print(d2)

            dLength = len(d1)
            print(dLength)
            try:
                allList.append([countyList[i],d1[dLength-6],d1[dLength-2]])
            except:
                print("1")
            i = i + 1

            print(d1)

        with open(sRaw, 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for c in allList:
                wr.writerow(c)
            myfile.close()


        return allList


    

    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_' + self.name_file + '.png'
            d_path = os.path.abspath("nh\\data_raw\\")
            o_name = d_path + "\Map of Cumulative Positive Cases.png"
            s_name = self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.saveData(f_name, s_name, o_name, d_path)
            print('  total list of cases', len(data_csv))
            return(data_csv, self.name_file, self.now_date)

## end of file
