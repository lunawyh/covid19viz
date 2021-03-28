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
import requests
from lxml import html
import json
import numpy as np
from selenium import webdriver  # https://selenium-python.readthedocs.io/installation.html
import time
import urllib.request
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabUT(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.name_file = ''
        self.now_date = ''

    ## save downloaded data to daily or overal data 
    def saveLatestDateUt(self, l_raw_data):
        l_overall = []
        
        l_overall.append(['County', 'Cases', 'Deaths'])
        for a_item in l_raw_data:
            l_overall.append(a_item)
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        return l_overall
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
        #print('  save2File', csv_name)
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data

    ## open a website 
    def open4WebsiteMain(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  open4WebsiteMain', csv_url)
        # save html file
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        #time.sleep(7)

        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        with open(fRaw, 'wb') as f:
            f.write(c_page.content)
        print('  saved to ', fRaw)
        # src="https://coronavirus-dashboard.utah.gov/overview.html"
        iframe = siteOpen.find_element_by_xpath('//iframe[@src="https://coronavirus-dashboard.utah.gov/overview.html"]')
        siteOpen.switch_to.frame(iframe)
        caseNumbers = siteOpen.find_elements_by_xpath('//tr[@role="row"]')
        full_list = []
        #print('nnnnnnnnnnnnn', caseNumbers)
        for l_date in caseNumbers[1:15]:
            dStringList = l_date.text.split()
            print('mmmmmmmm', dStringList)
            if len(dStringList) == 4:
                full_list.append([dStringList[0], dStringList[1], dStringList[3]])
            elif len(dStringList) == 5:
                if dStringList[1] == 'County':
                    full_list.append([dStringList[0], dStringList[2], dStringList[4]])
                elif dStringList[0] == 'Southeast': continue
                elif dStringList[0] == 'Southwest': continue
                else:
                    cbcb= dStringList[0]+' '+dStringList[1]
                    full_list.append([cbcb, dStringList[2], dStringList[4]])
            else:
                cbcb= dStringList[0]+' '+dStringList[1]
                full_list.append([cbcb, dStringList[3], dStringList[5]])

        print('full_listmmmmmmmmmmm', full_list)
        lst_data= []
        return full_list


    # southwest counties
    def open4WebsiteSwu(self, fRaw, lst_data):  	# https://swuhealth.org/covid/
        csv_url = self.l_state_config[5][3]
        print('  open4WebsiteMain', csv_url)
        print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
        # Opening the URL 
        driver = webdriver.Chrome() 
        driver.get(csv_url) 
  
        # Getting current URL source code 
        get_source = driver.page_source 
  
        # Printing the URL 
        #print(str(get_source))
        datas= str(get_source)
        n_start_1st = datas.find('Washington County:')
        n_end_1st = datas.find('See the descriptions for how')
        date_1st = datas[n_start_1st:n_end_1st]
        #print('kkkkkkkkkkkk', date_1st)
        data_2nd = date_1st.replace('<', '').replace('>', ' ').replace('/', '').replace('li', '').replace('strong', '').replace('ul', '').replace('em', '')
        data_3rd = data_2nd.split('   ')
        #print('qqqqqqqqqqqq', data_3rd)

        list_1st= []
        for data in data_3rd:
            rata = data.split(' ')
            #print('lllllllllllll', rata)
            list_1st.append(rata)

        list_a = []
        for lili in list_1st[0]:
            if lili == ' ': continue
            elif lili == '': continue
            else:
                list_a.append(lili)
        #print('aaaaaaaaaaaaa', list_a)
        list_b = []
        for lili in list_1st[1]:
            if lili == ' ': continue
            elif lili == '': continue
            else:
                list_b.append(lili)
        #print('aaaaaaaaaaaaa', list_b)
        list_c = []
        for lili in list_1st[2]:
            if lili == ' ': continue
            elif lili == '': continue
            else:
                list_c.append(lili)
        #print('aaaaaaaaaaaaa', list_c)
        list_d = []
        for lili in list_1st[3]:
            if lili == ' ': continue
            elif lili == '': continue
            else:
                list_d.append(lili)
        #print('aaaaaaaaaaaaa', list_d)
        list_e = []
        for lili in list_1st[4]:
            if lili == ' ': continue
            elif lili == '': continue
            else:
                list_e.append(lili)
        #print('aaaaaaaaaaaaa', list_e)

        abcde_list=['list']
        abcde_list=[(list_a)]+[(list_b)]+[(list_c)]+[(list_d)]+[(list_e)]
        #print(';;;;;;;;;;;;;;;;;;;;', abcde_list)

        final_list = []
        list1 = list_1st[0]+list_1st[1]
        final_list.append([list1[0], list1[2].replace('(', '').replace(',', ''), list1[4].replace('cases),', '')])
        list2 = list_1st[2]+list_1st[3]
        final_list.append([list2[0], list2[2].replace('(', '').replace(',', ''), list2[5]])
        list3 = list_1st[4]+list_1st[5]
        final_list.append([list3[0], list3[2].replace('(', '').replace(',', ''), list3[5]])
        list4 = list_1st[6]+list_1st[7]
        final_list.append([list4[0], list4[2].replace('(', '').replace(',', ''), list4[5]])
        list5 = list_1st[8]+list_1st[9]
        final_list.append([list5[0], list5[2].replace('(', '').replace(',', ''), list5[5]])
        '''
        final_list= []
        for cdcd in abcde_list:

            if cdcd[0] == 'Washington':
                final_list.append([cdcd[0], cdcd[11].replace('=', '').replace(',', ''), cdcd[13]])
            elif cdcd[0] == 'Iron':
                final_list.append([cdcd[0], cdcd[11].replace('=', '').replace(',', ''), cdcd[13]])
            elif cdcd[0] == 'Kane':
                susu =  cdcd[10].split('=')
                final_list.append([cdcd[0], susu[-1].replace(',', ''), cdcd[12]])
            elif cdcd[0] == 'Beaver':
                susu =  cdcd[10].split('=')
                final_list.append([cdcd[0], susu[-1].replace(',', ''), cdcd[12]])
            elif cdcd[0] == 'Garfield':
                susu =  cdcd[10].split('=')
                final_list.append([cdcd[0], susu[-1].replace(',', ''), cdcd[12]])
        '''
        '''
        sysy= cdcd[11].split('=')
        print('mmmmm', sysy)
        final_list.append([cdcd[0], sysy[-1].replace(',', ''), cdcd[12]])
        '''
        print('ffffffffffffffffff', final_list)
        return final_list

    def open4WebsiteSeu(self, fRaw, lst_data):
        csv_url = self.l_state_config[5][2]
        print('  open4WebsiteSeu', csv_url)
        # save html file
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(7)

        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        with open(fRaw, 'wb') as f:
            f.write(c_page.content)
        print('  saved to ', fRaw)


        iframe = siteOpen.find_element_by_xpath('//iframe[@title="htmlComp-iframe"]')
        siteOpen.switch_to.frame(iframe)

        caseNumbers = siteOpen.find_elements_by_xpath('//tr[@style="height: 48px;"]')
        full_list = []
        #print('nnnnnnnnnnnnn', caseNumbers)
        for l_date in caseNumbers:
            dStringList = l_date.text.split()
            #print('mmmmmmmm', dStringList)
            full_list.append([dStringList[0], dStringList[2], 0])
        print('kkkkkkkkkkk', full_list)

        return full_list

 
    
    ## paser data Ut
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            f_name = self.state_dir + 'data_html/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')

            # step A: downlowd and save
            lst_raw_data = self.open4WebsiteMain(f_name)
            lst_raw_data2 = self.open4WebsiteSeu(f_name, lst_raw_data)
            lst_raw_data3 = self.open4WebsiteSwu(f_name, lst_raw_data)

            lst_raw_data4 = np.concatenate((lst_raw_data2, lst_raw_data3), axis=0)
            lst_raw_data5 = np.concatenate((lst_raw_data, lst_raw_data4), axis=0)

            anum = 0
            adeath = 0
            for lst in lst_raw_data5:
                anum += int(lst[1])
                print('1111111111111111', lst[1])
                adeath += int(lst[2])
                
            raw_total_data = (['Total', anum, adeath])
            print('llllllllll', raw_total_data)
            lst_raw_data6 = np.append(lst_raw_data5, [['Total', anum, adeath]], axis=0)

            # step B: parse and open
            lst_data = self.saveLatestDateUt(lst_raw_data6)

            lst_data= []
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all



