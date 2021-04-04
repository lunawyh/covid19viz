#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabRI.py
#
#	grab data from RI state websites
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
import time
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== 
# save downloaded data to daily or overal data
# class for dataGrfirstsDate = str(siteOpen.find_elements_by_xpath('//strong')[2].get_attribute('innerHTML').encode('utf8'))abRI
class dataGrabRI(object):

    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''
    ## save to csv

    def openSite(self, f_name, s_name,page_url):
        siteOpen = webdriver.Chrome()
        siteOpen.get(page_url)
        time.sleep(5)
        iframe = siteOpen.find_element_by_xpath("//iframe[@id='countyCasesIframe']")
        siteOpen.switch_to.frame(iframe)
        time.sleep(5)
        siteOpen.find_element_by_xpath("//select[@id='state-select']/option[@value='RI']").click()
        time.sleep(5)
        cases = siteOpen.find_element_by_xpath('//tbody["_ngcontent-qmx-c0"]')
        num_list = []
        for c in cases.find_elements_by_xpath("//tr"):
            num_sub = []
            for col in c.find_elements_by_xpath("//td"):
                num_list.append(str(col.get_attribute("innerHTML").encode('utf8')))
            break

        i = num_list.__len__()-1
        badchars = ['&lt;',',']
        while i>=0:
            for b in badchars:
                num_list[i] = num_list[i].replace(b, '')
            if i%5 ==0:
                num_list.pop(i)
            i = i - 1

        allList = []
        allList.append(['County', 'Cases', 'Deaths'])
        countyList = enumerate(['Providence','Kent','Washington','Newport','Bristol'])
        for n,c in countyList:
            allList.append([c,num_list[n*4],num_list[n*4 + 3]])

        return allList, siteOpen.page_source.encode('utf8')

    def save_data(self, f_name, s_name, data_csv, code):
        with open(f_name, 'w') as f:
            f.write(code)
            f.close()

        with open(s_name, 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for c in data_csv:
                wr.writerow(c)
            myfile.close()

        return data_csv

    ## paser data RI
    def parseData(self, name_target, date_target, type_download):
        self.name_file = name_target
        f_name = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_' + self.name_file + '.html'
        s_name = self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv'
        page_url = self.l_state_config[5][1]
        if (not os.path.isdir(self.state_dir + 'data_raw/')): os.mkdir(self.state_dir + 'data_raw/')
        # step A: downlowd and save
        data_csv, save = self.openSite(f_name, s_name, page_url)
        data_csv = self.save_data(f_name, s_name, data_csv, save)
        print('  total list of cases', len(data_csv))
        return (data_csv, self.name_file, self.now_date)
## end of file

