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
import urllib.request
import numpy as np
from selenium import webdriver 
import time
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabwa(object):
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


    ## download a website 
    def download4Website(self, csv_url, fRaw):
        #csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.request.urlretrieve(csv_url, fRaw)
        return True


    ## paser data FL    
    def dataDownload(self, name_target):
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.xlsx'
        csv_url = 'https://www.doh.wa.gov/' + "/Portals/1/Documents/1600/coronavirus/data-tables/WA_COVID19_Cases_Hospitalizations_Deaths.xlsx"
    
        if(not isfile(f_name) ):
            result = self.download4Website(csv_url, f_name)
            print('  downloaded', result)
        else:
            print('  already exiting')
        print('/////////////////')
        return f_name


    ## paser data FL
    def dataReadConfirmed(self, f_name):
        l_data = []
        if(isfile(f_name) ):
            df = pd.read_excel(f_name, engine='openpyxl')
            print('/////////////////////', df)
            #print('uuuuuuuuuuuuu', type(df))
            df2 = df['County'].values.tolist()
            #print('mmmmmmmmm', df2)
            df3 = df['ConfirmedCases'].values.tolist()
            #print('mmmmmmmmm', df3)
            df4 =[0]* len(df2)
            l_cases3 = np.vstack([df2, df3, df4]).T 
            print(l_cases3)
            #l_data = self.parseDfData(df)
            #print('  l_data', l_data)

        return l_cases3                  
        
    def dataFilter(self, l_data_in)     :
        l_data_all = []
        l_cas_total = 0
        state_case = ''
        number= 0
        name=''

        #print('______________', l_data_in)
        for a_row in l_data_in:
            #print('jjjjjjjjjjjj', a_row)
            if l_data_all == []:
                #print('11111111111111', a_row)
                l_data_all.append(['first',0, 0])
                name = a_row[0]
                number= int(a_row[1])
            elif a_row[0] == name:
                #print('2222222222222', a_row)
                number += int(a_row[1])
            #elif a_row[0] != name:
            else:
                #print('3333333333333', a_row)
                l_data_all.append([name.replace(' County', ''), number, 0])
                name = a_row[0]
                number = int(a_row[1])
            #else:
                #print('function wrong')
        print('..........', l_data_all)


        total_num = 0
        total_death = 0
        for a_ll in l_data_all[1:]:
            total_num += int(a_ll[1])

        l_cases3 = np.append(l_data_all, [['Total', total_num, 0]], axis=0)
        print(';;;;;;;;;;;;;;;;', l_cases3)

        return l_cases3 

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
        print('hi--------------------')
        print(pd.__version__)
        self.name_file = name_target
        self.now_date = date_target
        #step A, download raw data
        f_target = self.dataDownload(name_target)
        if(f_target == ''): return ([], name_target, '')
        #step B, read data
        l_d_sort = self.dataReadConfirmed(f_target)
        #if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath(l_d_sort, pdfReader)
        #else: l_d_all = []
        # Step C: filter data
        l_data_all = self.dataFilter(l_d_sort)
        #l_data_find = self.gotTheData(l_data_all)
        return(l_data_all, self.name_file, self.now_date)  

## end of file
