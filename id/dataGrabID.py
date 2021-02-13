#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabID.py
#
#	grab data from ID state websites
#
#

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
from __future__ import print_function
import os
from os.path import isfile, join
import csv
import urllib
import datetime 
from lxml import html
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pytesseract
import cv2
import time
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== 
# save downloaded data to daily or overal data 
# class for dataGrabID
class dataGrabID(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):
        # create a node
        print("welcome to dataGrabID")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.now_date = ''


    ## save to csv 
    def openSite(self, f_name, s_name, page_url,d_name):
        if os.path.exists(d_name) == False:
            chrome_options1 = webdriver.ChromeOptions()
            prefs = {'download.default_directory': f_name}
            chrome_options1.add_experimental_option('prefs', prefs)
            siteOpen = webdriver.Chrome(chrome_options=chrome_options1)
            siteOpen.get(page_url)

            while True:
                time.sleep(1)
                if siteOpen.find_elements_by_xpath("//iframe[@title='Data Visualization']") != []:
                    break

            iframe = siteOpen.find_element_by_xpath("//iframe[@title='Data Visualization']")
            siteOpen.switch_to.frame(iframe)
            while True:
                time.sleep(1)
                if siteOpen.find_elements_by_xpath("//div[@role='button']") != []:
                    break
            buttonslist = siteOpen.find_elements_by_xpath("//div[@role='button']")
            buttonslist[len(buttonslist)-2].click()
            while True:
                time.sleep(1)
                if siteOpen.find_elements_by_xpath("//button") != []:
                    break

            buttonslist2 = siteOpen.find_elements_by_xpath("//div[@role='button']")
            down_button = buttonslist2[len(buttonslist2) - 5]
            siteOpen.execute_script("document.getElementsByClassName('fppw03o low-density')[1].click()")

            time.sleep(5)
        
        
        #siteOpen.switch_to.window(siteOpen.window_handles[1])

        #time.sleep(1)
        #link = siteOpen.find_elements_by_xpath("//a[@class='csvLink_summary']")[
        # 0].get_attribute("href")
        #siteOpen.get(str(link))

            os.rename("C:\Dennis\Covid19\covid19viz\id\data_raw\County.png",d_name)
        cases,deaths,counties = self.readDataFromPng(d_name)
        return cases,deaths,counties

    def readDataFromPng(self, d_name):
        print('  B.readDataFromPng', d_name)
        # step B: parse and open
        #---------------------------case-------------------------
        img = cv2.imread(d_name)
        custom_config = r'--oem 3 --psm 6'
        if os.name == 'nt':
            pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
        text = ''
        crop_img = img[722:1612, 479:580]
        crop_img = cv2.resize(crop_img, (0, 0), fx=5, fy=5)
        crop_img = crop_img * (70/127 + 1) - 70
        key = cv2.waitKeyEx(3000)
        text1 = pytesseract.image_to_string(crop_img, config=custom_config).encode('utf8')
        print(text.splitlines())

        crop_img = img[722:1612, 866:967]
        crop_img = cv2.resize(crop_img, (0, 0), fx=5, fy=5)
        crop_img = crop_img * (100 / 127 + 1) - 100
        key = cv2.waitKeyEx(3000)
        text2 = pytesseract.image_to_string(crop_img, config=custom_config).encode('utf8')

        crop_img = img[722:1612, 71:180]
        crop_img = cv2.resize(crop_img, (0, 0), fx=5, fy=5)
        crop_img = crop_img * (100 / 127 + 1) - 100
        key = cv2.waitKeyEx(3000)
        text3 = pytesseract.image_to_string(crop_img, config=custom_config).encode('utf8')

        return text1,text2,text3

    def save_data(self, f_name, s_name, c,d,e):
        allList = []
        allList.append(['County', 'Cases', 'Deaths'])
        countyList = enumerate(e.splitlines())

        d = d.splitlines()
        c = c.splitlines()

        j = 0
        for cc in c:
            c[j] = cc.replace(",","")
            j = j+1

        d = list(filter(None, d))
        countyList = list(filter(None, countyList))
        c = list(filter(None, c))

        total_cases = 0
        total_deaths = 0

        for i,l in countyList:
            if i<44:
                allList.append([l,c[i],d[i]])
                total_cases = total_cases + int(c[i])
                total_deaths = total_deaths + int(d[i])
            else:
                break

        allList.append(["Total",str(total_cases),str(total_deaths)])


        with open(s_name,"wb") as f:
            wr = csv.writer(f)
            for c in allList:
                wr.writerow(c)
            f.close()

        return allList

    def parseData(self, name_target, date_target, type_download):
        self.name_file = name_target
        f_name = "C:\Dennis\Covid19\covid19viz\id\data_raw"
        s_name = self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv'
        d_name = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_' + \
                 self.name_file + '.png'
        page_url = self.l_state_config[5][1]
        if (not os.path.isdir(self.state_dir + 'data_raw/')): os.mkdir(self.state_dir + 'data_raw/')
        # step A: downlowd and save
        c,d,e = self.openSite(f_name, s_name, page_url, d_name)
        data_csv = self.save_data(f_name, s_name, c,d,e)
        print('  total list of cases', len(data_csv))
        return (data_csv, self.name_file, self.now_date)