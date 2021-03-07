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
import urllib.request
from lxml import html
import json
import numpy as np
from selenium import webdriver  # https://selenium-python.readthedocs.io/installation.html
import time
from selenium.webdriver.common.keys import Keys 
import bs4
#from urllib.request import urlopen as uReq
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import requests
import lxml.html as lh
import pandas as pd
from pprint import pprint 
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabIl(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''

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


    def open4File(self, csv_name):
        list_a=[]
        with open(csv_name, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(', '.join(row))
                list_a.append(row)
        print('zzzzzzzzzzzzzzzzzzz', list_a)

        list_b = []
        for aaa in list_a[2:]:
            print('gggggggg', aaa[0])
            bbb= str(aaa).replace('[', '').replace(']', '').split(',')
            print('kkkkkkkkkkkkkk', bbb)
            list_b.append(bbb)
        full_list=[]
        for bbb in list_b[:73] + list_b[74:]:
            full_list.append([bbb[0], bbb[2], bbb[4]])
        print('llllllllllllll', full_list)

        case = 0
        death = 0
        for a_da in full_list:
            print('mmmmmmmmmmm', a_da)
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(full_list, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        return l_cases3

    ## download a website
    def download4Website(self, fRaw):
        csv_url = 'https://idph.illinois.gov/DPHPublicInformation/api/COVIDExport/GetCountyTestResults?format=csv'
        # save csv file
        urllib.request.urlretrieve(csv_url, fRaw)
        return True
    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            result = self.download4Website(f_name)
            # step B: parse and open
            lst_raw_data = self.open4File(f_name)


            return(lst_raw_data, self.name_file, self.now_date)

#end
