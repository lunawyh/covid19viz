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
#import StringIO
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pathlib import Path
import shutil
from PIL import Image
import pytesseract

import matplotlib.pyplot as plt
import cv2
import re
import numpy as np
from datetime import date

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabNj(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        print("need to use your hand click on 'Case and Mortality Summaries', then 'Download', then 'image' ")
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
   # page_url,f_data_raw, f_dl_name, s_dl_path
    def downloadAndParseLink(self,link_address):
        print('  download from', link_address)
        siteOpen = webdriver.Chrome()
        siteOpen.get(link_address)
        time.sleep(7)
        iframe = siteOpen.find_element_by_xpath('//iframe[@data-src="aHR0cHM6Ly9uamhlYWx0aC5tYXBzLmFyY2dpcy5jb20vYXBwcy9vcHNkYXNoYm9hcmQvaW5kZXguaHRtbA=="]')
        siteOpen.switch_to.frame(iframe)

        # <span style="" id="ember233" class="flex-horizontal feature-list-item ember-view">
        caseNumbers = siteOpen.find_elements_by_xpath('//span[@class="flex-horizontal feature-list-item ember-view"]')
        nambers_state = []
        for case_num in caseNumbers:  
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            nambers_state.append(dStringList)

        final_list= []
        for nst in nambers_state[2:]:
            #print('++++++++++', nst)
            if nst[0] == 'Cape':
                final_list.append([nst[0]+' '+ nst[1], nst[14].replace(',', ''), nst[7].replace(',', '')])
            else:
                final_list.append([nst[0], nst[13].replace(',', ''), nst[17].replace(',', '')])

        #print('===============', final_list)
        death= 0
        case = 0
        for a_da in final_list:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(final_list, [['Total', case, death]], axis=0)
        #l_cases4 = l_cases3.tolist()
        print('00000000000000000000000', l_cases3)

        
        time.sleep(4)
        return []
    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
        self.name_file = name_file
        page_url = self.l_state_config[5][1]
        # step A: downlowd and save
        data_csv = self.downloadAndParseLink(page_url)
        return(data_csv, self.name_file, self.now_date)
        
        # step A: read date
        urlData = self.open4excel(name_file)
        #self.open4excel(name_file)
        # step B: save raw
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
        f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
        #urlData = urlData.tolist()
        self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        print('save the data ------------------------------')
        today = (date.today())
        self.name_file = today.strftime('%Y%m%d')
        self.now_date = today.strftime('%m/%d/%Y')

        return(urlData, self.name_file, self.now_date)  


## end of file
