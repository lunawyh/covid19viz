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
    ## save to csv

    def saveLatestDateNy(self, l_data):
        l_d_sort = sorted(l_data, key=lambda k: k[0], reverse=False)
        # find different date time
        l_date = []
        for a_item in l_d_sort:
            #
            bFound = False
            for a_date in l_date:
                if(a_date in a_item[0]):
                    bFound = True
                    break
            if(not bFound):
                l_date.append(a_item[0])
        # generate all daily data
        l_daily = []
        for a_date in l_date:
            l_daily = self.saveDataFromDlNy(l_d_sort, a_date, bDaily=False)
        return l_daily

    def saveDataFromDlNy(self, l_data, a_test_date, bDaily=True):
        initial_test_date = None
        l_daily = []
        l_overral = []
        total_daily = 0
        total_overral = 0
        for a_item in l_data:
            #if (a_test_date is None):
            if (a_test_date is not initial_test_date):
                initial_test_date = a_test_date
                dt_obj = datetime.datetime.strptime(a_test_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
            elif (a_test_date in a_item[0]):
                pass
            else:
                continue
            total_daily += int(a_item[2])
            total_overral += int(a_item[3])
            l_daily.append([a_item[1], a_item[2], 0])
            l_overral.append([a_item[1], a_item[3], 0])
        l_daily.append(['Total', total_daily, 0])
        l_overral.append(['Total', total_overral, 0])
        #if (not os.path.isdir(self.state_dir + 'daily/')): os.mkdir(self.state_dir + 'daily/')
        if (not os.path.isdir(self.state_dir + 'data/')): os.mkdir(self.state_dir + 'data/')
        #self.save2File(l_daily,
        #               self.state_dir + 'daily/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv')
        self.save2File(l_overral,
                       self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv')
        return l_overral

    def saveLatestDateOh(self, l_data):
        # find different date time
        l_dates = []
        for a_item in l_data:
            if(a_item[3] in 'Total'): continue
            dt_obj = datetime.datetime.strptime(a_item[3], '%m/%d/%Y')
            dt_src = dt_obj.strftime('%m/%d/%Y')
            #
            bFound = False
            for a_date in l_dates:
                if(a_date in dt_src): 
                    bFound = True
                    break
            if(not bFound):
                l_dates.append(dt_src)
        # generate all daily data
        l_date_sort = sorted(l_dates, reverse=False)
        print('  saveLatestDateOh', len(l_date_sort))
        l_daily = []
        for a_date in l_date_sort:
            l_daily = self.saveDataFromDlOh(l_data, a_date, bDaily=False)
        return l_daily
    ## is validated or not 
    def isValidDate(self, src, dst, bDaily=True):
        if(bDaily):
            if( src in dst): return True
            else: return False
        else:
            if( 'Unknown' in src): return False
            if( 'Unknown' in dst): return False
            dt_obj = datetime.datetime.strptime(src, '%m/%d/%Y')
            dt_src = int( dt_obj.strftime('%Y%m%d') )
            dt_obj = datetime.datetime.strptime(dst, '%m/%d/%Y')
            dt_dst = int( dt_obj.strftime('%Y%m%d') )
            if( dt_src >= dt_dst): return True
            else: return False
    ## save downloaded data to daily or overal data 
    def saveDataFromDlOh(self, l_data, a_date, bDaily=True):
        l_daily = []
        total_daily = 0
        total_death = 0
        item_count_base = 6
        for a_item in l_data:
            if(a_item[3] in 'Total'): continue
            #
            if( self.isValidDate(a_date, a_item[3], bDaily=bDaily) ):
                pass
            else:
                continue
            total_daily += int( a_item[item_count_base] )            
            bFound = False
            for a_daily in l_daily:
                if(a_daily[0] in a_item[0]): 
                    bFound = True
                    a_daily[1] += int(a_item[item_count_base])
            if(not bFound):
                l_daily.append([a_item[0], int(a_item[item_count_base]), 0])
                #print([a_item[0], int(a_item[item_count_base]), 0])
        #print(' --------', self.now_date)
        for a_item in l_data:
            if(str(a_item[4]) in 'Total'): continue
            if(str(a_item[4]) in '0'): continue
            #
            if( self.isValidDate(a_date, a_item[4], bDaily=bDaily) ):
                bFound = False
                for a_daily in l_daily:                    
                    if(a_daily[0] in a_item[0]): 
                        bFound = True
                        a_daily[2] += int(a_item[item_count_base+1])
                if(not bFound):
                    l_daily.append([a_item[0], 0, int(a_item[item_count_base+1]) ])
                    #print([a_item[0], 0, int(a_item[item_count_base+1]) ])

                total_death += int( a_item[item_count_base+1] )            

        l_daily = sorted(l_daily, key=lambda k: k[0], reverse=False)
        l_daily.append(['Total', total_daily, total_death])
        # save to file
        dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
        self.name_file = dt_obj.strftime('%Y%m%d')
        self.now_date = dt_obj.strftime('%m/%d/%Y')
        if(bDaily): return l_daily
        else: type_dir = 'data/'
        if(not os.path.isdir(self.state_dir + type_dir) ): os.mkdir(self.state_dir + type_dir)
        self.save2File(l_daily, self.state_dir + type_dir+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        #print(' Total', total_daily, total_death, a_date)
        #print('   saved to', self.state_dir + type_dir+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        return l_daily

    ## download a website 
    def download4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True
    ## paser data CA
    def parseData(self, name_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            result = self.download4Website(f_name)
            # step B: parse and open
            lst_raw_data = self.open4File(f_name)
            # step C: convert to standard file and save
            if( type_download == 5):
                lst_data = self.saveLatestDateNy(lst_raw_data)
            if( type_download == 15):
                lst_data = self.saveLatestDateOh(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  

## end of file
