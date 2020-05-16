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
    def download4Website(self, csv_url, fRaw):
        #csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('See state report' in l_date.text_content()):
                a_address = l_date.get('href')
                print('  download report at', l_date.get('href'))
                break
        return a_address
    ## paser data FL
    def dataDownload(self, name_target):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if(True): # not isfile(f_name) ): 
                a_address = self.open4Website(None)
                if(a_address == ''): return ([], None, None)
                print('  a_address', a_address)
                n_start = a_address.find('report')
                if(n_start >= 0): 
                    s_date = a_address[n_start + 7: n_start + 7 + 5] 
                    print('  ', s_date)
                    dt_obj = datetime.datetime.strptime(s_date, '%m%d%y')
                    print('      ', dt_obj)
                    #nums = int(n_start)
                    self.name_file = dt_obj.strftime('%Y%m%d')
                    self.now_date = dt_obj.strftime('%m/%d/%Y')
                    f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                    if(not isfile(f_name) ):
                        result = self.download4Website(a_address, f_name)
                else: f_name = ''
            return f_name
    ## paser data FL
    def dataReadConfirmed(self, f_name):
            # step B: parse and open
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            case_total = 0
            case_total_rd = 0
            l_overall = [] 
            #l_overall.append(['County', 'Cases', 'Deaths'])

            pageObj = pdfReader.getPage(4)
            pageTxt = pageObj.extractText()
            l_pageTxt = pageTxt.split('\n')
            state_machine = 1
            a_name = ''
            a_digital = 0
            for a_row in l_pageTxt:
		        #print(a_row)
		        if(state_machine == 1):
		            if('County' in a_row):
		                state_machine = 2
		        elif(state_machine == 2):
		            if('Total' in a_row):
		                state_machine = 3
		        elif(state_machine == 3):
		            if('County' in a_row):
		                state_machine = 4
		        elif(state_machine == 4):
		            if('Total' in a_row):
		                state_machine = 5
		        elif(state_machine == 5):
		            if('Total' in a_row):
		                state_machine = 16
		            else:
		                a_name = a_row
		                state_machine = 6
		        elif(state_machine == 6):
		            if( a_row == '' ):
		                pass
		            elif( a_row.lower().islower() ):
		                if('Total' in a_name): case_total_rd = a_digital
		                else: 
		                    case_total += a_digital
		                    if(a_name in 'Dade'): a_name = 'Miami-Dade'
		                    l_overall.append([a_name, a_digital, 0])
		                a_name = a_row
		            else:
		                a_digital = int( re.sub("[^0-9]", "", a_row) )
            l_overall.append([a_name, a_digital, 0])
            case_total += a_digital
            
            l_d_sort = sorted(l_overall, key=lambda k: k[0])
            if(case_total == case_total_rd): l_d_sort.append(['Total', case_total, 0])
            else: print('  Total is mismatched', case_total, case_total_rd)
            return (l_d_sort, pdfReader)
    ## paser data FL
    def dataReadDeath(self, l_d_sort, pdfReader):
            # read death in county
            p_s, p_e = 20, 58
            #p_s, p_e = 31, 43 # page number in PDF for 4/19/2020
            #p_s, p_e = 30, 48 # page number in PDF for 4/24/2020
            case_total = 0
            for page in range(p_s-1, p_e+1):
		    pageObj = pdfReader.getPage(page)
		    pageTxt = pageObj.extractText()
		    l_pageTxt = pageTxt.split('\n')
		    if('Coronavirus: line list of deaths in Florida residents' in l_pageTxt[0]): pass
		    else: continue
		    state_machine = 1
		    for a_row in l_pageTxt:
		        #print(a_row)    
		        if(state_machine == 1):
		            if('today' in a_row):
		                state_machine = 2
		        elif(state_machine == 2 ):
		            if( a_row.lower().islower() ): pass
 		            else: continue
		            if( 'Unknown' in a_row ): continue
 		            if(a_row in 'Dade'): a_row = 'Miami-Dade'
		            for a_d_row in l_d_sort:
				if a_d_row[0] in a_row:
				    a_d_row[2] += 1
				    case_total += 1
				    break
		    print(' PDF page on', page+1, case_total)
            l_d_sort[-1][2] = case_total
            return l_d_sort 
    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            f_target = self.dataDownload(name_target)
            self.now_date = date_target
            if(f_target == ''): return ([], name_target, '')
            l_d_sort, pdfReader = self.dataReadConfirmed(f_target)
            l_d_all = self.dataReadDeath(l_d_sort, pdfReader)
            return(l_d_all, self.name_file, self.now_date)  
    ## paser data FL
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
