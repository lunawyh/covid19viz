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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabFl(object):
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


    ## download a website 
    def download4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True
    ## paser data CA
    def parseData(self, name_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if(not isfile(f_name) ): result = self.download4Website(f_name)
            # step B: parse and open
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            case_total = 0
            l_overall = []        
            l_overall.append(['County', 'Cases', 'Deaths'])

            pageObj = pdfReader.getPage(4)
            pageTxt = pageObj.extractText()
            l_pageTxt = pageTxt.split('\n')
            state_machine = 1
            for a_row in l_pageTxt:
                print(a_row)
                if (state_machine == 1):
                    if('County' in a_row):
                        state_machine = 2
                        a_name = a_row
                elif(state_machine == 2):
                    if('Total' in a_row):
                        a_number = a_row
                        state_machine = 3
                        #a_digital = int( re.sub("[^0-9]", "", a_number) )
            #l_overall.append([a_name, a_digital, 0])
            return(l_overall, self.name_file, self.now_date) 


    ## paser data CA
    def parseData2(self, name_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if(not isfile(f_name) ): result = self.download4Website(f_name)
            # step B: parse and open
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            case_total = 0
            l_overall = []        
            l_overall.append(['County', 'Cases', 'Deaths'])
            for page in range(5,14):
		    pageObj = pdfReader.getPage(page)
		    pageTxt = pageObj.extractText()
		    l_pageTxt = pageTxt.split('\n')
		    state_machine = 1
		    for a_row in l_pageTxt:
		        #print(a_row)    
		        if(state_machine == 1):
		            if('City and county' in a_row):
		                state_machine = 2
		        elif(state_machine == 2):
		            if('Cases' in a_row):
		                state_machine = 3
		        elif(state_machine == 3):
		            if('The' in a_row): break
		            a_name = a_row.split(',')[1]
		            state_machine = 4
		        elif(state_machine == 4):
		            a_number = a_row
		            state_machine = 3
		            a_digital = int( re.sub("[^0-9]", "", a_number) )
		            ## found or not
		            bFound = False
		            for a_row in l_overall:
		                if (a_name in a_row[0]):
		                    bFound = True
		                    a_row[1] += a_digital
		                    break
		            if(bFound):
		                pass
		            else: l_overall.append([a_name, a_digital, 0])

            return(l_overall, self.name_file, self.now_date)  


## end of file
