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
import urllib.request
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabNY(object):
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
        csv_data_f = open(csv_name, 'wb')
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
            #print('1111111111111111111111111111', l_data)
        else: return []
        return l_data
    ## save to csv

    def saveLatestDateCt(self, l_data):
        #l_d_sort = sorted(l_data, key=lambda k: k[0], reverse=False)
        # find different date time
        #print('jjjjjjjjjjjjjjjjjjjjjjjjj', l_data)
        name= []
        all_datas = []
        #print('222222222222222', len(name))
        for dada in l_data:
            #print('2222222222222222222222222222', dada)
            #print('333333333333333333333333', len(name))
            if len(name) >= 1:
                if dada[1] == name[1]: 
                    name = dada
                else:
                    all_datas.append([name[1], name[3], 0])
                    name = []
            else:
                name = dada

        total_num = 0
        total_death = 0
        for a_ll in all_datas:
            total_num += int(a_ll[1])

        l_cases3 = np.append(all_datas, [['Total', total_num, total_death]], axis=0)
        print('%%%%%%%%%%%%%%%%%%55', l_cases3)
        return l_cases3


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
            lst_data = self.saveLatestDateCt(lst_raw_data)

            return(lst_data, self.name_file, self.now_date)

## end of file
