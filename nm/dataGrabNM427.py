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
import requests
from lxml import html
import zipfile
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabNM(object):
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

    ## download a website
    def download4Website(self, fRaw):
        zip_url = self.l_state_config[5][1]
        print('  download4Website ...')

        htmlPage = requests.get(zip_url)
        tree = html.fromstring(htmlPage.content)
        list_I = tree.xpath('//article//div//ul//li')
        #print('list............', list_I)
        case_list = []
        for case_num in list_I: 
            dStringList = case_num.text.split()
            #print('  ------------case_num', dStringList )
            case_list.append([dStringList])
        #print('llllllllllll', case_list[42:75])  
        fin_list = []  
        for ccc in case_list[42:75]:
            if len(ccc[0]) == 3:
                print('ccc....', ccc)
                fin_list.append([ccc[0][0], ccc[0][2].replace(',', ''), 0])
            else:
                print('ccc....', ccc)
                fin_list.append([ccc[0][0]+ ccc[0][1], ccc[0][-1].replace(',', ''), 0])
                
        print('fin..........', fin_list)

        anum = 0
        adeath = 0
        for lst in fin_list:
            anum += int(lst[1])
            print('1111111111111111', lst[1])
            adeath += int(lst[2])
                
        raw_total_data = (['Total', anum, adeath])
        print('llllllllll', raw_total_data)
        finall_list = np.append(fin_list, [['Total', anum, adeath]], axis=0)

        return finall_list

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
            print('mmmmmmmmmm.............', a_row)
            csvwriter.writerow(a_row)
        csv_data_f.close()
        #print('  save2File', csv_name)
        
    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.zip'
            #l_name = self.state_dir + 'data_raw/'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.download4Website(f_name)
            # step B: parse and open
            #lst_raw_data = self.open4FileBuffer(data_csv)
            # step C: convert to standard file and save
            #lst_data = self.saveLatestDateMa(lst_raw_data)
            lst_data = self.saveLatestDateUt(data_csv)
            #print(data_csv)
            return(lst_data, self.name_file, self.now_date)

## end of file
