   
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
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        print(os.getcwd())
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
        print(os.getcwd())
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/ca/data_raw')
        print(os.getcwd())

        #craft the photo =============================================
        image1 = Image.open(self.state_name.lower() + '_covid19_start_'+self.name_file+ '.png')
        print(image1.size)
        print('11111111111111111')
        width, height = image1.size
        numberOfSplits = 5
        splitDist = width / numberOfSplits

        x = 0
        y = 0
        w = splitDist+x
        h = height+y
        print(x, y, w, h)

        croppedImg = image1.crop((x,y,w,h))
        croppedImg.save(self.state_name.lower() + '_covid19_'+self.name_file+ '.png') #save to file

        #craft the photo #2=============================================
        image1 = Image.open(self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.png')
        print(image1.size)
        print('11111111111111111')
        width, height = image1.size
        numberOfSplits = 5
        splitDist = width / numberOfSplits

        x = 0
        y = 0
        w = splitDist+x
        h = height+y
        print(x, y, w, h)

        croppedImg = image1.crop((x,y,w,h))
        croppedImg.save(self.state_name.lower() + '_covid19_'+self.name_file+ '2nd.png') #save to file
        
        #read words from picture
        #import pytesseract
        img = cv2.imread(self.state_name.lower() + '_covid19_'+self.name_file+ '.png')
        text = pytesseract.image_to_string(img)
        print('3333333333333333333333333333', text)
        print('////////////////////////////////////////////')
        l_data= ''
        return l_data



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
        urllib.urlretrieve(urlData, f_n_total)
        urllib.urlretrieve(self.l_state_config[5][1], f_name)
        # step C: read data file and convert to standard file and save
        lst_raw_data = self.open4Xlsx(f_n_total)

        self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')



        csv_url = self.l_state_config[5][1]
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_day = c_tree.xpath('//hs/text()')
        print('----------', l_day)
        for l_date in l_day:
            print('*******************', l_date)
            if('Updates as of' in l_date):
                a_date = l_date.replace('Updates as of ', '').replace(' ', '').replace(',', '')
                print('  ....................a_date', a_date)
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break

        return(lst_raw_data, self.name_file, self.now_date)  


