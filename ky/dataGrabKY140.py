   
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
import datetime 
from lxml import html
import requests
import PyPDF2
from datetime import date
import re 
import numpy as np

from selenium import webdriver  # https://selenium-python.readthedocs.io/installation.html
import time
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabKY(object):
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
        print('  download4Website', csv_url)

        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(7)

        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)

        caseNumbers = siteOpen.find_elements_by_xpath('//div[@class="external-html"]')
        #print('ccccccccccccccc', caseNumbers)
        #stateNames = siteOpen.find_elements_by_xpath('//div[@class="bc-row-label row-label chart-text label"]')
        case_list = []
        for case_num in caseNumbers: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append([dStringList[0], dStringList[8].replace(',', ''), dStringList[10].replace(',', '')])
        #print('llllllllllll', case_list)      

        case = 0
        death = 0
        for a_da in case_list:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(case_list, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        siteOpen.close()
        return l_cases3
    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            #self.open4pdf(name_file)
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'

            self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(urlData, self.name_file, str(today))  



