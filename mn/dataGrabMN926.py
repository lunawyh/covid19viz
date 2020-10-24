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
import ssl
import PyPDF2
import re
import requests
from lxml import html
import numpy as np
from PIL import Image
import webbrowser
import cv2
import imgkit
import os
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import time
from PIL import Image
import autopy
import pyautogui
import subprocess
import webbrowser as vb

import tempfile
import urlparse

#from gi.repository import Poppler, Gtk



# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabMN(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''
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
    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        #print('parseDfData', df.title)
        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )
                    continue
                a_case.append( df.iloc[ii, jj] )
            lst_data.append( a_case )
        # save to a database file
        if(fName is not None): self.save2File( lst_data, fName )
        return lst_data
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data

    ## download a website 
    def download4Website(self, csv_url, fRaw):
        #csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//ul//li//strong//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        print('   dddd', l_dates)
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('Weekly COVID-19 Report:') in l_date.text_content(): 
                print('   sss', l_date)
                a_address = 'https://www.health.state.mn.us' + l_date.get('href')
                print('  find pdf at', a_address)
                '''
                n_start = l_date.find('Report:')
                s_date = l_date[n_start+7:] 
                n_end = s_date.find('(PDF)')
                if(n_end >= 0):
                        s_date = s_date[1: 11].replace ('00:00:00', '')

                        dt_obj = datetime.datetime.strptime(s_date, '%m/%d/%Y')
                        print('  updated on', dt_obj)
                        #nums = int(n_start)
                        self.name_file = dt_obj.strftime('%Y%m%d')
                        self.now_date = dt_obj.strftime('%m/%d/%Y')
                '''
        '''
        l_2dates = c_tree.xpath('//ul//li//strong//a/text()')
        for l_date in l_2dates:
            #print(l_date.text_content())
            if('Weekly COVID-19 Report') in l_date: 
                print('ccccccccccccccc', l_date)
                n_start = l_date.find('Report:')
                if(n_start >= 0): 
                    s_date = l_date[n_start+7:] 
                    n_end = s_date.find('(PDF)')
                if(n_end >= 0):
                        s_date = s_date[1: 11].replace ('00:00:00', '')

                        dt_obj = datetime.datetime.strptime(s_date, '%m/%d/%Y')
                        print('  updated on', dt_obj)
                        #nums = int(n_start)
                        self.name_file = dt_obj.strftime('%Y%m%d')
                        self.now_date = dt_obj.strftime('%m/%d/%Y')
        '''
        print('11111111111111', a_address)


        return a_address



    ## paser data FL
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): 
                a_address = self.open4Website(f_namea)

                if(a_address == ''): 
                    print ('    No address of downloading PDF is found')
                    return ('')

                f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                

                if(not isfile(f_namea) ):
                    result = self.download4Website(a_address, f_namea)
                    print('  downloaded', result, f_namea)
                    print('__________________')
                else:
                    print('  already exiting', f_namea)
                    print('__________________')

            '''
            bitmap= autopy.bitmap.capture_screen()
            bitmap.save(self.state_dir + 'screenshot/.png')
            '''
            #webbrowser.open_new(f_namea)
            #subprocess.Popen([f_namea],shell=True)
            #vb.open_new('mn/screenshot/mn_covid19_20201023.pdf')            
            '''
            pdf = requests.get("mn/screenshot/mn_covid19_20201023.pdf")

            with tempfile.NamedTemporaryFile() as pdf_contents:
                pdf_contents.file.write(pdf)
                file_url = urlparse.urljoin(
                    'file:', urllib.pathname2url(pdf_contents.name))
                document = Poppler.Document.new_from_file(file_url, None)
            '''
            #import subprocess
            #process = subprocess.Popen(['<here path to acrobat.exe>', '/A', 'page=1', '<here path to pdf>'], shell=False, stdout=subprocess.PIPE)
            #process.wait()

            #import os
            os.system('mn/screenshot/mn_covid19_20201023.pdf')
            

            #take the screenshot
            x=1
            while x<2:
                pyautogui.screenshot('mn/screenshot/name.png')
                x+=1
                time.sleep(2)
            return f_namea
    ## look for page containing confirmed data
    def lookForConfirmedPage(self, pdfReader):
        for page in range(12, 13):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            # locate page
            n_start = pageTxt.find('Cases no longer')
            if(n_start >= 0): print('  found at page ', page) 
            else: continue
            return pageTxt
        return ''
    ## paser data FL
    def dataReadConfirmed(self, f_name):
            print('  B.dataReadConfirmed on page 5-10', f_name)
            # step B: parse and open
            #print('    nnn', f_name)
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            print(pdfReader.numPages)
            pageTxt = self.lookForConfirmedPage(pdfReader)
            print('3333333333333', pageTxt)


            l_datas= []
            return (l_datas)

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #Step A download and save as raw PDF files
            f_targeta = self.dataDownload(name_target)
            if(f_targeta == ''): return ([], name_target, '')
            #Step B read confirmed cases
            l_d_sort = self.dataReadConfirmed(f_targeta)
            #Step C read death cases
        

            return(l_d_sort, self.name_file, self.now_date)  

## end of file