   
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
import datetime 
from lxml import html
import requests
import numpy as np
from datetime import date
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabIN(object):
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


        return True
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
        # save to a database file
        print('>>>>>>>>>>>>>>>>>>>>>>', lst_data)

        state_na= []
        state_num= []
        state_death = []
        for lst in lst_data:
            state_na.append(lst[-1])
            state_num.append(lst[1])
            state_death.append(lst[2])
        l_data = np.vstack((state_na, state_num, state_death)).T 
        print('<<<<<<<<<<<<<<<<<<<<<', l_data)
        #if the file do not already exist
        if(fName is not None): self.save2File( l_data, fName )
        #return the data that turned in to a ?? now you can use it?
        return l_data
    ## save downloaded data to daily or overal data 
    def saveLatestDateTx(self, l_raw_data, name_file):
        l_cases2 = np.append( [['County', 'Cases', 'Deaths']],l_raw_data, axis=0)
        case= 0
        death = 0 
        for raw in l_raw_data:
            case += int(raw[1])
            death += int(raw[2])
        l_cases3 = np.append(l_cases2, [['Total', case, death]], axis=0)
        print ('  Total**********************88', l_cases3)
        self.save2File(l_cases3, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_cases3

    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        l_data = []
        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            print('  sheet_names', xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('Report' in (sheet)):
                    print('  select sheet', sheet)
                    nfx = sheet
                    break
            if nfx == '': # if not found, use the 1st sheet
                if(len(xl_file.sheet_names) > 0): nfx = xl_file.sheet_names[0]
                else: return []
            df = xl_file.parse( nfx )
            
            l_data = self.parseDfData(df)
            #print('  l_data', l_data)

        return l_data

    ## $^&&
    def open4excel(self, name_file):
        csv_url = self.l_state_config[5][1]
        a_address = csv_url
        return a_address

    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][2]
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//meta//meta/text()')
        print('----------', l_dates)
        for l_date in l_dates:
            if('Datasets ' in l_date):
                a_date = l_date.replace('Public Use Datasets ', '')
                #a_date = a_date[2:]
                print('  a_date', a_date)
                #ccc= a_date.replace('\xa0', '')
                #print('  111111111', a_date)
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break

    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            self.open4Website(name_file)
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
            today = (date.today())
            self.name_file = today.strftime('%Y%m%d')
            self.now_date = today.strftime('%m/%d/%Y')

            lst_data = self.saveLatestDateTx(lst_raw_data, self.name_file)
            print(';;;;;;;;;;;;;;;;;;;;;', lst_data)
            return(lst_data, self.name_file, self.now_date)  

            # the end