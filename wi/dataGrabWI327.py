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
class dataGrabWI(object):
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
        #csv_url = self.l_state_config[5][1]
        #print('  download4Website', csv_url)

        csv_url = self.l_state_config[5][1]
        print('  download4Website', csv_url)
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(10)
        #'''
        #page 1
        County_names1 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names1: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases1 = [0] + case_list

        #page 2
        from selenium.webdriver.common.keys import Keys
        element = driver.find_elements_by_link_text('2')[0].click()
        print('clicked the botton ==============')
        time.sleep(5)
        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases2 = [0] + case_list

        #page 3
        element = driver.find_elements_by_link_text('3')[0].click()
        print('clicked the botton ==============')
        time.sleep(5)
        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases3 = [0] + case_list

        #page 4
        element = driver.find_elements_by_link_text('4')[0].click()
        print('clicked the botton ==============')
        time.sleep(5)
        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases4 = [0] + case_list

        #page 5
        element = driver.find_elements_by_link_text('5')[0].click()
        print('clicked the botton ==============')
        time.sleep(5)
        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases5 = [0] + case_list

        #page 6
        element = driver.find_elements_by_link_text('6')[0].click()
        print('clicked the botton ==============')
        time.sleep(5)
        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases6 = [0] + case_list

        #page 7
        element = driver.find_elements_by_link_text('7')[0].click()
        print('clicked the botton ==============')
        time.sleep(5)
        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases7 = [0] + case_list

        #page 8
        element = driver.find_elements_by_link_text('8')[0].click()
        #element[0].send_keys("\n")
        print('clicked the botton ==============')
        time.sleep(5)

        County_names2 = driver.find_elements_by_xpath('//td[@tabindex="-1"]')
        case_list = []
        for case_num in County_names2: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append(dStringList)
        l_cases8 = [0] + case_list  
        l_cases8 = l_cases8[:132]

        l_cases9 = l_cases1 +l_cases2 +l_cases3 +l_cases4 +l_cases5 +l_cases6 +l_cases7 +l_cases8
        l_cases10 = np.reshape(l_cases9, (len(l_cases9)//66, 66)).T
        print('lllllllllll', l_cases10)
        l_data = np.vstack((l_cases10[2], l_cases10[4], l_cases10[10])).T 
        print('lllllllllll', l_data)
        return l_data

    
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
