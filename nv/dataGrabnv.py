
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
        print('xlsx_name.....', xlsx_name)
        if xlsx_name is None:
            print("Error! A file exported from magicdraw is not found.")
            return
        sheet_xlsx_name = 'Tests, Cases, and Deaths'
        df = pd.read_excel(xlsx_name, sheet_name=sheet_xlsx_name)
        (n_rows, n_columns) = df.shape
        print("  excel_sheet_read", sheet_xlsx_name, df.shape)
        csv_data =[]
        for ii in range(n_rows):
            a_row = []
            for jj in range(n_columns):
                if str(df.iloc[ii, jj]) == "nan":
                    a_row.append("")
                else:
                    a_row.append(df.iloc[ii, jj])
            csv_data.append(a_row)
        print('data;;;;;;;;;;;;;;', csv_data)

        list_l = []
        for ccc in csv_data[2:]:
            list_l.append([ccc[0], ccc[2], ccc[3]])
        print('list.....', list_l)
        return list_l

    ## $^&&
    def open4excel(self, name_file):
        print("  open4Website")
        csv_url = self.l_state_config[5][1]
        print('data', csv_url)
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(25)

        my_file = Path("./nv/data_raw/"+self.state_name.lower() + '_covid19_'+self.name_file+ '.xlsx') #when under folders, use '.' to represent path
        if my_file.is_file() == True:
            print('!!!!!! file already exsist, for first')
        else:
            siteOpen.find_elements_by_link_text('Download Data')[0].click()
            print('click the button===========')
            #============================================
            #print(os.getcwd())

            shutil.move(self.get_download_path() + "/Nevada Dashboard Extract.xlsx", my_file)

        print('..........................................')

    def get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')


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


