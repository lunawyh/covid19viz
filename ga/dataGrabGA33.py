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

import webbrowser

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
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
        if('Parish' in str(l_data[0][0])): pass
        else: csvwriter.writerow(['County', 'Cases', 'Deaths'])
        for a_row in l_data:
            csvwriter.writerow(a_row)
        csv_data_f.close()
    '''
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
    '''


    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = (df)
        else: return []
        return l_data
    ## save downloaded data to daily or overal data 
    def saveLatestDateGa(self, l_raw_data, name_file):
        l_overall = []
        n_total = [0, 0]
        for a_item in l_raw_data:
            n_total[0] += a_item[2]                
            n_total[1] += a_item[3]                
            l_overall.append(a_item[1:4])

        l_overall.append(['Total', n_total[0], n_total[1]])
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall
    '''
    def get_download_path(self):
	    """Returns the default downloads path for linux or windows"""
	    if os.name == 'nt':
		import winreg
		sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
		downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
		with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
		    location = winreg.QueryValueEx(key, downloads_guid)[0]
		return location
	    else:
		return os.path.join(os.path.expanduser('~'), 'Downloads')

    ## paser data CA
    def browseData(self, name_file):
            self.name_file = name_file
            # step A: downlowd and save
            webbrowser.open(self.l_state_config[5][1], new=2)
            self.f_download = self.get_download_path() + "/countycases.csv"
            
            return ([], name_file, '')
    '''
    def unzipdta(self, data):
        '''
        resp = urlopen("https://dph.georgia.gov/covid-19-daily-status-report/ga_covid_data.zip")
        zipfile = ZipFile(StringIO(resp.read()))
        #read first countycases.csv from resp
        '''

        resp = urlopen("https://dph.georgia.gov/covid-19-daily-status-report/ga_covid_data.zip")
        zipfile = ZipFile(BytesIO(resp.read()))
        for line in zipfile.open(file).readlines():
            print(line.decode('utf-8'))
        print ('hi')
            #print zipfile.namelist
            #file_name = zipfile.namelist[0]
        # opening the zip file in READ mode 
        data = zip.read(countycases.csv)
        return data
        

    ## paser data CA
    def parseData(self):
        self.unzipdta()
        return
        '''
            if(isfile(self.f_download) ):
                f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
                shutil.move(self.f_download, f_name)
                l_data_raw = self.open4File(f_name)
                l_overall = self.saveLatestDateGa(l_data_raw, self.name_file)
                return True, l_overall
            return False, []
        '''

## end of file
