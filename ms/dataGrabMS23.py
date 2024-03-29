#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabFl.py
#
#	grab data from FL state websites
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
import PyPDF2
import re
import requests
from lxml import html
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabMS(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''

    ## save downloaded data to daily or overal data 
    def saveLatestDateMs(self, l_raw_data):
        l_overall = []
        
        l_overall.append(['County', 'Cases', 'Deaths'])
        for a_item in l_raw_data:
            # remove ******************************************************
            #print('  save data', a_item)
            a_item[2] = str(a_item[2]).replace('*', '')
            #***************************************
            a_item[1]=  str(a_item[1]).replace('*', '')
            l_overall.append(a_item[:3])
        #for a_item in l_overall:
        #    print (a_item)
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        return l_overall
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
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  from', csv_url)
        # save html file
        urllib.request.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//div/text()')

        for l_date in l_dates:
            if('Updated' in l_date):
                print('  data is ', l_date)  # Updated June 10, 2020.
                a_date = l_date.replace('Updated', '')
                #b_date = a_date.split(' ')
                #print (b_date)
                #datetime_object = datetime.datetime.strptime(b_date[1], "%B")
                #month_number = datetime_object.month
                dt_obj = datetime.datetime.strptime(a_date.replace('.', '').replace(' ', ''), '%B%d,%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break

        '''
        # get links to downloading files
        #print('hi')
        division = c_tree.xpath('//ul//li//a/@href')
        #print ('***division', division)
        for divs in division:
            if 'resources' in divs:
                print('division_resources ^*&', divs)
                divisions = divs[ :2]
                link = divisions
        link = "https://msdh.ms.gov" + link
        print("  get link: " + link)
       
        return link
        '''
        # read tables
        cov_tables = pd.read_html(csv_url)
        row_max, n_table = 0, 0
        for jj in range(len(cov_tables)):
            (n_rows, n_columns) = cov_tables[jj].shape
            print('  table ', jj, (n_rows, n_columns) )
            if(n_rows > row_max): 
                row_max = n_rows
                n_table = jj
        # read  table: Overall Confirmed COVID-19 Cases by County
        print('  read table ', n_table)
        return cov_tables[n_table]   # use the maximum size of table, do not use fixed number


    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        print('  get data table', df.shape)
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
        print('  **********************************', lst_data)
        return lst_data


    
    ## paser data MS
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            f_name = self.state_dir + 'data_html/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')
            # step A: downlowd and save
            df_a = self.open4Website(f_name)
            f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            # step B: parse and open
            lst_raw_data = self.parseDfData(df_a)
            # step C: convert to standard file and save
            lst_data = self.saveLatestDateMs(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all



