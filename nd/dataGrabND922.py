#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabFl.py
#
#	grab data from FL state websites
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
import re
import requests
from lxml import html
import json
import numpy as np
from selenium import webdriver  # https://selenium-python.readthedocs.io/installation.html
import time
from selenium.webdriver.common.keys import Keys 
import bs4
from urllib2 import urlopen as uReq

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabND(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''

    ## save downloaded data to daily or overal data 
    def saveLatestDateUt(self, l_raw_data):
        #l_overall = []
        self.save2File(l_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        print ('GHJJ')
        return l_raw_data
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
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data

    ## download a website 
    def getUpdatedDate(self, page_content, fRaw):
        c_tree = html.fromstring(page_content)
        print('    look for updated date')
        se_dates = c_tree.xpath('//strong/text()')
        for se_data in se_dates:
            #print('  se_data', se_data)
            if('/' in se_data):
                print('      updated date', se_data)
                # update file name
                #print('      updated date from web', se_data)
                se_data=se_data.split(' ')[0]  # .replace('1 p.m.', '').replace(' ', '')
                print('      updated date', se_data)
                dt_obj = datetime.datetime.strptime(se_data, '%m/%d/%y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                f_name = self.state_dir + 'data_html/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
                return f_name, se_dates
        return fRaw, se_dates
    ## download a website 
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

        caseNumbers = siteOpen.find_elements_by_xpath('//div[@class="bc-bars"]')
        #stateNames = siteOpen.find_elements_by_xpath('//div[@class="bc-row-label row-label chart-text label"]')

        #print('++++++++++', caseNumbers)
        case_num_list = []
        for case_num in caseNumbers:  # this is cases------------------------------------bc-bar-inner dw-rect
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_num_list.append(dStringList)

        case_li = []
        death_li = []
        for a_line in case_num_list:
            if len(a_line) == 5:
                case_li.append(a_line[0])
                death_li.append(a_line[3])

        state_name_list = []
        caseNames = siteOpen.find_elements_by_xpath('//div[@class="bc-row-label row-label chart-text label"]')
        for state_nam in caseNames:  # this is names------------------------------------
            dStateName = state_nam.text # .split()
            #print('  -----------', dStateName )
            #unicodedata.normalize('NFKD', dStateName).encode('ascii', 'ignore')  # from unicode to ansi string
            #print(type(dStateName))
            state_name_list.append(dStateName)

        #state_name_list2 = state_name_list[1: ]
        l_data_case = np.vstack((state_name_list[1:], case_li, death_li)).T 

        print('  saveWebsite: read data ', len(l_data_case) )

        case = 0
        death = 0
        for a_da in l_data_case:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(l_data_case, [['Total', case, death]], axis=0)

        siteOpen.close()
        return l_cases3

    
    ## paser data Ut
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')

            # step A: downlowd and save
            lst_raw_data = self.saveWebsite(f_name)
            #print('2222222222', lst_raw_data)

            # step B: parse and open
            lst_data = self.saveLatestDateUt(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all



