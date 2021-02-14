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
import os, subprocess
import itertools
from pdfminer.high_level import extract_text  # pip install pdfminer.six
 
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabPA(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''


    ## open a website ***********
    def open4Website(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        # get pdf address
        l_dates = c_tree.xpath('//ul//ul//li//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('   dddd', l_dates)
        a_address, b_address = '', ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('County case counts by date' in l_date.text_content() or 'See state report' in l_date.text_content()):
                #print('   sss', l_date) 
                a_address = 'https://www.health.pa.gov' + l_date.get('href')
                print('  find pdf 1 at', a_address)
                f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                urllib.urlretrieve(a_address, f_n_total)
            if('Death by county of residence' in l_date.text_content() or 'See state linelist' in l_date.text_content()):
                #print('   sss', l_date)
                b_address = 'https://www.health.pa.gov' + l_date.get('href')
                print('  find pdf 2 at', b_address)
                #break
        # get updated time
        l_dates = c_tree.xpath('//p/text()')  
        for l_date in l_dates:
            #
            if('This information has been extracted from death' in l_date):
                print('   found ', l_date) 
                #s_date = '20200729'
                dt_obj = datetime.datetime.strptime(l_date.split(' ')[-1].replace('.', '' ), '%m/%d/%Y')
                #print('  updated on', dt_obj)
                #nums = int(n_start)
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
        return a_address, b_address

 

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
    def dataReadConfirmed(self, f_namea, f_nameb):
            print('  B.dataReadConfirmed on page 1', f_namea)
            # step B: parse and open
            #---------------------------case-------------------------
            text = extract_text(f_namea)
            l_text = text.split('\n')
            #print('  ...................222222', l_text)
            
            #state names for cases
            l_cases1 = []
            for aaa in l_text[267:315]:
                if len(aaa) <= 2: continue
                else:
                    l_cases1.append(aaa) 
            state_name= l_text[1:43] + l_cases1
            full_name = []
            #print('vvvvvvvvvvvvvvvvvvvvv', state_name)
            for stst in state_name:
                sasa = stst[0] + stst[1:].lower()
                #print('tttttttttttttt', sasa)
                full_name.append(sasa)

            state_cases = l_text[93:135] + l_text[316:341]
            #print('llllllllllllllllllll', state_cases)


            #cases death-------------------------
            text2 = extract_text(f_nameb)
            l_text2 = text2.split('\n')
            #print('  ...................222222', l_text2)
            state2_cases = l_text2[50:91] + l_text2[233:259]

            cases_death = []
            for caca in state2_cases:
                cvcv= caca.replace(',', '')
                cases_death.append(cvcv)
           #-----------------------------------
            l_data = np.vstack((full_name, state_cases, cases_death)).T
            #print('777777777777', l_data)


            case = 0
            death = 0
            for a_da in l_data:
                case += int(a_da[1])
                death += int(a_da[2])
            l_cases3 = np.append(l_data, [['Total', case, death]], axis=0)
            print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
            return l_cases3
            #return (finall_list)

    ## paser data FL************
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            #f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            #f_nameb = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'_death.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): 
                a_address, b_address = self.open4Website('')
                #print(',,,,,,,,,,,,,,,,,,,,', a_address)
                if(a_address == ''): 
                    print ('    No address of downloading PDF is found')
                    return ('', '')
                # download now
                f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                f_nameb = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'_death.pdf'
                if(not isfile(f_namea) ):
                        result = self.download4Website(a_address, f_namea)
                        print('  downloaded', result, f_namea)
                else:
                        print('  already exiting', f_namea)
                if(not isfile(f_nameb) ):
                        result = self.download4Website(b_address, f_nameb)
                        print('  downloaded', result, f_nameb)
                else:
                        print('  already exiting', f_nameb)

               
            return f_namea, f_nameb

    ## download a website ********
    def download4Website(self, csv_url, fRaw):
        #csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True


    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #Step A download and save as raw PDF files
            f_targeta, f_targetb = self.dataDownload(name_target)
            if(f_targeta == ''): return ([], name_target, '')
            #Step B read confirmed cases
            l_d_sort = self.dataReadConfirmed(f_targeta, f_targetb)
            #print('666666666666666', l_d_sort)
            #Step C read death cases
            if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath4Pages(l_d_sort, f_targetb)
            else: l_d_all = []
            #print('7777777777', l_d_all)
            anum = 0
            adeath = 0
            for a_ll in l_d_all:
                anum += int(a_ll[1])
                adeath += int(a_ll[2])

            l_d_all = np.append(l_d_all, [['Total', anum, adeath]], axis=0)

            return(l_d_all, self.name_file, self.now_date)  

## end of file
