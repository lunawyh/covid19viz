   
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
import ssl
from lxml import html
import requests
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import numpy as np
import datetime 
import time
import openpyxl
from openpyxl import load_workbook
from itertools import islice
import webbrowser
from pathlib import Path
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import re
from datetime import date

import pytesseract
print('????????????????????????//')


# ==============================
#================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabCA(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        print("need to use your hand click on 'Case and Mortality Summaries', then 'Download', then 'image' ")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.now_date = ''
        self.name_file = ''


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

    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):

        xl = pd.ExcelFile(xlsx_name)
        print('55555555555', xl.sheet_names)
        df1 = xl.parse('County Tiers and Metrics')

        f_nanm = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'

        df1.to_csv(f_nanm)

        import csv
        f_data =[]
        with open(f_nanm, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                #print('rrrrrrrrrrrrrrrrrrr', row)
                f_data.append(row)
        names= []
        cases= []
        for ff in f_data:
            if len(ff[0]) >= 20: continue
            if str(ff[0])== 'County': continue
            if str(ff[0])== '': continue
            elif len(ff) ==13 :
                names.append(ff[0])
                cases.append(ff[7])
        zeros= [0]*len(names)

        l_data = np.vstack((names, cases, zeros)).T
        print('777777777777', l_data)


        total_num = 0
        total_death = 0
        for a_ll in l_data:
            total_num += int(a_ll[1])

        l_cases3 = np.append(l_data, [['Total', total_num, total_death]], axis=0)
        print(';;;;;;;;;;;;;;;;', l_cases3)


        return l_cases3

    ## $^&&
    def open4excel(self, name_file):
        #csv_url = self.l_state_config[5][1]
        csv_url ='https://public.tableau.com/profile/ca.open.data#!/vizhome/COVID-19CasesDashboardv2_0/CaseStatistics'
        print('  #$$search website', csv_url)
        #webbrowser.open(csv_url, new=1)
        #time.sleep(20)
        #print(os.getcwd())
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        print('no in is in the home file')
        print(os.getcwd())
        #move the files from download to data_raw
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.pdf')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Case Statistics.pdf', '/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.pdf')
        
        my_file_2 = Path('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.pdf')
        if my_file_2.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Case Statistics (1).pdf', '/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.pdf')


        #get back to start file
        #print(os.getcwd())
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw')
        #print(os.getcwd())

        #craft the photo =============================================
        pdf_1st = (self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.pdf')
        pdf_2nd = (self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.pdf')
        print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))')
        import pdfplumber
        with pdfplumber.open(pdf_1st) as pdf:
            first_page = pdf.pages[0]
            print('llllllllllllllllllllllllllllllllllll')
            print(first_page.extract_text())


        zeros= [0]*len(l_pageTxt_number)
        l_data = np.vstack((l_pageTxt_name, l_number, zeros)).T 
        case = 0
        for a_da in l_data:
            case += int(a_da[1])
        l_cases3 = np.append(l_data, [['Total', case, 0]], axis=0)
        print('00000000000000000000000', l_cases3)

        os.chdir('..')
        os.chdir('..')
        print(os.getcwd())
        return l_cases3



    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
        self.name_file = name_file
        # step A: read date
        urlData = self.open4excel(name_file)
        #self.open4excel(name_file)
        # step B: save raw
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
        f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
        # 
        datassss= urlData.tolist()
        print('>>>>>>>>>>>>>>>>>>>>>.', datassss)
        self.save2File(datassss, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        print('save the data ------------------------------')
        today = (date.today())
        self.name_file = today.strftime('%Y%m%d')
        self.now_date = today.strftime('%m/%d/%Y')

        return(datassss, self.name_file, self.now_date)  


