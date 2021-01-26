#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabOh.py
#
#	grab data from OH state websites
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
import requests
from lxml import html
import zipfile
import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pathlib import Path
import shutil
from PIL import Image
import pytesseract

import matplotlib.pyplot as plt
import cv2
import re
import numpy as np
from datetime import date

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabNj(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        print("need to use your hand click on 'Case and Mortality Summaries', then 'Download', then 'image' ")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''
    ## save to csv

    ## $^&&
    def open4excel(self, name_file):
        #csv_url = self.l_state_config[5][1]
        csv_url ='https://njhealth.maps.arcgis.com/apps/MapSeries/index.html?appid=50c2c6af93364b4da9c0bf6327c04b45&amp;folderid=e5d6362c0f1f4f9684dc650f00741b24'
        print('  #$$search website', csv_url)
        #webbrowser.open(csv_url, new=1)
        #open time.sleep=================================================================
        #time.sleep(10)
        #print(os.getcwd())
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
        print('now it is in the home file')
        print(os.getcwd())
        #move the files from download to data_raw
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/nj/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Confirmed Cases.png', '/home/lunawang/Documents/luna2020/covid19viz/nj/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')

        
        #get back to start file
        #print(os.getcwd())
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/nj/data_raw')
        #print(os.getcwd())

        #craft the photo =============================================
        image1 = Image.open(self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')
        print(image1.size)
        width, height = image1.size
        numberOfSplits = 5
        splitDist = width / numberOfSplits

        x = 0
        y = 0
        w = splitDist+x
        h = height+y
        print(x, y, w, h)
    

        croppedImg = image1.crop((x,y,400,850))
        croppedImg.save(self.state_name.lower() + '_covid19_'+self.name_file+ '1st.png') #save to file

       
        #read words from picture--------------------------------------------------------------------------
        #import pytesseract
        img = cv2.imread(self.state_name.lower() + '_covid19_'+self.name_file+ '1st.png')
        text = pytesseract.image_to_string(img)
        print('111____________', text)
        
        #now make data to list --------------------
        n_start_1st = text.find('BERGEN')
        date_1st = text[n_start_1st:]
        l_pageTxt_1st = date_1st.split('\n')


        datas= []
        for stst in l_pageTxt_1st:
            if stst == '': continue
            elif stst == ' ': continue
            else:
                sdsd = stst.replace('j', '').replace('z', '').replace(' ', '').replace('.', '').replace('[', '').replace(']', '').replace('<', '').replace('is', '').replace('see', '').replace(',', '')
                #print('sdsd==================', sdsd)
                sasa = [re.split('(\d.*)', pcode) for pcode in sdsd.split(' ')]
                #print('55555555555-----------', sasa)
                datas += sasa[0]

        data_list = []
        for dada in datas:
            if dada == '' : continue
            else: 
                data_list.append(dada)

        l_cases2 = np.reshape(data_list, (len(data_list)/2, 2)).T
        zeros = [0]*len(l_cases2[0])
        l_data = np.vstack((l_cases2[0], l_cases2[1], zeros)).T 
        print('3333333333333333333333333333', l_data)

        final_list = []
        for adad in l_data:
            if 'MIDDLESEX' in adad[0]:
                final_list.append(['Middlesex', adad[1], 0])
            elif 'MORRIS' in adad[0]:
                final_list.append(['MORRIS', adad[1], 0])
            else:
                acac= adad[0][0] + adad[0][1:].lower()
                final_list.append([acac, adad[1], 0])

        print('44444444444444444444444', final_list)

        case = 0
        for a_da in final_list:
            case += int(a_da[1])
        l_cases3 = np.append(final_list, [['Total', case, 0]], axis=0)
        #l_cases4 = l_cases3.tolist()
        print('00000000000000000000000', l_cases3)

        os.chdir('..')
        os.chdir('..')
        print(os.getcwd())
        return l_cases3

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

    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
        self.name_file = name_file
        # step A: read date
        urlData = self.open4excel(name_file)
        #self.open4excel(name_file)
        # step B: save raw
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
        f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
        #urlData = urlData.tolist()
        self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        print('save the data ------------------------------')
        today = (date.today())
        self.name_file = today.strftime('%Y%m%d')
        self.now_date = today.strftime('%m/%d/%Y')

        return(urlData, self.name_file, self.now_date)  



## end of file
