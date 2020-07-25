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
class dataGrabKY(object):
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
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//div//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('   dddd', l_dates)
        a_address = '', ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('KY COVID-19' in l_date.text_content() or 'KY COVID-19' in l_date.text_content()):
                #print('   sss', l_date)
                a_address = l_date.get('href')
                print('  find pdf at', l_date.get('href'))
            
        return a_address
    ## paser data FL
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
           
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): 
                a_address = self.open4Website(f_namea)
                if(a_address == ''): 
                    print ('    No address of downloading PDF is found')
                    return ('')
                n_start = a_address.find('Summary')
                if(n_start >= 0): 
                    s_date = a_address[n_start+7:] 
                    n_end = s_date.find('2020')
                    if(n_end >= 0):
                        s_date = s_date.replace ('00:00:00', '')

                        dt_obj = datetime.datetime.strptime(s_date, '%m%d%Y')
                        print('  updated on', dt_obj)
                        #nums = int(n_start)2020
                        self.name_file = dt_obj.strftime('%Y%m%d')
                        self.now_date = dt_obj.strftime('%m/%d/%Y')
                        f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                        
                if(not isfile(f_namea) ):
                    result = self.download4Website(a_address, f_namea)
                    print('  downloaded', result, f_namea)
                else:
                    print('  already exiting', f_namea)
               
            return f_namea 
    ## paser data FL
    def dataReadConfirmed(self, f_name):
            print('  B.dataReadConfirmed on page 3,4', f_name)
            # step B: parse and open
            #print('    nnn', f_name)
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            pageObj = pdfReader.getPage(2)
            pageObj2 = pdfReader.getPage(3)
            pageTxt = pageObj.extractText() + pageObj2.extractText()
            print('  pageTxt 5:', pageTxt)
            n_start = pageTxt.find('by County')
            if(n_start >= 0):
                n_end = pageTxt.find('2020')
                s_date = pageTxt[n_start: n_end+4]
                print('    updating date', s_date)
                s_date = s_date.replace('by County ', '')
                dt_obj = datetime.datetime.strptime(s_date, '%m/%d/%Y')
                print('    updated on', dt_obj)
                #nums = int(n_start)
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')

            # get text in the table list

            n_start = pageTxt.find('Jefferson')

            pageTxt = pageTxt[n_start:]


            #print('********', pageTxt)
            #pageTxt = pageTxt[n_start:]
            tableTxt = ''
            pre_char = '\n'
            for a_char in pageTxt:
                if( a_char.isalpha() ):
                    if( pre_char.isdigit() ): tableTxt += '\n'
                pre_char = a_char
                tableTxt += a_char
            print('  tableTxt on 5:', len(tableTxt))
            l_d_sort = self.parseTableConfirmed(tableTxt)
            return (l_d_sort, pdfReader)
 
    ## paser data FL
    def parseTableConfirmed(self, pageTxt):
            case_total = 0
            case_total_rd = 0
            l_overall = [] 
            #l_overall.append(['County', 'Cases', 'Deaths'])

            l_pageTxt = pageTxt.split('\n')
            state_machine = 1
            a_name = ''
            a_digital = 0
            l_numbers = []
            for a_row in l_pageTxt:

		        print('  a_row', a_row)
		        '''
		        if(state_machine == 1):
		            if( a_row.lower().islower() ):
		                # a county
		                a_name = a_row
		                l_numbers = []
		                state_machine = 2
		        elif(state_machine == 2):
		            if( a_row.lower().islower() ):
		                print('  error county name', a_row)
		            elif '0.' in a_row: pass
		            else:
		                # a line of numbers
		                l_numbers.append(a_row)
		                state_machine = 3
		        elif(state_machine == 3):
		            if( a_row == '' ):
		                pass
		            elif '0.' in a_row: pass
		            #if(a_digital <= 0): print('    at a_row', a_name)
		            if('Total' in a_name): 
		                    case_total_rd =  a_digital
		                    print('    Total is read', a_digital)
		            else:
		                case_total += a_digital
		                    
		                l_overall.append([a_name, a_digital, 0])
		                print( '*****', l_overall)
		                # another county
		                a_name = a_row
		                l_numbers = []
		                state_machine = 2
		                # to next county
		        '''
		            
            # the last name and number
            a_digital = self.getNumberConfirmed(l_numbers)
            if('Total' in a_name): 
                case_total_rd =  a_digital
                print('    Total is read', a_digital)
            else:
                l_overall.append([a_name, a_digital, 0])
                case_total += a_digital
            
            l_d_sort = sorted(l_overall, key=lambda k: k[0])
            if(case_total == case_total_rd): 
                l_d_sort.append(['Total', case_total, 0])
                print('  Total is confirmed', case_total, case_total_rd)
            else: 
                l_d_sort.append(['Total', case_total_rd, 0])
                print('  Total is mismatched', case_total, case_total_rd)
            return (l_d_sort)


    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #Step A download and save as raw PDF files
            f_targeta = self.dataDownload(name_target)
            if(f_targeta == ''): return ([], name_target, '')
            #Step B read confirmed cases
            l_d_sort, pdfReader = self.dataReadConfirmed(f_targeta)
            #Step C read death cases
            #if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath4Pages(l_d_sort, f_targetb)
            #else: l_d_all = []
            l_d_all = []
            return(l_d_all, self.name_file, self.now_date)  

## end of file
