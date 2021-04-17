
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
from datetime import date
import urllib.request
from selenium import webdriver 
import time
from pathlib import Path
import shutil

from openpyxl import Workbook
import openpyxl
import xlrd
from openpyxl import load_workbook

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabnv(object):
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


        return True

    ## save downloaded data to daily or overal data 
    def saveLatestDateTx(self, l_raw_data, name_file):
        l_cases2 = np.append( [['County', 'Cases', 'Deaths']],l_raw_data, axis=0)
        case= 0
        death = 0 
        for raw in l_raw_data:
            case += int(raw[1])
            death += int(raw[2])
        l_cases3 = np.append(l_cases2, [['Total', case, death]], axis=0)
        print ('  Total**********************88', l_cases3)
        self.save2File(l_cases3, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_cases3

    ## open a xlsx 
    def open4Xlsx(self, xlsx_name, fName=None):
        l_data = []

        #////////////////////////////////
        print('os.getcwd()...')
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/nv/data_raw/') 
        print(os.getcwd())
        #File_name = "/nv/data_raw/" +self.state_name.lower() + '_covid19_'+self.name_file+ '.xlsx'
        name_of_file = self.state_name.lower() + '_covid19_'+self.name_file+ '.xlsx'
        time.sleep(5)
        print('xlsx_name....', str(name_of_file))
        file_name = str(name_of_file)
        print('type of file name.....', type(file_name))
        wb = load_workbook(file_name) #(filename = str(name_of_file))
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        sheet_ranges = wb['range names']
        print(sheet_ranges['D18'].value)

        '''
        if(isfile(xlsx_name) ):
            df = pd.read_excel(xlsx_name, engine='openpyxl')
            print('/////////////////////', df)
            
            
            print('uuuuuuuuuuuuu', type(df))
            df2 = df['COUNTY_NAME'].values.tolist()
            print('mmmmmmmmm', df2)
            df3 = df['COVID_COUNT'].values.tolist()
            #print('mmmmmmmmm', df3)
            df4 = df['COVID_DEATHS'].values.tolist()
            l_cases3 = np.vstack([df2, df3, df4]).T 
        '''

        list1= []
        state_num = 0
        state_name = ''
        state_death = 0
        for a_lst in l_cases3:
            if state_name == '':
                state_name = a_lst[0]
                state_num= a_lst[1]
                state_death= a_lst[2]
            elif a_lst[0] == state_name:
                state_name = a_lst[0]
                state_num= a_lst[1]
                state_death= a_lst[2]
            elif a_lst[0] != state_name:
                list1.append([state_name, state_num, state_death])
                state_num = 0
                state_death= 0
                state_name = ''
        print('mmmmmmmmmm', list1)

        return list1

    ## $^&&
    def open4excel(self, name_file):
        print("  open4Website")
        csv_url = 'https://app.powerbigov.us/view?r=eyJrIjoiMjA2ZThiOWUtM2FlNS00MGY5LWFmYjUtNmQwNTQ3Nzg5N2I2IiwidCI6ImU0YTM0MGU2LWI4OWUtNGU2OC04ZWFhLTE1NDRkMjcwMzk4MCJ9'
        print('data', csv_url)
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(5)

        siteOpen.find_elements_by_link_text('Download Data')[0].click()
        print('click the button===========')
        #============================================
        #print(os.getcwd())
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        print('no in is in the home file')
        print(os.getcwd())
        print('to the start file')
        time.sleep(5)

        my_file = Path("/home/lunawang/Documents/luna2020/covid19viz/nv/data_raw/"+self.state_name.lower() + '_covid19_'+self.name_file+ '.xlsx')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Nevada Dashboard Extract.xlsx', "/home/lunawang/Documents/luna2020/covid19viz/nv/data_raw/"+self.state_name.lower() + '_covid19_'+self.name_file+ '.xlsx')

        #nv_covid19_20210416.xlsx
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/') 
        print('..........................................')

    


    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4excel(name_file)
            #self.open4excel(name_file)
            # step B: save raw
            '''
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # 
            urllib.request.urlretrieve(urlData, f_n_total)
            urllib.request.urlretrieve(self.l_state_config[5][1], f_name)
            '''
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            # step C: read data file and convert to standard file and save
            lst_raw_data = self.open4Xlsx(f_n_total)
            today = (date.today())
            self.name_file = today.strftime('%Y%m%d')
            self.now_date = today.strftime('%m/%d/%Y')

            lst_data = self.saveLatestDateTx(lst_raw_data, self.name_file)
            print(';;;;;;;;;;;;;;;;;;;;;', lst_data)
            return(lst_data, self.name_file, self.now_date)  

            # the end
## end of file


