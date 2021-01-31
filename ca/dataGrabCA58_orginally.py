   
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
        csv_url ='https://public.tableau.com/views/COVID-19CasesDashboard_15931020425010/Cases?:embed=y&:showVizHome=no'
        print('  #$$search website', csv_url)
        #webbrowser.open(csv_url, new=1)
        time.sleep(120)
        #print(os.getcwd())
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        print('no in is in the home file')
        print(os.getcwd())
        #move the files from download to data_raw
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Cases.png', '/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')
        
        my_file_2 = Path('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.png')
        if my_file_2.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Cases (1).png', '/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.png')
        
        #get back to start file
        #print(os.getcwd())
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw')
        #print(os.getcwd())

        #craft the photo =============================================
        image1 = Image.open(self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')
        #print(image1.size)
        width, height = image1.size
        numberOfSplits = 5
        splitDist = width / numberOfSplits

        x = 0
        y = 0
        w = splitDist+x
        h = height+y
        #print(x, y, w, h)

        croppedImg = image1.crop((x,y,w-80,h))
        croppedImg.save(self.state_name.lower() + '_covid19_'+self.name_file+ '.png') #save to file

        #craft the photo #2=============================================
        image1 = Image.open(self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.png')
        #print(image1.size)
        width, height = image1.size
        numberOfSplits = 5
        splitDist = width / numberOfSplits

        x = 0
        y = 0
        w = splitDist+x
        h = height+y
        #print(x, y, w, h)

        croppedImg = image1.crop((x,y,w-80,h))
        croppedImg.save(self.state_name.lower() + '_covid19_'+self.name_file+ '2nd.png') #save to file
        
        #read words from picture
        #import pytesseract
        img = cv2.imread(self.state_name.lower() + '_covid19_'+self.name_file+ '.png')
        text = pytesseract.image_to_string(img)
        #print('3333333333333333333333333333', text)
        img2 = cv2.imread(self.state_name.lower() + '_covid19_'+self.name_file+ '2nd.png')
        text_2nd = pytesseract.image_to_string(img2)
        #print('4444444444444444444444444444444', text_2nd)

        #now make data to list --------------------
        #find start word #1
        n_start_1st = text.find('Los Angeles')
        date_1st = text[n_start_1st:]
        l_pageTxt_1st = date_1st.split('\n')
        #print('333333333333333333333', l_pageTxt_1st)
        #find start word #2
        n_start_2st = text_2nd.find('Shasta')
        date_2st = text_2nd[n_start_2st:]
        l_pageTxt_2st = date_2st.split('\n')
        #print('44444444444444444444444', l_pageTxt_2st)
        l_pageTxt_together = l_pageTxt_1st+ l_pageTxt_2st
        #loop #1
        datas= []
        for stst in l_pageTxt_together:
            if stst == '': continue
            else:
                sdsd= stst.replace(' ', '').replace('\u2014', '').replace('#', '').replace('=', '').replace('+', '').replace('.', '').replace('|', '').replace('\u2018', '')
                sasa = [re.split('(\d.*)', pcode) for pcode in sdsd.split(' ')]
                #print('55555555555555555', sasa)
                datas.append(sasa)
        #print('&&&&&&&&&&&&&&', datas)
        list_data = datas[:2] +datas[3:41]+ datas[42:-1]
        #print('###############33', list_data)
        name_and_number = []
        for a_aa in list_data:
            if a_aa[0][0] =="Alpinemn" : continue
            elif a_aa[0][0] == 'DelNorteez': continue
            else:
                a_name = a_aa[0][0]
                a_number = a_aa[0][1].replace(',', '')
                name_and_number.append([a_name, a_number, 0])
        #print('(((((((((((((((((((', name_and_number)
        case = 0
        for a_da in name_and_number:
            case += int(a_da[1].replace(',', ''))
        l_cases3 = np.append(name_and_number, [['Total', case, 0]], axis=0)
        l_cases4 = np.append(l_cases3, [['County', 'Cases', 'Deaths']], axis=0)
        print('00000000000000000000000', l_cases4)
        l_data= ''
        os.chdir('..')
        os.chdir('..')
        print(os.getcwd())
        return l_cases4



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

