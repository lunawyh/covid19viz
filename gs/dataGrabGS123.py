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
import io
import zipfile
import urllib
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabGS(object):
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
        print('555555555555555', n_columns)
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
            '''
            l_cases2 = np.reshape(lst_data, (len(lst_data)/12, 12)).T

            '''
            #print('55555555555555', lst_data)
        # save to a database file
        if(fName is not None): self.save2File( lst_data, fName )
        #print('888888888888', lst_data)
        #================
        state_nam = []
        state_case = []
        state_death = []
        for a_line in lst_data:
            if a_line[0] != 'Non-GA Resident/Unknown State' or 'Unknown':
                state_nam.append(a_line[0])
                state_case.append(a_line[1])
                state_death.append(a_line[7])
        print('=============', state_nam)
        print('=============', state_case)
        print('=============', state_death)
        l_data = np.vstack((state_nam, state_case, state_death)).T 
        n_total = [0, 0]
        for a_item in l_data:
            n_total[0] += int(a_item[1])              
            n_total[1] += int(a_item[2])                
        np.append(l_data, ['Total', n_total[0], n_total[1]])
        print('lllllllllll', l_data)

        return l_data



    ## open a csv 
    def open4Buffer(self, csv_buffer):
        if( True):
            df = pd.read_csv(io.BytesIO(csv_buffer))
            print('111111111', df)
            l_data = self.parseDfData(df)
            '''
            # open csv file
            with open(csv_buffer, 'rb') as csvfile:

                # get number of columns
                for line in csvfile.readlines():
                    array = line.split(',')
                    first_item = array[0]

                num_columns = len(array)
                csvfile.seek(0)

                reader = csv.reader(csvfile, delimiter=' ')
                included_cols = [0, 1, 7]

                for row in reader:
                        content = list(row[i] for i in included_cols)
                        print ('77777777777777777', content)
            '''

        else: return []
        return l_data
    ## save downloaded data to daily or overal data 
    def saveLatestDateGa(self, l_raw_data, name_file):
        self.save2File(l_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_raw_data
    def unzipdta(self, f_name):
        # save to raw file
        urllib.urlretrieve(self.l_state_config[5][1], f_name)
        # open and unzip
        #filehandle, _ = urllib.urlretrieve(self.l_state_config[5][1])
        zip_file_object = zipfile.ZipFile(f_name, 'r')
        first_file = zip_file_object.namelist()[3]
        print('  data file', first_file)
        csv_file = zip_file_object.open(first_file)
        content = csv_file.read()
        print('======================unzip done==============')
        return content
        

    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
        self.name_file = name_file
        self.now_date = date_target
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.zip'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
        # step 1, download zipped file
        content = self.unzipdta(f_name)
        # step 2, save as raw data file
        #with open(f_name, 'w') as a_file:
        #    a_file.write(content)
        print('  save raw to ', f_name)
        # step 3, save as stanard data file
        l_data_raw = self.open4Buffer(content)
        l_overall = self.saveLatestDateGa(l_data_raw, self.name_file)
        return l_overall, self.name_file, self.now_date

## end of file
