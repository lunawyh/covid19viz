#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrab.py
#
#	grab data from CA counties websites
#
#

from __future__ import print_function
import os
from lxml import html
import requests
import urllib
import re
import ssl
# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import pandas as pd
import csv
from os.path import isfile, join
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt
import math
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrab(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config

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
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data
    ## paser data CA
    def parseDataCa(self, name_file):
        l_links = self.open4File(self.state_dir + self.l_state_config[5][1])
        if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')
        link_dir =  self.state_dir + 'data_html/' + name_file + '/'
        if(not os.path.isdir(link_dir) ): os.mkdir(link_dir)
        '''
        for a_link in l_links:
                f_name = link_dir+a_link[0]+'.html'
                #print(a_link[1], f_name)
                #gcontext = ssl._create_unverified_context()
                urllib.urlretrieve(a_link[1], f_name)  #, context=gcontext)
        '''
        l_data_daily = []
        total_daily = 0
        total_death = 0
        l_data_daily.append(['County', 'Cases', 'Deaths', 'Date'])
        for a_link in l_links:
            if(a_link[0] in 'Alameda'):	
                page = requests.get(a_link[1])
                tree = html.fromstring(page.content)
                l_cases = tree.xpath('//span[@style="font-size: 75%;"]/text()')
                for a_case in l_cases:
                    if('Last updated by the City:' in a_case): 
                        a_case_l = a_case.split(':') 
                        c_date = a_case_l[1].encode('ascii','ignore')
                l_cases = tree.xpath('//p/text()')
                for a_case in l_cases:
                    if('Positive Alameda County Cases:' in a_case): 
                        a_case_l = a_case.split(':') 
                        c_pos = int( re.sub("[^0-9]", "", a_case_l[1]) )
                    if('Deaths:' in a_case):
                        a_case_l = a_case.split(':') 
                        c_death = int( re.sub("[^0-9]", "", a_case_l[1]) )
                l_data_daily.append([a_link[0], c_pos, c_death, c_date])
                total_daily += c_pos
                total_death += c_death
                break
        l_data_daily.append(['Total', total_daily, total_death, 'Today'])
        return(l_data_daily)  

## end of file
