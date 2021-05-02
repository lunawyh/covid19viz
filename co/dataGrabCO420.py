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
import urllib.request as urllib2
import itertools
#dataGrabWI327.py
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabCO(object):
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
    def saveWebsite(self, fRaw):

        csv_url = self.l_state_config[5][1]
        print('  download4Website', csv_url)
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(10)
        #'''
        driver.find_elements_by_link_text('Cases and deaths by county')[0].click()

        # to get the table
        html = requests.get(csv_url).content
        df_list = pd.read_html(html)
        df = df_list[-2]
        print('//////////////////', df)
        print(type(df))

        #type ==== <class 'pandas.core.frame.DataFrame'>
        #name
        state_name = df.iloc[:, 0].values.tolist()
        print('state_name;;;;;', state_name)

        #cases
        cases_li = df.iloc[:, 1].values.tolist()
        print('cases_li;;;;;', cases_li)

        #deaths
        death_li = df.iloc[:, 3].values.tolist()
        print('death_li;;;;;', death_li)
        d_list= []
        for ddd in death_li:
            if ddd == '*': d_list.append('0')
            else:
                d_list.append(ddd)

        #get the list together
        l_cases1 = np.vstack((state_name, cases_li, d_list)).T 
        print('l_cases1..........', l_cases1)
        
        return l_cases1

    
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
