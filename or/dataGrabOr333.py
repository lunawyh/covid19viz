   
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
import PyPDF2
from datetime import date
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabOR(object):
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


    ## $^&&
    def open4pdf(self, name_file):
        csv_url = self.l_state_config[5][1]
        print('  #$$search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//div//tbody//tr//td//span/text()')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('/////////////', l_dates)
        f_name = []
        for l_d in l_dates:
            if '/' in l_d: continue
            else: f_name.append(l_d)
        print('11111111111', f_name)

        cases = c_tree.xpath('//td[@style="text-align: center; width: 20%;"]/text()')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('22222222222222222', cases)
        f_cases = cases[ : len(f_name)]
        print('2222222222222', f_cases)

        death = c_tree.xpath('//td[@style="width: 20%;"]/text()')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('22222222222222222', cases)
        l_death = death[ : len(f_name)*2]
        l_cases2 = np.reshape(l_death, (len(l_death)/2, 2)).T
        f_death = l_cases2[0]
        print('333333333333333', f_death)

        #l_cases2 = np.reshape(l_dates, (len(l_dates)/4, 4)).T
        f_data = np.vstack((f_name, f_cases, f_death)).T


        case = 0
        death = 0
        for a_da in f_data:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(f_data, [['Total', case, death]], axis=0)

        a_address=[]
        return l_cases3

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

    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.cvs'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv') 
            #urllib.urlretrieve(urlData, f_n_total)
            #urllib.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            #self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(urlData, self.name_file, str(today))  
