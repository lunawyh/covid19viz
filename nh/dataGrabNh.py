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
from pdfminer.high_level import extract_text

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

    def downloadAndParseLink(self,link_address,fRaw,o_Raw):
        #chrome_options1 = webdriver.ChromeOptions()
        #prefs = {'download.default_directory': 'C:\Dennis\Covid19\covid19viz\\nh\data_raw'}
        #chrome_options1.add_experimental_option('prefs', prefs)
        #siteOpen = webdriver.Chrome(chrome_options=chrome_options1)
        siteOpen = webdriver.Chrome()

        siteOpen.get(link_address)
        time.sleep(5)
        iframe = siteOpen.find_element_by_xpath("//iframe[@id='cases']")
        siteOpen.switch_to.frame(iframe)
        buttons = siteOpen.find_elements_by_css_selector("[role=button]")
        buttons[len(buttons)-2].click()
        time.sleep(1)
        buttons2 = siteOpen.find_elements_by_css_selector("button")
        buttons2[len(buttons2)-3].click()
        time.sleep(1)
        buttons3 = siteOpen.find_elements_by_css_selector("button")
        buttons3[len(buttons3)-1].click()
        time.sleep(4)
        linkclick = siteOpen.find_element_by_css_selector(".suppressClickBusting")
        linkclick.click()
        time.sleep(4)
        print('  pdf file is downloaded', o_Raw)
        print('  save raw data to', os.getcwd() + fRaw[1:])
        os.rename(o_Raw, os.getcwd() + fRaw[1:])

        #linkedPdf = PyPDF2.PdfFileReader(open(fRaw,'rb'))
        #print(str(linkedPdf.getNumPages()))
        #txtFile = str(linkedPdf.getPage(0).extractText().encode('utf8'))
        #print(txtFile)
        #with open("C:/Dennis/Covid19/covid19viz/nh/data_raw/mega.txt", "w") as f:
        #    f.write(txtFile)
        #    f.close()

        siteOpen.quit()  # close the window
        return []

    ## download a website
    def saveData(self, fRaw, sRaw, oRaw):
        page_url = self.l_state_config[5][1]
        print('  download4Website ...', page_url)
        nj_info = self.downloadAndParseLink(page_url,fRaw, oRaw)

        if(len(nj_info) < 1): return []
        with open(sRaw, 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for c in nj_info:
                wr.writerow(c)
            myfile.close()
        print('  saved to', sRaw)
        return nj_info

    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            o_name = self.get_download_path() + "/Map of Cumulative Positive Cases.pdf"
            s_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.saveData(f_name, s_name, o_name)
            print('  total list of cases', len(data_csv))
            return(data_csv, self.name_file, self.now_date)

## end of file
