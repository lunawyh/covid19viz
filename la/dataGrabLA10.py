   
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
import urllib.request
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabLa(object):
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

    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  open4Website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_links = c_tree.xpath('//p//a')
        a_address = ''
        for l_data in l_links:      
            if('Data by Parish by Day' in l_data.text_content()):
                a_address = 'https://ldh.la.gov' + l_data.get('href')
                print('  find link at', a_address)
		
        return a_address
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
        #print('......', lst_data)

        state_nam = []
        state_case = [ ]
        case = 0
        for a_lst in lst_data:
            #print('111111111', a_lst)
            if a_lst[1] not in state_nam:
                if case is not 0:
                  state_case = state_case[: -1]
                  state_case.append(case)
                  case = 0

                else:
                    state_nam.append(a_lst[1])
                    state_case.append((a_lst[5]))
                    case +=(int(a_lst[5]))
            else:
                case += int(a_lst[5])

        #print('22222222222', (state_nam))
        #print('33333333333', (state_case))
        #print('len 22222222222', len(state_nam))
        #print('len 33333333333', len(state_case))

        l_cases3 = np.vstack((state_nam, state_case, [0]*len(state_case))).T 


        total_death = 0
        total_case = 0
        for a_line in l_cases3:
                total_case += int(a_line[1])
                total_death += int(a_line[2])

        l_cases3 = np.append(l_cases3, [['Total', total_case, total_death]], axis=0)

        #if the file do not already exist
        if(fName is not None): self.save2File( l_cases3, fName )
        #return the data that turned in to a ?? now you can use it?
        print('555555555', l_cases3)
        return l_cases3
    ## save downloaded data to daily or overal data 
    def saveLatestDateTx(self, l_raw_data, name_file):
        l_overall = []

        l_overall.append(['County', 'Cases', 'Deaths'])
        lst_raw_data6 = np.append(l_overall, l_raw_data, axis=0)

        self.save2File(lst_raw_data6, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return lst_raw_data6
    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        l_data = []
        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            print('  sheet_names', xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('TESTING' in (sheet)):
                    print('  select sheet', sheet)
                    nfx = sheet
                    break
            if nfx == '': # if not found, use the 1st sheet
                if(len(xl_file.sheet_names) > 0): nfx = xl_file.sheet_names[0]
                else: return []
            df = xl_file.parse( nfx )
            
            l_data = self.parseDfData(df)
            print('  88888888888888888 l_data', l_data)

        return l_data


    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            self.now_date = date_target
            # step A: read date
            urlData = self.open4Website(name_file)
            #self.open4excel(name_file)
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # 
            urllib.request.urlretrieve(urlData, f_n_total)
            urllib.request.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            lst_raw_data = self.open4Xlsx(f_n_total)

            lst_data = self.saveLatestDateTx(lst_raw_data, self.name_file)
            return(lst_data, self.name_file, self.now_date)  


