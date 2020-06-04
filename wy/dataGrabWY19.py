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
import re
import requests
from lxml import html
import json
import numpy as np
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
        print('  save2File', csv_name)
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data

    ## open a website 
    def open4WebsiteMain(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  open4WebsiteMain', csv_url)
        # save html file
        if(not isfile(fRaw) ): 
            urllib.urlretrieve(csv_url, fRaw
        # read updated date
        print('  read date')
        if( isfile(fRaw) ): 
            with open(fRaw, 'r') as file:
                page_content = file.read()
        else: return []
        lst_data = lst_data[0:-1]  # remove total row
        lst_data_se = []
        # reset subtotal of SE
        '''
        for a_item in lst_data:
            if('Southeast Utah' in a_item[0]):
                lst_data_se.append(['Southeast Utah', 0, a_item[2]])
            else:
                lst_data_se.append(a_item)
        '''

        c_tree = html.fromstring(page_content)
        print('    look for updated date')
        se_dates = c_tree.xpath('//span/text()')
        for se_data in se_dates:
            #change the month every month
            if('2020-06' in se_data):
                print('      updated date', se_data)
                break
        print('    look for county data')
        se_dates = c_tree.xpath('//h3[@class = "yoast-schema-graph yoast-schema-graph--main"]/text()')
        l_county_cases = []
        for se_data in se_dates:
            if(se_data.isdigit()):
                #print('      county number:', se_data)
                l_county_cases.append(['', int(se_data), 0])
        c_index = 0
        se_dates = c_tree.xpath('//span[@class="et_pb_text_inner"]/text()')
        for se_data in se_dates:
            if(' Cases by County' in se_data):
                print('      county names:', se_data)
                l_county_cases[c_index][0] = se_data.split(' ')[0]
                print('      data:', l_county_cases[c_index])
                lst_data_se.append(l_county_cases[c_index])
                c_index += 1
                if(c_index >= len(l_county_cases)): break
        # calculate total
        xx = list( sorted(lst_data_se) )
        arr_data_all = np.array(xx).T        
        total_confirmed=(sum(map(int, arr_data_all[1])))
        total_death=(sum(map(int, arr_data_all[2])))
        lst_data_se.append(['Total', total_confirmed, total_death])
        return lst_data_se
    
    ## paser data Ut
    def parseData(self, name_file):
            self.name_file = name_file
            f_name = self.state_dir + 'data_html/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')

            # step A: downlowd and save
            lst_raw_data = self.open4WebsiteMain(f_name)


            # step B: parse and open
            lst_data = self.saveLatestDateUt(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all



