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
class dataGrabks(object):
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
    def download4Website(self, pdf_url, fRaw):
        print("  download4Website: ", pdf_url, fRaw)
        #csv_url = self.l_state_config[5][1]
        # save pdf file
        #urllib.urlretrieve(pdf_url, fRaw)
        r = requests.get(pdf_url)
        with open(fRaw, 'wb') as f:
            f.write(r.content)
        return True
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        
        
        #code
        tree = html.fromstring(c_page.content)
        division = tree.xpath('//div//p//a/@href')
        link = division[1]
        #link = "https://www.mass.gov" + link
        print("  get link: " + link)
        return link


    ## paser data FL
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): # not isfile(f_name) ): 
                a_address = self.open4Website(None)
                #rg_a_address = requests.get(a_address)
                #dt_obj = datetime.datetime.strptime(s_date, '%Y%m%d')
                #print('  updated on', dt_obj)
                #nums = int(n_start)
                #f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                if(not isfile(f_name) ):
                        result = self.download4Website(a_address, f_name)
                        print('  downloaded', result)
                else:
                        print('  already exiting')
            else: f_name = ''
            return f_name
    ## paser data FL
    def readList4Page(self, pdfReader, page):
        pageObj = pdfReader.getPage(page)
        print ('  ------readList4Page', page)
        pageTxt = pageObj.extractText().split('\n')
        lst_cases = []
        a_name = ''
        a_number = 0

        case_total_append = 0
        case_total_rd = 0
        
        state_machine = 100
        #if(page == 1): print(pageTxt)
        for a_line in pageTxt:                     
            if(state_machine == 100): 
                if(page == 0):
                    if('Case' in a_line):
                        state_machine = 150     
                else:
                    if ('Change' in a_line):
                        state_machine = 150    
            elif(state_machine == 150): 
                if (page == 0):
                    if('Count' in a_line):
                        state_machine = 200   
                    elif('ount' in a_line):
                        state_machine = 200   
                else:
                    if ('202' in a_line):
                        state_machine = 200
                    
            elif(state_machine == 200): 
                a_line2 = a_line.split(' ')  
                a_line1 = []
                for a_l in a_line2:
                    if a_l != '': a_line1.append(a_l)
                # after seperated with space, get the list of word
                n_line1 = len(a_line1)
                if(n_line1 < 1): continue

                #print('  --200 :', a_line)
                if( n_line1 == 2 ): # name
                    a_name = a_line1[0]
                    #print('  200 a:', a_name)
                    state_machine = 300
                elif( n_line1 == 1 ): # number
                    a_line1[0]= a_line1[0].replace(',' , '')
                    a_number = int(a_line1[0])
                    lst_cases.append([a_name, a_number, 0])
                    
                    #print('  200 c:', a_number)
                    state_machine = 500
                else: # errors
                    print('  200 d ERROR:',a_line)
                    pass

            elif(state_machine == 300): 
                a_line2 = a_line.split(' ')  
                a_line1 = []
                for a_l in a_line2:
                    if a_l != '': a_line1.append(a_l)
                # after seperated with space, get the list of word
                n_line1 = len(a_line1)
                if(n_line1 < 1): continue

                #print('  --300 :', a_line)
                if( n_line1 == 2 ): # name
                    if(a_name != ''):
                        lst_cases.append([a_name, a_number, 0]) # save last name
                        case_total_append += a_number
                        #a_name = ''
                    a_name = a_line1[0]
                    #print('  300 a:', a_name)
                    
                elif( n_line1 == 3 ): # number + name
                    a_number = int(a_line1[0])
                    lst_cases.append([a_name, a_number, 0]) # save last name
                    case_total_append += a_number
                    a_name = a_line1[1]
                    #print('  300 b:', a_number, a_name )
                elif( n_line1 == 1 ): # number or ,
                    if ',' in a_line : 
                        state_machine = 400
                        continue
                    #
                    a_number = int(a_line1[0])
                    if(a_name == ''):
                        state_machine = 500
                        print('    300 d:', a_number)
                        continue
                    #print('  300 c:', a_number)
                else: # errors
                    print('  300 d ERROR:',a_line)
                    pass
            elif(state_machine == 400): 
                a_line2 = a_line.split(' ')  
                a_line1 = []
                for a_l in a_line2:
                    if a_l != '': a_line1.append(a_l)
                # after seperated with space, get the list of word
                n_line1 = len(a_line1)
                if(n_line1 < 1): continue

                #print('  --400 :', a_line)
                if( n_line1 == 1 ): # number
                    if ',' in a_line :  
                        print('  400 a ERROR:',a_line)
                        continue
                    else:
                        a_number = int(a_line1[0]) + a_number * 1000
                        if(a_name == ''):
                            a_number = int(a_line1[0])
                            state_machine = 500
                            print('  400 d:', a_number)
                            continue
                        #print('  400 e:', a_name)
                        lst_cases.append([a_name, a_number, 0])
                        case_total_append += a_number
                        a_name = ''
                        state_machine = 300

            if(state_machine == 500): 
                a_line2 = a_line.split(' ')  
                a_line1 = []      
                for a_l in a_line2:
                    if a_l != '': a_line1.append(a_l)
                # after seperated with space, get the list of word                                 
                n_line1 = len(a_line1)
                if(n_line1 < 1): continue

                print('    --500 :', a_line) 
                              
                if( n_line1 == 1 ): # number
                    if(a_line1[0] == ','): continue
                    else: 
                        case_total_rd = a_number*1000 + int(a_line1[0])
                        print('    case_total_rd', case_total_rd)
                else: pass
        if(a_name != ''):
                    lst_cases.append([a_name, a_number, 0])
                    case_total_append += a_number
                    a_name = ''

        print('    readList4Page:', len(lst_cases), case_total_append, case_total_rd)
        return lst_cases, case_total_append, case_total_rd
    ## paser data FL
    def dataReadConfirmed(self, f_name):
            stack = [] 
            print('  B.dataReadConfirmed on page 5', f_name)
            # step B: parse and open
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            pageObj = pdfReader.getPage(0)
            # get date
            pageTxt = pageObj.extractText()
            n_start = pageTxt.find('Updated')
            if(n_start >= 0): 
                    s_date = pageTxt
                    #print('  ', s_date)
                    n_start = s_date.find('Updated')
                    n_end = s_date.find('There')
                    s_date = s_date[n_start: n_end] 
                    s_date = s_date.replace('Updated ','').replace('\n','')
                    print('  ^^^^^^^^^^', s_date)
                    #s_date = s_date.replace ('00:00:00', '')

            dt_obj = datetime.datetime.strptime(s_date.replace(' ',''), '%m/%d/%Y')
            print('  updated on', dt_obj)


            self.name_file = dt_obj.strftime('%Y%m%d')
            self.now_date = dt_obj.strftime('%m/%d/%Y')
            # read data of confirmed
            l_cases_all = []
            n_cases_total = 0
            for page in range(0,10):
                lst_cases_page, case_total_page, case_total_rd = self.readList4Page(pdfReader, page)
                l_cases_all += lst_cases_page
                n_cases_total += case_total_page
                if(case_total_rd > 0):
                    if(n_cases_total == case_total_rd):
                        print('  total is matched in', len(l_cases_all), n_cases_total, case_total_rd)
                        l_cases_all.append(['Total', n_cases_total, 0])
                    else:
                        print('  total is not matched in', len(l_cases_all), n_cases_total, case_total_rd)
                    break
                #break
            #l_d_sort = self.parseTableConfirmed(tableTxt)
            return (l_cases_all)

    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #step A, download raw data
            f_target = self.dataDownload(name_target)
            if(f_target == ''): return ([], name_target, '')
            #step B, read data
            l_d_sort = self.dataReadConfirmed(f_target)
            #if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath(l_d_sort, pdfReader)
            #else: l_d_all = []
            return(l_d_sort, self.name_file, self.now_date)  

## end of file
