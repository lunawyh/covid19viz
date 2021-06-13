   
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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabAR(object):
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
    def find_date(self, fRaw, name_file):
      
        csv_url = self.l_state_config[5][1]
        print('  find_date', csv_url)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        with open(fRaw, 'wb') as f:
            f.write(c_page.content)
        '''
        l_dates = c_tree.xpath('//p/text()')
        for l_date in l_dates:
            #if('Updated ' in l_date):
                #a_date = l_date.replace('Updated ', '')
                a_date = ('6/22/2020')
                print('  a_date', a_date)
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
        '''
        if(True):
                dt_obj = datetime.datetime.strptime(name_file, '%Y%m%d')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
        return True
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
        #if the file do not already exist
        if(fName is not None): self.save2File( lst_data, fName )
        #return the data that turned in to a ?? now you can use it?
        return lst_data



    ## $^&&
    def open4excel(self, name_file):
        csv_url = self.l_state_config[5][1]
        #print('  #$$search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//tbody//tr//p/text()')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print ('^^^', l_dates)

        l_cases2 = np.reshape(l_dates, (len(l_dates)//4, 4)).T
<<<<<<< HEAD
        print('////////////', l_cases2[0])
        print('////////////', l_cases2[1])
        print('////////////', l_cases2[3])


        l_data = np.vstack((l_cases2[0], l_cases2[1], l_cases2[3])).T 
        l_data[-1][1] = l_data[-1][1].replace('*', '').replace(',', '')

        return l_data

=======
        l_data = np.vstack((l_cases2[0], l_cases2[1], l_cases2[3])).T 
        l_data[-1][1] = l_data[-1][1].replace('*', '').replace(',', '')
        '''
        l_data_1 = l_data[:-1] 
        l_data_2 = l_data[-1]
        l_data_3 = [l_data_2[0], l_data_2[1].replace('*', '').replace(',', ''), l_data_2[2]]     
        l_data_4 = np.vstack((l_data_1, l_data_3))
        return(l_data_4)
        '''
        return l_data
        #print ('^^^', l_data_4)

        #print('      cases reshaped', len(l_cases2))
        #total_cases = (sum(map(int, (l_cases2[1]).replace(',','').replace('*', '')))
        #print( total_cases)
        #total_death = (sum(map(int, l_cases2[3])))
            
        #l_data = np.vstack((np.array(l_cases2[0]), l_cases2[1], l_cases2[3]))          
        #return np.vstack((l_data.T, np.array(['Total', total_cases, total_death])))
>>>>>>> 6337489a8b1fe08500c24132eb5a24f03cfe0f99

        ## save downloaded data to daily or overal data 
    def saveLatestDate(self, l_raw_data, name_file):

        self.save2File(l_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_raw_data

    ## paser data CA
    def parseData(self, name_file, now_date, type_download):
            self.name_file = name_file
            self.now_date = now_date
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: save raw data
            self.find_date(f_name, name_file)
            # step B: grab the data
            lst_data = self.open4excel(name_file)
            # step C:save the data in standered formate
            self.saveLatestDate(lst_data, self.name_file)
            return(lst_data, self.name_file, self.now_date)  

       






