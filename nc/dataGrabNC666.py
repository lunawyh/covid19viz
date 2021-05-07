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
import PyPDF2
import pytesseract
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabnc(object):
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
        csv_url = 'https://covid19.ncdhhs.gov/dashboard/data-behind-dashboards'
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

	#1.....
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.pdf')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/County Cases and Deaths.pdf', '/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.pdf')

	#2.....
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.pdf')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/County Cases and Deaths (1).pdf', '/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '2nd.pdf')

	#3.....
        my_file = Path('/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '3rd.pdf')
        if my_file.is_file() == True:
            print('!!!!!! file already exsist')
        else:
            shutil.move('/home/lunawang/Downloads/County Cases and Deaths (2).pdf', '/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '3rd.pdf')
        
       
        #print(os.getcwd())
        os.chdir('/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw')
        #print(os.getcwd())



    

	
        #read words from picture--------------------------------------------------------------------------
        #import pytesseract
        f_name = (self.state_name.lower() + '_covid19_start_'+self.name_file+ '1st.pdf')
        
        # creating a pdf file object 
        pdfFileObj = open(f_name, 'rb') 
    
        # creating a pdf reader object 
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    
        # printing number of pages in pdf file 
        print(pdfReader.numPages) 
    
        # creating a page object 
        pageObj = pdfReader.getPage(0) 
    
        # extracting text from page 
        print(pageObj.extractText()) 
    
        # closing the pdf file object 
        pdfFileObj.close() 



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

