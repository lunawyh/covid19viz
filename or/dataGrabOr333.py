   
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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabOR(object):
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


    ## $^&&
    def open4pdf(self, name_file):
        csv_url = self.l_state_config[5][1]
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
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/or/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/Daily Data Update.png', '/home/lunawang/Documents/luna2020/covid19viz/or/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png')
        
       
        #print(os.getcwd())
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/or/data_raw')
        #print(os.getcwd())

        #craft the photo =============================================
        image1 = Image.open(self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png')
        print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))')
        print(image1.size)
        width, height = image1.size
        numberOfSplits = 5
        splitDist = width / numberOfSplits

        x = 0
        y = 0
        w = splitDist
        h = height+y
        print(x, y, w, h)

        croppedImg = image1.crop((x,890,1099,h-130))
        croppedImg.save(self.state_name.lower() + '_covid19_'+self.name_file+ '1st.png') #save to file
    
        
        #read words from picture--------------------------------------------------------------------------
        #import pytesseract
        img = cv2.imread(self.state_name.lower() + '_covid19_'+self.name_file+ '1st.png')
        text = pytesseract.image_to_string(img, config='--psm 6')
        print('111____________', text)

        #now make data to list --------------------
        n_start_1st = text.find('Baker')
        date_1st = text[n_start_1st:]
        l_pageTxt_1st = date_1st.split('\n')
        print('11111111111111111111', l_pageTxt_1st)
        #find start word #2

        datas= []
        for sasa in l_pageTxt_1st[:-1]:
            sdsd= sasa.split(' ')
            print('sdsd-----------------', sdsd)
            datas.append([sdsd[0], sdsd[-2].replace(',', ''), sdsd[-1].replace(',', '')])
        print('----------datas', datas)


        case = 0
        for a_da in datas:
            case += int(a_da[1])
        l_cases3 = np.append(datas, [['Total', case, 0]], axis=0)
        print('00000000000000000000000', l_cases3)

        os.chdir('..')
        os.chdir('..')
        print(os.getcwd())
        return l_cases3


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
        print('  save2File', csv_name)

    ## paser data or
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.cvs'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv') 
            #urllib.urlretrieve(urlData, f_n_total)
            #urllib.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            #self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(urlData, self.name_file, str(today))  
