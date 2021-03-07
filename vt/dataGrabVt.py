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
import urllib.request
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time
import requests
from lxml import html
import numpy as np

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabVt(object):
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


    def saveWebsite(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  download4Website', csv_url)

        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(7)

        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        with open(fRaw, 'wb') as f:
            f.write(c_page.content)
        print('  saved to ', fRaw)

        iframe = siteOpen.find_element_by_xpath('//iframe[@id="ifrSafe"]')
        siteOpen.switch_to.frame(iframe)

        caseNumbers = siteOpen.find_elements_by_xpath('//div[@class="external-html"]')

        #print('++++++++++', caseNumbers)
        
        case_num_list = []
        for case_num in caseNumbers[1: 16]:  
            dStringList = case_num.text.split()
            print('  ------------case_num', dStringList )
            case_num_list.append([dStringList[0], dStringList[-1], 0])

        print('===============', case_num_list)
        death= 0
        case = 0
        for a_da in case_num_list:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(case_num_list, [['Total', case, death]], axis=0)
        #l_cases4 = l_cases3.tolist()
        print('00000000000000000000000', l_cases3)

        return l_cases3


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
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step B: parse and open
            lst_raw_data = self.saveWebsite(f_name)

            self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
            return(lst_raw_data, self.name_file, self.now_date)  

## end of file
