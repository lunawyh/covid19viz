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

import requests
from lxml import html
import json
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabUT(object):
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
    def saveLatestDateUt(self, l_raw_data):
        l_overall = []
        
        l_overall.append(['County', 'Cases', 'Deaths'])
        for a_item in l_raw_data:
            l_overall.append(a_item)
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
        #if(not isfile(fRaw) ): 
        urllib.urlretrieve(csv_url, fRaw)

        # read updated date
        print('  read date')
        if( isfile(fRaw) ): 
            with open(fRaw, 'r') as file:
                page_content = file.read()
        else: return []
        c_tree = html.fromstring(page_content)
        u_dates = c_tree.xpath('//p/text()')
        for l_date in u_dates:
            if('Report Date: ' in l_date):
                print('    data is updated,', l_date)
                n_start = l_date.find(l_date)
                s_date = l_date[n_start:].split(':')
                #print (s_date[1]) # an example,  May 24, 2020
                dt_obj = datetime.datetime.strptime(s_date[1], " %b %d, %Y")
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                print('    name_file is updated:', self.name_file)
                break
        # read tables
        print ('  read data table of counties')
        # read 1st table: Overall Confirmed COVID-19 Cases by County
        u_scripts = c_tree.xpath('//script/text()')
        for l_script in u_scripts:
            if('Jurisdiction' in l_script and 'Cases' in l_script and 'Deaths' in l_script):
                print('  ###############################################  counties data:', l_script)
                return self.parseJsonString(l_script)
                
        return []
    ## parse from exel format to list 
    def parseJsonString(self, j_str):
        print('    parseJsonString')
        lst_data = []
        j_data = json.loads(j_str.replace(' County', ''))  # is a json string
        l_raw_data = j_data['x']['data']		# fixed keys
        print('  ############################################### ', l_raw_data)
        l_raw_data = l_raw_data[:2] + l_raw_data[3:]  	# remove 3rd column of Hospitalizations
        lst_data = zip(*l_raw_data)			# transpose the matrix
        
        print('    counties', len(lst_data))
        return lst_data

    def data_in_eastwest(self, ew_data):
        ew_webname = self.l_state_config[5][2]  #'https://swuhealth.org/covid/'
        c_tree = html.fromstring(ew_webname)
        ew_dates = c_tree.xpath('//ul/text()')
        for ew_data in ew_dates:
            if('Washington County' in ew_data):
                n_start = ew_data.find(ew_data)
                s_date = ew_data[n_start:].split(':')

    def data_in_southeast(self, se_data):
        se_webname = https://www.seuhealth.com/covid-19
        c_tree = html.fromstring(se_webname)
        se_dates = c_tree.xpath('//ul/text()')
        for se_data in se_dates:
            if('Washington County' in se_data):
                n_start = se_data.find(se_data)
                s_date = se_data[n_start:].split(':')

    
    ## paser data Ut
    def parseData(self, name_file):
            self.name_file = name_file
            f_name = self.state_dir + 'data_html/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')
            # step A: downlowd and save
            lst_raw_data = self.open4Website(f_name)
            # step B: parse and open
            lst_data = self.saveLatestDateUt(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all



