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
# selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import time
#import xml.etree.ElementTree as ET
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabmd(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''




    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1] #'https://maryland.maps.arcgis.com/apps/opsdashboard/index.html#/d83b7887227e45728e6daf51a6c91c9f'
        print('  download4Website', csv_url)
        
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(5)
        #iframe = siteOpen.find_element_by_xpath('//iframe[@style="height: 1200px"]')
        iframe = siteOpen.find_element_by_xpath('//iframe[@src="https://maryland.maps.arcgis.com/apps/opsdashboard/index.html#/d83b7887227e45728e6daf51a6c91c9f"]')
        siteOpen.switch_to.frame(iframe)
        time.sleep(11)
        caseNumbers = siteOpen.find_elements_by_xpath('//span[@style="font-size:11px"]')
        
        dst_list= []
        for case_num in caseNumbers:
            dStringList = case_num.text.replace(',', '').split()
            print('  case_num', dStringList )
            dst_list.append(dStringList)
        print('list---', (dst_list))

        all_list = []
        for dst in dst_list:
            if len(dst)>3:
                all_list.append([dst[0]+dst[1], dst[3], 0])
            else:
                all_list.append([dst[0], dst[2], 0])
        print('nnnnnnnnnnnnnnnnnnnn' ,all_list)

        case = 0
        death = 0
        for a_da in all_list:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(all_list, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        siteOpen.close()
        return l_cases3


    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            f_name_raw = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.html'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            #step A, download raw data
            l_target = self.open4Website(f_name_raw)
            if(len(l_target) <= 0): return ([], name_target, date_target)
            #step B, read data
            return(l_target, self.name_file, self.now_date)  

## end of file





