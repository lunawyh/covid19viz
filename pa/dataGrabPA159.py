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
        l_dates = c_tree.xpath('//div//li//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        #print('   dddd', l_dates)
        a_address, b_address = '', ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('County case counts by date' in l_date.text_content() or 'See state report' in l_date.text_content()):
                #print('   sss', l_date) 
                a_address = 'https://www.health.pa.gov' + l_date.get('href')
                print('  find pdf 1 at', a_address)
            if('Death by county of residence' in l_date.text_content() or 'See state linelist' in l_date.text_content()):
                #print('   sss', l_date)
                b_address = 'https://www.health.pa.gov' + l_date.get('href')
                print('  find pdf 2 at', b_address)
                #break
        # get updated time
        l_dates = c_tree.xpath('//div//p//em/text()')  
        for l_date in l_dates:
            #
            if('Page last updated????' in l_date):
                print('   found ', l_date) 
                #s_date = '20200729'
                dt_obj = datetime.datetime.strptime(l_date.split(' ')[-1], '%m/%d/%Y')
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
            text = extract_text(f_namea)
            #print('  dataReadConfirmed', text)
            l_text = text.split('\n')
            l_cases1 = []
            l_cases1_sub = []
            for a_text in l_text:
                if(a_text == '' and len(l_cases1_sub)>0 ):
                    l_cases1.append(l_cases1_sub)
                    l_cases1_sub = []
                else:
                    l_cases1_sub.append(a_text)
            print('  l_cases1', len(l_cases1), len(l_cases1[0]))        
            for l_sub1 in l_cases1:
                print('  l_sub1', l_sub1[0])
            return []
            #state names, nam_list_no3 is the final state_name list
            n_start = text.find('ADAMS')
            n_end = text.find('Region')
            pre_nam_list_no1 = text[n_start:n_end]
            p1r2_nam_list = pre_nam_list_no1.split('\n')
            nam_list_no1= []
            state_nam = ''
            for aaa in p1r2_nam_list:
            	state_m =1 
            	#print('seeeee      j',aaa)
            	if len(aaa)== 2: pass
            	elif len(aaa) >= 3:
            	    nam_list_no1.append(aaa.lower())
            n2_start = text.find('MERCER')
            n2_end = text.find('YORK')
            pr_nam_list_no2 = text[n2_start:n2_end]
            #print('pre_2ndooooooooooooooooooo', pr_nam_list_no2)
            pr2_nam_list = pr_nam_list_no2.split('\n')
            #print('pre_2ndooooooooooooooooooo', pr_nam_list_no2)
            #return ([], None)
            nam_list_no2= []
            state_nam = ''
            for aaa in pr2_nam_list:
            	state_m =1 
            	#print('seeeee      j',aaa)
            	if len(aaa)== 2: pass
            	elif len(aaa) >= 3:
            	    nam_list_no2.append(aaa.lower())
            nam_list_no2.append('YORK')
            #print('33333333333333', nam_list_no2)
            nam_list_no3 = nam_list_no1 + nam_list_no2
            #print('finalooooooooooooooooooo', nam_list_no3)


            #state case numbers, num_list_no3 is the final state_case list
            m_start = text.find('Probable')
            m_end = text.find('PersonsWithNegativePCR')
            pre_num_list_no1 = text[m_start+8 :m_end]
            #print('111111111111111', pre_num_list_no1)
            pr1_num_list = pre_num_list_no1.split('\n')
            #print('333333333333', pr1_num_list)
            number_list1 = []
            for sss in pr1_num_list[2:]:
                if len(sss) >= 1:
                    number_list1.append(int(sss))
                    #print('22222222222', sss)
                else:
                    break
            m2_start = text.find('YORK')
            pre_num_list_no1 = text[m2_start+4 :]
            pr2_num_list = pre_num_list_no1.split('\n')
            #print('333333333333', pr2_num_list)
            number_list2 = []
            for sss in pr2_num_list[2:]:
                if len(sss) >= 1:
                    number_list2.append(int(sss))
                    #print('22222222222', sss)
                else:
                    break
            num_list_no3 = number_list1 +number_list2
            #print('4444444444444',num_list_no3 )


            #print('555555555555', len(nam_list_no3))
            #print('6666666666', len(num_list_no3))
            nam_num_list = np.vstack((nam_list_no3, num_list_no3, [0] * len(nam_list_no3))).T  



            #for Death data*************
            text2 = extract_text(f_nameb)
            print('lllllllllll', text2)



            #print('d222222222222222', death_p1r2_nam_list)
            d2_start = text2.find('Rate2')
            d2_end = text2.find('Montgomery')
            death_num_no1 = text2[d2_start:d2_end]
            death_p1r2_nam_list = death_num_no1.split('\n')
            #print('99999',death_p1r2_nam_list)
            d_number = []
            for d_line in death_p1r2_nam_list[44:-2]:
                if '.' in d_line: pass
                if d_line == '':continue
                d_number.append(int(d_line))

            
            d3_start = text2.find('851')
            d3_end = text2.find('828,604')
            death_num_no1 = text[d3_start:d3_end]
            d_list_no2 = death_num_no1.split('\n')
            print(';;;;;;',death_num_no1 )

            d_number2 = []
            for d_row in d_list_no2:
               if d_row != '':
                   d_number2.append(d_row)
               elif d_row == '': break



            death_case_final = d_number + d_number2
            print('66666666666', death_case_final)
            




            
            d_start = text2.find('Rate2')
            d_end = text2.find('Montgomery')
            death_nam_no1 = text[d_start:d_end]
            death_p1r2_nam_list = text2.split('\n')

            death_state_nam1 = []
            for ddd in death_p1r2_nam_list:
               if( ddd.lower().islower() ):
                   death_state_nam1.append(ddd)
               else: pass
            #print('d111111111111111',death_state_nam1 )
            death_state_nam = death_state_nam1[5: -3 ]

            death_state_nam_fin = []
            for dfd in death_state_nam:
               dfd.replace('\x0c', '')
               dfd.replace('\n', '')
               #print('..............', dfd)
               death_state_nam_fin.append(dfd.lower())
            print('d111111111111111',death_state_nam_fin )


            #print('lennnnn name', len(nam_list_no3))
            #print('lennnnn case', len(num_list_no3))
            print('lennnnn death', len(death_case_final))
            print('lennnnn death name', len(death_state_nam_fin))
            death_nam_num_list = np.vstack((death_state_nam_fin, death_case_final)).T
            print(' list death', death_nam_num_list)
            print(' list names', nam_num_list)

            #merge death_nam_num_list and nam_num_list            
            #final_nam_num_list = []
            for a_death in death_nam_num_list:
                for a_case in nam_num_list:                
                    if a_death[0] == a_case[0]:
                        a_case[2] = a_death[1]   
                        #final_nam_num_list.append(a_case)                
                        break
            print ('lllllllllllllll list merged', nam_num_list)
            
            return (nam_num_list)

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
            #Step C read death cases
            if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath4Pages(l_d_sort, f_targetb)
            else: l_d_all = []

            return(l_d_all, self.name_file, self.now_date)  

## end of file
