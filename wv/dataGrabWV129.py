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
import numpy as np
import os
from selenium import webdriver
from time import sleep
import time
from datetime import date 
from datetime import timedelta 
#from gi.repository import Poppler, Gtk



# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabWV(object):
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
    ## parse from exel format to list 

    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//div//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('   dddd', l_dates)

        a_address = ''
        for l_date in l_dates:
            print(l_date.text_content())
            if('COVID-19 Daily Update ') in l_date.text_content(): 
                print('   sss', l_date)
                a_address =l_date.get('href')
                break
        print('11111111111111', a_address)
        return a_address

    ## paser data FL
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.aspx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): 
                a_address = self.open4Website(f_namea)

                if(a_address == ''): 
                    print ('    No address of downloading PDF is found')
                    return ('')

  
            return a_address

    ## paser data FL
    def dataReadConfirmed(self, f_name):
        # save html file

        siteOpen = webdriver.Chrome()
        siteOpen.get(f_name)
        time.sleep(7)
        c_page = requests.get(f_name)
        c_tree = html.fromstring(c_page.content)
      
        caseNumbers = siteOpen.find_elements_by_xpath('//div[@id="ctl00_PlaceHolderMain_ctl02__ControlWrapper_RichHtmlField"]')

        case_num_list = []
        for case_num in caseNumbers:  # this is cases------------------------------------bc-bar-inner dw-rect
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            if 'Virginia' in dStringList:
                print('  ------------case_num', dStringList )
                case_num_list=(dStringList)

        list_aaa = []
        list_ll = case_num_list[174:284]
        print('lllllllllll......', list_ll)
        for lll in list_ll:
            aaa = lll.replace('(', '').replace(')', '').replace(',', '').replace('.', '')
            list_aaa.append(aaa)

        print('aaaaaaaaaa......', list_aaa)


        l_cases2 = np.reshape(list_aaa, (len(list_aaa)//2, 2)).T
        print('ccccccccccccccc', l_cases2)
        cases= []
        for c_c in l_cases2[1]:
            c_d = c_c.replace('(', '').replace(')', '').replace(',', '').replace('.', '')
            cases.append(c_d)
        #print('333333333333', cases)
        zeros = [0] * len(l_cases2[0])
        l_data = np.vstack((l_cases2[0], cases, zeros)).T 

        print('ffffffffff', l_data)
        case = 0
        death = 0
        for a_da in l_data:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(l_data, [['Total', case, death]], axis=0)
        l_datas= []
        self.save2File(l_cases3, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        print('dddddddddddddddddd', l_cases3)
        return (l_cases3)

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #Step A download and save as raw html files
            f_targeta = self.dataDownload(name_target)
            if(f_targeta == ''): return ([], name_target, '')
            #Step B read confirmed cases
            l_d_sort = self.dataReadConfirmed(f_targeta)
            #Step C read death cases
        

            return(l_d_sort, self.name_file, self.now_date)  

## end of file
