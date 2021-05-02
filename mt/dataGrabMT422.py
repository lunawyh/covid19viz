  
#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabTx.py
#
#	grab data from TX state websites
#
#	dataGrabMT422.py
#	map-of-montana.jpg

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
class dataGrabMT(object):
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
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(10)

        from selenium.webdriver.common.keys import Keys
        element = driver.find_elements_by_xpath('//button[@aria-label="Go to entry 2: COVID-19 Cases"]') #[0].click()
        print('...................')
        element[0].send_keys("\n")
        print('clicked the botton ==============')

        time.sleep(20)

        iframe = driver.find_element_by_xpath('//iframe[@src="https://experience.arcgis.com/experience/b5272da8fbd04258a18720065b21f8c2"]')
        driver.switch_to.frame(iframe)
        print('..................')

        iframe = driver.find_element_by_xpath('//iframe[@src="https://montana.maps.arcgis.com/apps/opsdashboard/index.html#/6a55cf30ec4e4a65a682021b7db3dd91"]')
        driver.switch_to.frame(iframe)
        print('..................')

        state_name = driver.find_elements_by_xpath('//span[@style="font-size:14px"]')
        #print('ccccccccccccccc', state_name)
        full_list = []
        for case_num in state_name: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            full_list.append(dStringList)    

        state_name = []
        state_case = []
        for ccc in full_list:
            if len(ccc) == 3:
                state_name.append(ccc[0])
            elif len(ccc) == 4:
                name = ccc[0] + ' '+ ccc[1]
                state_name.append(name)
            elif 'Lewis' == ccc[0]:
                name = ccc[0] + ' '+ ccc[1] + ' '+ ccc[2] 
                state_name.append(name)
            else:
                state_case.append(ccc[0].replace(',', ''))
        print('name.....', state_name)
        print('name.....', len(state_name))
        print('case.....', state_case)
        print('case.....', len(state_case))

        zeros= [0]*len(state_case)
        l_data = np.vstack((state_name, state_case, zeros)).T
        print('final list......', l_data)

        case = 0
        death = 0
        for a_da in l_data:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(l_data, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        driver.close()
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




