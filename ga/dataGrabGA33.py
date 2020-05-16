#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabGa.py
#
#	grab data from GA state websites
#
#

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
from __future__ import print_function
import os
import shutil
from os.path import isfile, join
import pandas as pd
import csv

import zipfile
import urllib
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabGa(object):
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
        csvwriter.writerow(['County', 'Cases', 'Deaths'])
        for a_row in l_data:
            csvwriter.writerow(a_row)
        csv_data_f.close()
        print('  save data to ', csv_name)

    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        #print('  parseDfData', df.columns[0])
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
    ## save downloaded data to daily or overal data 
    def saveLatestDateGa(self, l_raw_data, name_file):
        l_overall = []
        n_total = [0, 0]
        for a_item in l_raw_data:
            n_total[0] += a_item[1]                
            n_total[1] += a_item[2]                
            l_overall.append(a_item[0:3])

        l_overall.append(['Total', n_total[0], n_total[1]])
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall
    def unzipdta(self):
        filehandle, _ = urllib.urlretrieve(self.l_state_config[5][1])
        zip_file_object = zipfile.ZipFile(filehandle, 'r')
        first_file = zip_file_object.namelist()[0]
        print('  data file', first_file)
        csv_file = zip_file_object.open(first_file)
        content = csv_file.read()
        return content
        

    ## paser data CA
    def parseData(self, name_file):
        # step 1, download zipped file
        content = self.unzipdta()
        # step 2, save as raw data file
        self.name_file = name_file
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
        with open(f_name, 'w') as a_file:
            a_file.write(content)
        print('  save raw to ', f_name)
        # step 3, save as stanard data file
        l_data_raw = self.open4File(f_name)
        l_overall = self.saveLatestDateGa(l_data_raw, self.name_file)
        return True, l_overall

## end of file
