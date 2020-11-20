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
import ssl
import PyPDF2
import re
import requests
from lxml import html
import numpy as np
from PIL import Image
import webbrowser
import cv2
import imgkit
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import autopy
import pyautogui
import subprocess
import webbrowser as vb

import tempfile
import urlparse
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
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        #print('parseDfData', df.title)
        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )
                    continue
                a_case.append( df.iloc[ii, jj] )
            lst_data.append( a_case )
        # save to a database file
        if(fName is not None): self.save2File( lst_data, fName )
        return lst_data
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data

    ## download a website 
    def download4Website(self, csv_url, fRaw):
        #csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        print('   dddd', l_dates)


        today = date.today()
        print("Today is: ", today) 
        datall = ''
        # Yesterday date 
        yesterday = today - timedelta(days = 1) 
        print("Yesterday was: ", yesterday) 

        dt_obj = str(yesterday) 
        print("++++++++++++++ ", dt_obj) 
        print("++++++++++++++ ", type(dt_obj))

        dt_obj = datetime.datetime.strptime(dt_obj, '%Y-%m-%d')
        datall = dt_obj.strftime('%m-%d-%Y')

        print('ddddddddddddddd', datall)
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('COVID-19 Daily Update ' + datall[:2]) in l_date.text_content(): 
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
      

        caseNumbers = siteOpen.find_elements_by_xpath('//font[@size="3"]')

        case_num_list = []
        for case_num in caseNumbers:  # this is cases------------------------------------bc-bar-inner dw-rect
            dStringList = case_num.text.split()
            print('  ------------case_num', dStringList )
            case_num_list.append(dStringList)


        l_cases2 = np.reshape(case_num_list[16][3:], (len(case_num_list[16][3:])/2, 2)).T
        #print('22222222222222222', l_cases2)
        cases= []
        for c_c in l_cases2[1]:
            #print('555555555555555555', (c_c))

            c_d = c_c.replace('(', '').replace(')', '').replace(',', '').replace('.', '')

            #print('^^^^^^^^^^^^^^^^^^^^^6', c_d)
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
        print('dddddddddddddddddd', l_cases3)


        l_datas= []
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
