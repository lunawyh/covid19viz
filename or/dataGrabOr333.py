   
#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabTx.py
#
#	grab data from TX state websites
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
import urllib
import ssl
from lxml import html
import requests
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import numpy as np
import datetime 
import time
import openpyxl
from openpyxl import load_workbook
from itertools import islice
import webbrowser
from pathlib import Path
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import re
from datetime import date

import pytesseract
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabOR(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config


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


    ## $^&&
    def open4pdf(self, name_file):
        csv_url = self.l_state_config[5][1]
        print(os.getcwd())
        #
        '''
        siteOpen = webdriver.Chrome() #chrome_options=chrome_options)
        siteOpen.get(csv_url)
        time.sleep(7)

        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)

        f_name ="C:\Dennis\Covid19\covid19viz\id\data_raw"

        chrome_options1 = webdriver.ChromeOptions()
        prefs = {'download.default_directory': f_name}
        chrome_options1.add_experimental_option('prefs', prefs)
        siteOpen = webdriver.Chrome(chrome_options=chrome_options1)
        siteOpen.get(csv_url)

        buttonslist2 = siteOpen.find_elements_by_xpath('//div[@role="button"]')
        print('bbbbbbbbbbbbbbbbbb', buttonslist2)
        down_button = buttonslist2[len(buttonslist2) - 5]
        siteOpen.execute_script("document.getElementsByClassName('tabToolbarButton tab-widget download').click()")
        #class="tabToolbarButton tab-widget download"
        time.sleep(5)
        '''

        driver = webdriver.Chrome()
        driver.get(csv_url)
        button= driver.find_element_by_xpath("//div[@role='button']") 
        print('111111111111111111111', button)
        button = driver.find_element_by_id('class="tabToolbarButtonImg tab-icon-download"')
        button.click()
        return l_cases3

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

    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.cvs'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv') 
            #urllib.urlretrieve(urlData, f_n_total)
            #urllib.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            #self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(urlData, self.name_file, str(today))  
