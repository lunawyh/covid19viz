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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabtn(object):
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
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        
        tree = html.fromstring(c_page.content)
        division = tree.xpath('//div//p//a')
        #print('IIIII', division)
        #print ("    HIHI", division)
        link = ''
        for l_data in division:
            if('Age by County' in l_data.text_content()):
                a_address = l_data.get('href')
                print('  find pdf at', l_data.get('href')) 
                link = 'https://www.tn.gov'+ a_address        
                print('  ____________________', link)
                break
        #print (' HJHJ', division)
        #link = "https://www.tn.gov" + link
        #print("  get link: " + link)
        return link


    ## paser data FL    
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.xlsx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): # not isfile(f_name) ): 
                a_address = self.open4Website(None)
                #rg_a_address = requests.get(a_address)
                #dt_obj = datetime.datetime.strptime(s_date, '%Y%m%d')
                #print('  updated on', dt_obj)
                #nums = int(n_start)
                #f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                if(not isfile(f_name) ):
                        result = self.download4Website(a_address, f_name)
                        print('  downloaded', result)
                else:
                        print('  already exiting')
            else: f_name = ''
            return f_name


    ## paser data FL
    def dataReadConfirmed(self, f_name):
        l_data = []
        if(isfile(f_name) ):
            df = pd.read_excel(f_name, engine='openpyxl')
            print('/////////////////////', df)
            #print('uuuuuuuuuuuuu', type(df))
            df2 = df['COUNTY'].values.tolist()
            #print('mmmmmmmmm', df2)
            df3 = df['CASE_COUNT'].values.tolist()
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
        state_machine = 100
        #print('______________', l_data_in)
        for a_row in l_data_in:
            if a_row [2] != 'Pending': continue
            #l_data_a = set(l_data_all) 
            if a_row[0] in l_data_all : 
                number += int(a_row[3])

            else:
                l_data_all.append([name, number, 0])
                name= ''
                number = 0
                name = (a_row[0])
                number = int(a_row[3])
        print('4444444444444444444444', l_data_all)
 
        return l_data_all   

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
