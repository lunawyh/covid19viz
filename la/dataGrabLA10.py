#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabLa.py
#
#	grab data from LA state websites
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

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabLa(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.f_download1 = None
        self.f_download2 = None

    # go to parseDfData
    ##to shape the list that is combinded
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
        print('  save to', csv_name)
    
    # go to open4File
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
    def saveLatestDateLa(self, l_raw_data_1, l_raw_data_2, name_file):
        l_overall = []
        n_total = [0, 0]
        for a_item in l_raw_data_1:
            n_total[0] += a_item[2]                
             
            l_overall.append(a_item[0:2])
        for a_item2 in l_raw_data_2:
               
            n_total[1] += a_item2[2]                
            l_overall.append(a_item2[1:2])

        l_overall.append(['Total', n_total[0], n_total[1]])
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall
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
            self.f_download1 = self.get_download_path() + "/Case Counts by Parish.csv"
            self.f_download2 = self.get_download_path() + "/Deaths by Parish.csv"

            return ([], name_file, '')


    ## paser data CA
    def parseData(self):
            if( (self.f_download1 is not None) and isfile(self.f_download1) ):
                f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
                print('  save raw file to', f_name)
                shutil.move(self.f_download1, f_name)
                self.f_download1 = None
            if( (self.f_download2 is not None) and isfile(self.f_download2) ):
                f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'_2.csv'
                if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
                print('  save raw file to', f_name)
                shutil.move(self.f_download2, f_name)
                self.f_download2 = None
            if( (self.f_download1 is None) and (self.f_download2 is None) ):
                # open and save as the standard file
                f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                l_data_raw_1 = self.open4File(f_name)
                f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'_2.csv'
                l_data_raw_2 = self.open4File(f_name)
                l_overall = self.saveLatestDateLa(l_data_raw_1, l_data_raw_2, self.name_file)
                return True, l_overall

            return False, []

## end of file
