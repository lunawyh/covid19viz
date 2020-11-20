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
# selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabwa(object):
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
        #c_page = requests.get(csv_url)
        #c_tree = html.fromstring(c_page.content)
        #
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(5)
        page_text = driver.page_source

        # get updated time
        c_tree = html.fromstring(page_text)
        #print('  ooooooooooopen4Website', page_text)
        l_text_data = c_tree.xpath('//tbody//tr//td//a/text()')
        #print(' 1111111111111 open4Website date:',l_text_data)
        # then l_text_data is the state names-------------------
        l_num_data = c_tree.xpath('//tbody//tr//td/text()')
        cc = len(l_text_data) *3 
        l_num = l_num_data[ : cc]
        #print('2222222222222222222222',l_num)
        un_sigh = l_num_data[cc : cc+4]
        total = l_num_data[cc+4 : cc+7]
        tootal= ['Total',]
        for a_ll in total:
            tootal.append(a_ll)
        #print('2222222222222222222222',un_sigh)
        #print('2222222222222222222222',total)

        number_data= []
        for a_un in l_num:
            aa= a_un.replace(',', '')
            number_data.append(aa)

        un_sigh= []
        for a_un in un_sigh:
            aa= a_un.replace(',', '')
            un_sigh.append(aa)

        tootal= []
        for a_un in tootal:
            aa= a_un.replace(',', '')
            tootal.append(aa)


        un_sigh = np.reshape( un_sigh, (len( un_sigh)/4, 4)).T  
        un_sigh = np.vstack((un_sigh[0], un_sigh[1], un_sigh[3])).T      

        tootal = np.reshape( tootal, (len( tootal)/4, 4)).T  
        tootal = np.vstack((tootal[0], tootal[1], tootal[3])).T  

        l_cases3 = np.reshape( number_data, (len( number_data)/3, 3)).T
        print(' ------ l_text_data:', len(l_text_data))
        print('  ------l_text_data_num:', l_cases3)

        # put together        
        l_cases3 = np.vstack((l_text_data, l_cases3[0], l_cases3[2])).T 
        l_data2= np.append(l_cases3, un_sigh)
        l_data2= np.append(l_data2, tootal)
        print('3333333333333', len(l_data2))
        print('3333333333333', l_data2)

        l_dd = []
        for a_cc in l_data2:
            if a_cc == '\n' : pass
            else: l_dd.append(a_cc)
        print('444444444', l_dd)

        l_data2 = np.reshape( l_dd, (len( l_dd)/3, 3)).T
        print('3333333333333', l_data2)

        l_cases3 = np.vstack((l_data2[0], l_data2[1], l_data2[2])).T 
        print('3333333333333', l_cases3)
        driver.quit()  # close the window
        return l_cases3


    ## paser data FL
    def readList4Page(self, pdfReader, page):
        pageObj = pdfReader.getPage(page)
        print ('  ------readList4Page', page)
        pageTxt = pageObj.extractText().split('\n')
        lst_cases = []
        a_name = ''
        a_number = 0

        case_total_append = 0
        case_total_rd = 0
        
        state_machine = 100

    ## paser data FL
    def dataReadConfirmed(self, f_name):
        print('>>>>>>>>>>>>', f_name)
        l_data = []
        if(isfile(f_name)):
            xl_file = pd.ExcelFile(f_name)
            print('  sheet_names', xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('DAILY_COUNTY_AGE_GROUP_FINAL' in (sheet)) or ('Cases' in (sheet)):
                    print('  select sheet', sheet)
                    nfx = sheet
                    break
            if nfx == '': 
                # if not found, use the 1st sheet
                if(len(xl_file.sheet_names) > 0): nfx = xl_file.sheet_names[0]
                else: return []
            df = xl_file.parse( nfx )
            
            l_data = self.parseDfData(df)
            #print('  l_data', l_data)

        return l_data                  
        

    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        #print('parseDfData', df.title)
        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                #is the 'iloc(select rows and columns by number)' is ' nan(not a number)'
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )

                    continue
                #a_case will have all the data from the 'data'
                a_case.append( df.iloc[ii, jj] )
            lst_data.append( a_case )
        return lst_data
    def dataFilter(self, l_data_in)     :
        l_data_all = []
        l_cas_total = 0
        state_case = ''
        print ('dataFilter', l_data_in[-1][0])
        c_time = l_data_in[-1][0]
        #c_time = int(c_time).replace('00:00:00', '')
        state_machine = 100
        for a_row in l_data_in:
            if a_row[0] != c_time: continue
                
        
            #print(' HIHI')
            bFound = False
            for a_ll in l_data_all:
                if a_row[1] == a_ll[0]:
                    bFound = True
                    a_ll[1] += int(a_row[3])
                    l_cas_total += int(a_row[3])
                    break
            if(not bFound):
                l_cas_total += int(a_row[3])
                l_data_all.append([ a_row[1], int(a_row[3]), 0 ])
        l_data_all.append(['Total', int(l_cas_total), 0])
        print('++++++++++++++++++++ l_data_all_no2', l_data_all)
        print('total::::::::', l_cas_total)
        return l_data_all   

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            f_name_raw = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.html'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            #step A, download raw data
            l_target = self.open4Website(f_name_raw)
            if(len(l_target) <= 0): return ([], name_target, date_target)
            #step B, read data
            return(l_target, self.name_file, self.now_date)  

## end of file
