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
class dataGrabMa(object):
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
    def downloadFileMa(self, link_name):
        urllib.urlopen(link_nameg)

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
<<<<<<< HEAD
    ## open a csv
=======
    ## open a csv 
>>>>>>> aa58caeb5257c21e95ecd4691238da0331cb4893
    def open4File(self, f_name):
        # unzip downloaded file and get a csv file
        print('  unzip ...')
        # open a csv file
        csv_name = 'County.csv'
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data
    ## save to csv

    def saveLatestDateMa(self, l_data):
        l_d_sort = sorted(l_data, key=lambda k: k[0], reverse=False)
        # find different date time
        l_date = []
        for a_item in l_d_sort:
            #
            bFound = False
            for a_date in l_date:
                if(a_date in a_item[8]):
                    bFound = True
                    break
            if(not bFound):
                l_date.append(a_item[8])
        # generate all daily data
        l_daily = []
        for a_date in l_date:
            l_daily = self.saveDataFromDlMa(l_d_sort, a_date, bDaily=False)
        return l_daily

    def saveDataFromDlMa(self, l_data, a_test_date, bDaily=True):
        initial_test_date = None
        #l_daily = []
        l_overral = []
        #total_daily = 0
        total_overral = 0
        total_overral_deaths = 0
        for a_item in l_data:
            #if (a_test_date is None):
            if (initial_test_date is None and a_test_date in a_item[8]):
                initial_test_date = a_test_date
                dt_obj = datetime.datetime.strptime(a_test_date, '%Y/%m/%d %H:%M:%S')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
            elif (a_test_date in a_item[8]):
                pass
            else:
                continue
            #total_daily += int(a_item[2])
            total_overral += int(a_item[4])
            total_overral_deaths += int(a_item[5])
            #l_daily.append([a_item[1], a_item[2], 0])
            l_pending = []
            if 'Pending Validation' in a_item:
                l_pending = a_item
            else:
                l_overral.append([a_item[1], a_item[4], a_item[5]])
            l_overral.sort(key=lambda county: county[0])
        #l_daily.append(['Total', total_daily, 0])
        l_overral.append(l_pending)
        l_overral.append(['Total', total_overral, total_overral_deaths])
        #if (not os.path.isdir(self.state_dir + 'daily/')): os.mkdir(self.state_dir + 'daily/')
        if (not os.path.isdir(self.state_dir + 'data/')): os.mkdir(self.state_dir + 'data/')
        #self.save2File(l_daily,
        #               self.state_dir + 'daily/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv')
        self.save2File(l_overral,
                       self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + self.name_file + '.csv')
        return l_overral


    ## download a website
    def download4Website(self, fRaw):
        zip_url = self.l_state_config[5][1]
        print('  download4Website from', zip_url)
        # get the updated date from the website
        # update self.name_file and self.now_date
        print('  get the updated date ...')
<<<<<<< HEAD
        c_page = requests.get(self.l_state_config[5][1])
=======
        c_page = requests.get(self.l_state_config[5][2])
>>>>>>> aa58caeb5257c21e95ecd4691238da0331cb4893
        ''' this is an example ONLY
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//strong/text()')
        for l_date in l_dates:
            if('Confirmed COVID-19 Cases by Jurisdiction updated' in l_date):
                a_date = l_date.replace('Confirmed COVID-19 Cases by Jurisdiction updated ', '')
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
        '''
        # save csv file
        #urllib.urlretrieve(csv_url, fRaw)  # does NOT work
<<<<<<< HEAD
        r = requests.get(zip_url)
=======
        r = requests.get(zip_url)        
>>>>>>> aa58caeb5257c21e95ecd4691238da0331cb4893
        with open(fRaw, 'wb') as f:
            f.write(r.content)
        print('  saved to', fRaw)
        return True
    ## paser data CA
    def parseData(self, name_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.zip'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            result = self.download4Website(f_name)
            # step B: parse and open
            lst_raw_data = self.open4File(f_name)
            # step C: convert to standard file and save
            if( type_download == 5):
                lst_data = self.saveLatestDateNy(lst_raw_data)
            if( type_download == 22):
                lst_data = self.saveLatestDateMa(lst_raw_data)

            return(lst_data, self.name_file, self.now_date)

## end of file