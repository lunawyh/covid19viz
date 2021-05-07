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
import re
import requests
from lxml import html
import json
import numpy as np
from selenium import webdriver  
import time
from selenium.webdriver.common.keys import Keys 
import urllib.request as urllib2
import itertools
import pyautogui
from pathlib import Path
from PIL import Image
import cv2
import pytesseract
#dataGrabWI327.py
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabHI(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''

    ## save downloaded data to daily or overal data 
    def saveLatestDateUt(self, l_raw_data):
        #l_overall = []
        self.save2File(l_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        print ('GHJJ')
        return l_raw_data
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
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data


    ## download a website 
    def saveWebsite(self, fRaw):
        #csv_url = self.l_state_config[5][1]
        #print('  download4Website', csv_url)
        my_file = Path('./hi/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:


            csv_url = self.l_state_config[5][1]
            print('  download4Website', csv_url)
            driver = webdriver.Chrome()
            driver.get(csv_url)
            time.sleep(5)

            element = driver.find_elements_by_link_text('Cases')[0].click()
            print('click to the element page...........')
            time.sleep(5)
        
            poto = self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png'
            ####
            print(os.getcwd())
            print('cccccccccccccccccccc')
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save('./hi/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png') #\home\lunawang\Documents\luna2020\covid19viz
            print('save the screenshot.............')

        ##................2
        image1 = Image.open('./hi/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.png')
        print(')))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))')


        ## ............3
        my_file = Path('./hi/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '.png')
        if my_file.is_file() == True:
            print('!!!!!! file 2nd already exsist')
        else:
            # FOR THE NUMBERS OF THE COUNTRY
            print(image1.size)
            width, height = image1.size
            numberOfSplits = 5
            splitDist = width / numberOfSplits

            x = 0
            y = 0
            w = splitDist
            h = height+y
            print(x, y, w, h)
            #croppedImg = image1.crop((x+640,y+750,1500,h+300))
            croppedImg = image1.crop((x+640,y+750,820,h+600))
            croppedImg.save('./hi/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '.png') 
            print('save the photo craft')

        ## .....3
        img = cv2.imread('./hi/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '.png')
        text = pytesseract.image_to_string(img, config='--psm 6')
        #print('111____________', text)
        test_l = text.split('\n')
        test_ll = test_l[4:8]
        #print('lll...', test_ll)


        number_li = []
        name_li = []
        for aaa in test_ll: 
            bbb = aaa.split(' ')
            name_li.append(bbb[0])
            if len(bbb[1]) == 4:
                number_li.append(bbb[1][1: ])
            else:
                number_li.append(bbb[1].replace('[', '').replace(',', '').replace("'", '').replace("-", '').replace("f", '').replace("j", '').replace(".", '').replace("|", ''))
        print('nnnnnnnn..........', name_li)
        print('nnnnnnnn..........', number_li)
        #print('first one ===============')

        ## ............4
        my_file = Path('./hi/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '_total_confirmed_cases.png')
        if my_file.is_file() == True:
            print('!!!!!! file 2nd already exsist')
        else:
            # FOR THE TOTAL NUMBER TOGETHER
            # FOR THE NUMBERS OF THE COUNTRY
            print('image_size..........', image1.size)
            width, height = image1.size
            numberOfSplits = 5
            splitDist1 = width / numberOfSplits

            x = 0
            y = 0
            w = splitDist1
            h = height+y
            print('image_size..........',x, y, w, h)
            #croppedImg =image1.crop((x+60,y+250,350,h+300))
            croppedImg = image1.crop((50, 250, 350, 500))
            croppedImg.save('./hi/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '_total_confirmed_cases.png') 
            print('save the photo craft')

        ## .....3 ) because there is no data for the 'Kalawao' county, we nee to find the 
        # total cases, then minues it by the other four county cases
        img2 = cv2.imread('./hi/data_raw/' + self.state_name.lower() + '_covid19_'+self.name_file+ '_total_confirmed_cases.png')
        text2 = pytesseract.image_to_string(img2, config='--psm 6')
        print('222____________', text2)
        test_l = text2.split('\n')
        
        test_ll = test_l[2].replace(',', '')
        print(test_ll)

        name_li.append('Kalawao')
        number_li.append(test_ll)
        zeros = len(name_li) *[0]
        l_data = np.vstack((name_li, number_li, zeros)).T 
        print('lllllllllll', l_data)
                
        case = 0
        death = 0
        for a_da in l_data:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(l_data, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        driver.close()

        return l_cases3

    
    ## paser data Ut
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')

            # step A: downlowd and save
            lst_raw_data = self.saveWebsite(f_name)
            #print('2222222222', lst_raw_data)

            # step B: parse and open
            lst_data = self.saveLatestDateUt(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all
