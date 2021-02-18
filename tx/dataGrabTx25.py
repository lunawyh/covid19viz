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
import urllib.request
import numpy as np
from datetime import date
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabTx(object):
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
    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        print('  parseDfData of', df.shape)
        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )
                    continue
                a_case.append( df.iloc[ii, jj] )
            lst_data.append( a_case )
            if( len(a_case) > 0 and a_case[0] == 'Total' ):
                print('  Last Read', a_case)
                break
        # save to a database file
        if(fName is not None): self.save2File( lst_data, fName )
        return lst_data
    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        print("  open4Xlsx", xlsx_name)
        s_date = ''
        if(isfile(xlsx_name) ):
            xl_file = pd.read_excel(xlsx_name, engine= 'openpyxl')
            #xl_file = pd.read_excel(xlsx_name)
            #print("  sheet names==================", xl_file)
            #print('2222222222222222222222', type(xl_file))

            xl_cdcd = xl_file.to_numpy()
            #print("  vvvvvvvvvvvvvvv", xl_cdcd)
            #print('sssssssssssssssssss', type(xl_cdcd))
            list_full = []
            for svsv in xl_cdcd[2:-2]:
                susu = str(svsv)
                #print('//////////////', susu)
                #print('cccccccccccc', type(susu))
                stst= susu.replace("'", "").replace("[", "").replace("]", "")
                #print('9999999999999', stst)
                sisi = stst.split(' ')
                #print('//////////////', sisi)
                list_full.append([sisi[0], sisi[-3], 0])
            print('list_full=============', list_full)
                

        return list_full
    ## save downloaded data to daily or overal data 
    def saveLatestDateTx(self, l_raw_data, name_file):
        l_overall = []
        offset = 0   # after 5/5 changed from 1 to 0
        l_overall.append(['County', 'Cases', 'Deaths'])
        for a_item in l_raw_data:
            if 'County' in str(a_item[offset]):continue
            #if str(a_item [1]) in '0':
            #    a_item[1]='Total'
                
            l_overall.append(a_item[offset:])  
        #for a_item in l_overall:
        #    print (a_item)
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall
    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_file+'.xlsx'
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_file+'total.xlsx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            gcontext = ssl._create_unverified_context()
            urllib.request.urlretrieve(self.l_state_config[5][2], f_n_total)#, context=gcontext)
            urllib.request.urlretrieve(self.l_state_config[5][1], f_name)#, context=gcontext)
            # step B: parse and open
            lst_raw_data = self.open4Xlsx(f_name)
            today = (date.today())
            name_file = today.strftime('%Y%m%d')
            now_date = today.strftime('%m/%d/%Y')

            # step C: convert to standard file and save
            lst_data = self.saveLatestDateTx(lst_raw_data, name_file)
            return(lst_data, name_file, now_date)  

## end of file
