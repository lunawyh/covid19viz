   
#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabTx.py
#
#	grab data from TX state websites
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
import urllib
import ssl
import datetime 
from lxml import html
import requests
import numpy as np
import urllib.request
import xlrd
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabLa(object):
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

    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  open4Website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_links = c_tree.xpath('//p//a')
        a_address = ''
        for l_data in l_links:      
            if('Data by Parish by Day' in l_data.text_content()):
                a_address = 'https://ldh.la.gov' + l_data.get('href')
                print('  find link at', a_address)
		
        return a_address

    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        l_data = []
        if(isfile(xlsx_name) ):
            #pandas.core.frame.DataFrame            
            df=pd.read_excel(xlsx_name, engine='openpyxl')
            print('/////////////////////', df)
            print('uuuuuuuuuuuuu', type(df))
            df2 = df['Parish'].values.tolist()
            #print('mmmmmmmmm', df2)
            df3 = df['Daily Negative Test Count'].values.tolist()
            #print('mmmmmmmmm', df3)
        
            l_cases3 = np.vstack((df2, df3, [0]*len(df3))).T 
        list1= []
        state_num = 0
        state_name = ''
        for a_lst in l_cases3:
            if state_name == '':
                state_name = a_lst[0]
                state_num= a_lst[1]
            elif a_lst[0] == state_name:
                state_name = a_lst[0]
                state_num= a_lst[1]
            elif a_lst[0] != state_name:
                list1.append([state_name, state_num, 0])
                state_num = 0
                state_name = ''
        print('mmmmmmmmmm', list1)

        
        return list1

    def saveLatestDateTx(self, l_raw_data, name_file):
        l_overall = []

        l_overall.append(['County', 'Cases', 'Deaths'])
        lst_raw_data6 = np.append(l_overall, l_raw_data, axis=0)

        self.save2File(lst_raw_data6, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return lst_raw_data6

    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            self.now_date = date_target
            # step A: read date
            urlData = self.open4Website(name_file)
            #self.open4excel(name_file)
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # 
            urllib.request.urlretrieve(urlData, f_n_total)
            urllib.request.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            lst_raw_data = self.open4Xlsx(f_n_total)

            lst_data = self.saveLatestDateTx(lst_raw_data, self.name_file)
            return(lst_data, self.name_file, self.now_date)  


