#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabFl.py
#
#	grab data from FL state websites
#
#inspect

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
from selenium.webdriver.chrome.options import Options
import shutil
import os
from pathlib import Path

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabMO(object):
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
        print('$$$$$$$$$$$$$$$$$$$$$$', l_data)

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
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(5)
        driver.find_element_by_id("btnUSTableExport").click()
        print(os.getcwd())

        #os.chdir("../covid19viz")
        #os.chdir("../luna2020")
        #os.chdir("../Documents")
        #os.chdir("../home")
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        print('no in is in the home file')
        print(os.getcwd())

        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/mo/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '.csv')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/united_states_covid19_cases_and_deaths_by_state.csv', '/home/lunawang/Documents/luna2020/covid19viz/mo/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '.csv')

        print(os.getcwd())

        os.chdir('/home/lunawang/Documents/luna2020/covid19viz')
        print(os.getcwd())

        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
        l_data = self.open4File(f_name)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        #l_cases3 = []
        return l_data

    ## open a csv
    def open4File(self, csv_name):
        l_datas = []
        if(isfile(csv_name) ):
            with open(csv_name,'rt')as f:
                  data = csv.reader(f)
                  for row in data:
                      #print(row)
                      l_datas.append(row)
        else: return []
        #prase data
        l_name=[]
        l_cases=[]
        l_deaths=[]
        for a_row in l_datas[4:-1]:
            l_name.append(a_row[0])
            l_cases.append(a_row[1])
            if a_row[7] == 'null':
                l_deaths.append(0)
            else: l_deaths.append(a_row[7])
        l_data = np.vstack((l_name, l_cases, l_deaths)).T 

        case = 0
        death = 0
        for a_da in l_data:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(l_data, [['Total', case, death]], axis=0)

        print('2222222222222', l_cases3)
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

