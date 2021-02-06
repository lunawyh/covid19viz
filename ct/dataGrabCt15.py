#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabOh.py
#
#	grab data from OH state websites
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
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabCt(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''


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
        #print('ccccccccccccc', lst_data)
        list_data= []
        for ccc in lst_data:
            list_data.append([ccc[2], str(ccc[4]).replace('.0', ''), str(ccc[8])])

        #print('kkkkkkkkkkkkkkkkkkk', list_data[-8:])

        case = 0
        death = 0
        for a_da in list_data[-8:]:
            case += int(a_da[1].replace('.0', ''))
            death += int(a_da[2])
        l_cases3 = np.append(list_data[-8:], [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        return l_cases3


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
            lst_data = self.saveLatestDateUt(l_data)
        else: return []
        return lst_data
    ## save to csv



    ## download a website
    def download4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.request.urlretrieve(csv_url, fRaw)
        return True
    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            result = self.download4Website(f_name)
            # step B: parse and open
            lst_raw_data = self.open4File(f_name)
            # step C: convert to standard file and save

            return(lst_raw_data, self.name_file, self.now_date)

## end of file
