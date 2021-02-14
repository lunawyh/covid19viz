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
import urllib.request
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
        urllib.request.urlretrieve(csv_url, fRaw)
        return True
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        
        tree = html.fromstring(c_page.content)
        division = tree.xpath('//div//p//a')
        #print('IIIII', division)
        #print ("    HIHI", division)
        link = ''
        for l_data in division:
            if('Age by County' in l_data.text_content()):
                a_address = l_data.get('href')
                print('  find pdf at', l_data.get('href')) 
                link = 'https://www.tn.gov'+ a_address        
                print('  ____________________', link)
                break
        #print (' HJHJ', division)
        #link = "https://www.tn.gov" + link
        #print("  get link: " + link)
        return link


    ## paser data FL    
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.xlsx'
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
        l_data = []
        if(isfile(f_name)):
            xl_file = pd.ExcelFile(f_name)
            print('  sheet_names', xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('DAILY_COUNTY_AGE_GROUP_FINAL' in (sheet)) or ('Data' in (sheet)):
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
        number= 0
        name=''
        state_machine = 100
        #print('______________', l_data_in)
        for a_row in l_data_in:
            if a_row [2] != 'Pending': continue
            #l_data_a = set(l_data_all) 
            if a_row[0] in l_data_all : 
                number += int(a_row[3])

            else:
                l_data_all.append([name, number, 0])
                name= ''
                number = 0
                name = (a_row[0])
                number = int(a_row[3])
        print('4444444444444444444444', l_data_all)
                
        '''
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
        '''
        l_data_all.pop(0) 
        return l_data_all   

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
        print('hi--------------------')
        print(pd.__version__)
        self.name_file = name_target
        self.now_date = date_target
        #step A, download raw data
        f_target = self.dataDownload(name_target)
        if(f_target == ''): return ([], name_target, '')
        #step B, read data
        l_d_sort = self.dataReadConfirmed(f_target)
        #if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath(l_d_sort, pdfReader)
        #else: l_d_all = []
        # Step C: filter data
        l_data_all = self.dataFilter(l_d_sort)
        #l_data_find = self.gotTheData(l_data_all)
        return(l_data_all, self.name_file, self.now_date)  

## end of file
