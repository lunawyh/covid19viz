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

    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data

    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  from', csv_url)
        # save html file
        urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//h3/text()')

        for l_date in l_dates:
            if('Total Mississippi Cases and Deaths as of' in l_date):
                print('  data is updated', l_date)
                a_date = l_date.replace('Total Mississippi Cases and Deaths as of', '')
                b_date = a_date.split(' ')
                #print (b_date)
                datetime_object = datetime.datetime.strptime(b_date[1], "%B")
                month_number = datetime_object.month

                dt_obj = datetime.datetime.strptime('%d/%d/2020'%(month_number,int(b_date[2]) ), '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
        # read tables
        cov_tables = pd.read_html(csv_url)
        # read 1st table: Overall Confirmed COVID-19 Cases by County
        print('  read table 1')
        return cov_tables[1]

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
        #print('  **********************************', lst_data)
        return lst_data


    
    ## paser data MS
    def parseData(self, name_file):
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



