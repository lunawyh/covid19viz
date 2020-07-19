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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabtn(object):
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
        print ("    HIHI")
        tree = html.fromstring(c_page.content)
        division = tree.xpath('//div//iframe/@src')
        link = division[0]
        print('  ____________________', link)
        #print (' HJHJ', division)
        #link = "https://www.tn.gov" + link
        #print("  get link: " + link)
        return link


    ## paser data FL    
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): # not isfile(f_name) ): 
                a_address = self.open4Website(None)
                #rg_a_address = requests.get(a_address)
                #dt_obj = datetime.datetime.strptime(s_date, '%Y%m%d')
                #print('  updated on', dt_obj)
                #nums = int(n_start)
                #f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                if(not isfile(f_name) ):
                        result = self.download4Website(a_address, f_name)
                        print('  downloaded', result)
                else:
                        print('  already exiting')
            else: f_name = ''
            return f_name
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
            stack = [] 
            print('  B.dataReadConfirmed on page 0', f_name)
            # step B: parse and open
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            pageObj = pdfReader.getPage(0)
            # get date
            pageTxt = pageObj.extractText()
            print ('  ===+++++++++++++', pageTxt)
            n_start = pageTxt.find('TennesseeCOVID')
            if(n_start >= 0): 
                    s_date = pageTxt
                    print('  ssss', s_date)
                    n_start = s_date.find('TennesseeCOVID-')
                    n_end = s_date.find('Epidemiology')
                    s_date = s_date[n_start: n_end] 
                    s_date = s_date.replace('TennesseeCOVID-19-','').replace('\n','')
                    print('  ^^^^^^^^^^', s_date)
                    #s_date = s_date.replace ('00:00:00', '')

            dt_obj = datetime.datetime.strptime(s_date.replace(' ',''), '%B%d,%Y')
            print('  updated on', dt_obj)


            self.name_file = dt_obj.strftime('%Y%m%d')
            self.now_date = dt_obj.strftime('%m/%d/%Y')
            # read data of confirmed
            l_cases_all = []
            n_cases_total = 0
            for page in range(0,10):
                lst_cases_page, case_total_page, case_total_rd = self.readList4Page(pdfReader, page)
                l_cases_all += lst_cases_page
                n_cases_total += case_total_page
                if(case_total_rd > 0):
                    if(n_cases_total == case_total_rd):
                        print('  total is matched in', len(l_cases_all), n_cases_total, case_total_rd)
                        l_cases_all.append(['Total', n_cases_total, 0])
                    else:
                        print('  total is not matched in', len(l_cases_all), n_cases_total, case_total_rd)
                    break
                #break
            #l_d_sort = self.parseTableConfirmed(tableTxt)
            return (l_cases_all)

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #step A, download raw data
            f_target = self.dataDownload(name_target)
            if(f_target == ''): return ([], name_target, '')
            #step B, read data
            l_d_sort = self.dataReadConfirmed(f_target)
            #if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath(l_d_sort, pdfReader)
            #else: l_d_all = []
            return(l_d_sort, self.name_file, self.now_date)  

## end of file
