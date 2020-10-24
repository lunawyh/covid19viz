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
import numpy as np

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
            if('Weekly COVID-19 Report' in l_date.text_content()):
                print('   sss', l_date)
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
                n_start = a_address.find('Weekly-Report-')
                if(n_start >= 0): 
                    s_date = a_address[n_start+14:] 
                    print('.............', s_date)
                    n_end = s_date.find('-FINAL.pdf')
                    s_date= s_date[: n_end]
                    print('.............', s_date)
                    if(n_end >= 0):
                        dt_obj = datetime.datetime.strptime(s_date, '%Y-%m-%d')
                        print('  updated on', dt_obj)
                        #nums = int(n_start)
                        self.name_file = dt_obj.strftime('%Y%m%d')
                        self.now_date = dt_obj.strftime('%m/%d/%Y')
                        f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                        f_nameb = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'_death.pdf'
                if(not isfile(f_namea) ):
                    result = self.download4Website(a_address, f_namea)
                    print('  downloaded', result, f_namea)
                else:
                    print('  already exiting', f_namea)
                
            return f_namea
    ## look for page containing confirmed data
    def lookForConfirmedPage(self, pdfReader):
        for page in range(9, 12):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            # locate page
            n2_start = pageTxt.find('Published ')
            n2_end = pageTxt.find(' Data are provisional')
            s2_date = pageTxt[n2_start+10 : n2_end]
            s2_date = s2_date.replace('\n', '')
            print('33333333333', s2_date)
            # get time
            if(s2_date >= 0):
                dt_obj = datetime.datetime.strptime(s2_date, '%B %d, %Y')
                #nums = int(n_start)
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
                #return holw_data
        for page in range(9, 10):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            #print('-------------', pageTxt)
            d_start = pageTxt.find('deaths')
            #d_end = pageTxt.find('Oregon Public Health Division')
            d_list1 = pageTxt[d_start+6: ]
            #print('ddddddddddddddd', d_list1)

        for page in range(10, 11):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            #print('-------------', pageTxt)
            d_start = pageTxt.find('Novel Coronavirus (COVID-19)')
            d_end = pageTxt.find('Total ')
            d_list2 = pageTxt[d_start+28 : d_end]
            #print('ddddddddddddddd', d_list2)

        for page in range(10, 11):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            #print('-------------', pageTxt)
            d_start = pageTxt.find('a Total deaths')
            #d_end = pageTxt.find('Total ')
            d_list3 = pageTxt[d_start+17 : ]
            #print('ddddddddddddddd', d_list3)

        for page in range(11, 12):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            #print('-------------', pageTxt)
            d_start = pageTxt.find('(COVID-19)')
            #d_end = pageTxt.find('Total ')
            d_list4 = pageTxt[d_start+9 : ]
            #print('ddddddddddddddd', d_list4)

        for page in range(12, 13):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            #print('-------------', pageTxt)
            d_start = pageTxt.find('(COVID-19)')
            d_end = pageTxt.find('Total')
            d_list5 = pageTxt[d_start+9 : d_end]
            #print('ddddddddddddddd', d_list5)
        hole_list = d_list1 + d_list2 + d_list3 + d_list4 + d_list5
        #print('99999999999', hole_list)
        return hole_list

    ## paser data FL
    def dataReadConfirmed(self, f_name):
            print('  B.dataReadConfirmed on page 12-13', f_name)
            # step B: parse and open
            #print('    nnn', f_name)
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            # look for page containing confirmed data
            pageTxt = self.lookForConfirmedPage(pdfReader)
            #print('4444444', pageTxt)
            if(pageTxt == ''): return ([], pdfReader)
            page_tehTxt = pageTxt.split('\n')

            state_nam= []
            case= []
            case_num = 0
            death_num = 0
            death= []
            for d_li in page_tehTxt[9: ]:
                print('ffffffffffff ==', d_li)
                d_lisss= d_li.split(' ')
                if '/' in d_li:
                    if d_lisss[-1].isnumeric()  and d_lisss[-2].isnumeric():
                        case.append(d_lisss[-2])
                    
                        death.append(d_lisss[-1])
                        if len(d_lisss) >= 4:
                            state_nam.append(d_lisss[-4])
                        else: pass
                    elif d_lisss[0].isalpha():

                        if d_lisss[-1].isalpha():
                            state_nam.append(d_lisss[-1])
                        elif d_lisss[-2].isalpha():
                            state_nam.append(d_lisss[-2])
                        elif d_lisss[-3].isalpha():
                            state_nam.append(d_lisss[-3])  
                            case.append(d_lisss[-1])
                        elif d_lisss[-4].isalpha():
                            state_nam.append(d_lisss[-4])  
                            case.append(d_lisss[-2])
                            death.append(d_lisss[-1])

                        elif d_lisss[-1].isnumeric():
                                state_nam.append(d_lisss[-4])
                                death.append(d_lisss[-1])
                                case.append(d_lisss[-2])
                    
                else:
                    if len(d_lisss)== 3:
                        case.append(d_lisss[-2])
                        death.append(d_lisss[-1])
                    elif len(d_lisss) == 2:
                        case.append(d_lisss[-2])
                        death.append(d_lisss[-1])
                    elif len(d_lisss)== 1:
                        if d_lisss[0].isnumeric():
                            death.append(d_lisss[0])

            print('111111111111', state_nam)
            print('22222222222', case)
            print('333333333333', death)





            l_datas= []
            pdfReader = []
            return (l_datas, pdfReader)

 
   ## paser data FL
    def dataReadDeath4Pages(self, l_d_sort, f_name):
        print('  C.dataReadDeath4Pages from', f_name)
        # read death in county
        pdfFileObj = open(f_name, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        p_s, p_e = 1, 99
        #p_s, p_e = 31, 43 # page number in PDF for 4/19/2020
        #p_s, p_e = 30, 48 # page number in PDF for 4/24/2020
        case_total = 0
        for page in range(p_s-1, p_e+1):
		    pageObj = pdfReader.getPage(page)
		    pageTxt = pageObj.extractText()
		    l_pageTxt = pageTxt.split('\n')
		    if('line list of deaths in Florida residents' in l_pageTxt[0]): pass
		    else: break

		    #print('    pdf page is found', page)
		    state_machine = 100
		    for a_row in l_pageTxt:
		        #print('    dataReadDeath4Pages:', a_row)    
		        if(state_machine == 100):
		            if('today' in a_row):
		                state_machine = 200
		            if('provisional' in a_row):
		                state_machine = 200
		        elif(state_machine == 200 ):
		            if( a_row.lower().islower() ): pass
 		            else: continue
 		            #print('    dataReadDeath4Pages:', a_row) 
 		            #if( 'Unknown' in a_row ): continue
 		            if('Dade' in a_row): a_row = 'Miami-Dade'
 		            for a_d_row in l_d_sort:
 		                if a_d_row[0] in a_row:
 		                    a_d_row[2] += 1
 		                    case_total += 1
 		                    break
		    print('    found PDF page on', page+1, case_total)
		    #break
        l_d_sort[-1][2] = case_total
        return l_d_sort 


    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #Step A download and save as raw PDF files
            f_targeta = self.dataDownload(name_target)
            if(f_targeta == ''): return ([], name_target, date_target)
            #Step B read confirmed cases
            l_d_sort, pdfReader = self.dataReadConfirmed(f_targeta)
            #Step C read death cases
        

            return(l_d_sort, self.name_file, self.now_date)  

## end of file
