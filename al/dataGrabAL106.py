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

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabAL(object):
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
        #csv_url = self.l_state_config[5][1]
        #print('  download4Website', csv_url)
        #https://www.alreporter.com/mapping-coronavirus-in-alabama/

        csv_url = "https://dph1.adph.state.al.us/covid-19/"
        print('  download4Website', csv_url)
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(7)


        from pynput.mouse import Button, Controller
        mouse = Controller()
        print('mmmmmmmmmmmm', mouse.position)
        #mouse.move(-150, 300)
        mouse.position = (784, 431)
        print('moving ------', mouse.position)
        #time.sleep(5)
        mouse.click(Button.left, 1)
        time.sleep(4)

        caseName = siteOpen.find_elements_by_xpath('//td[@data-field="CNTYFIPS"]')
        #print('ccccccccccccccc', caseName)
        #stateNames = siteOpen.find_elements_by_xpath('//div[@class="bc-row-label row-label chart-text label"]')
        stateName_list = []
        for case_num in caseName: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            stateName_list.append(str(dStringList).replace('[', '').replace(']', '').replace("'", ''))
        print('nnnnnnnn', stateName_list)     
        print('dddddddddddddddds', len(stateName_list)) 

        caseNumbers = siteOpen.find_elements_by_xpath('//td[@data-field="CONFIRMED"]')
        #print('ccccccccccccccc', caseNumbers)
        #stateNames = siteOpen.find_elements_by_xpath('//div[@class="bc-row-label row-label chart-text label"]')
        stateCase_list = []
        for case_num in caseNumbers: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            stateCase_list.append(str(dStringList).replace('[', '').replace(']', '').replace("'", ''))
        print('ccccccccc', stateCase_list)  
        print('dddddddddddddddds', len(stateCase_list))

        caseDeath = siteOpen.find_elements_by_xpath('//td[@data-field="DIED"]')
        #print('ccccccccccccccc', caseDeath)
        #stateNames = siteOpen.find_elements_by_xpath('//div[@class="bc-row-label row-label chart-text label"]')
        stateDeath_list = []
        for case_num in caseDeath: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            stateDeath_list.append(str(dStringList).replace('[', '').replace(']', '').replace("'", ''))
        print('dddddddddddddddds', stateDeath_list) 
        print('dddddddddddddddds', len(stateDeath_list))


        l_data = np.vstack((stateName_list, stateCase_list, stateDeath_list)).T
        print('777777777777', l_data)

        total_num = 0
        total_death = 0
        for a_ll in l_data:
            total_num += int(a_ll[1])
            total_death += int(a_ll[2])

        l_cases3 = np.append(l_data, [['Total', total_num, total_death]], axis=0)
        print(';;;;;;;;;;;;;;;;', l_cases3)

        return l_cases3


    def flatten(self, l):
        try:
            return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
        except IndexError:
            return []

    
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



