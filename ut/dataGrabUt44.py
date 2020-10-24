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
        if(not isfile(fRaw) ): 
            urllib.urlretrieve(csv_url, fRaw)

        # read updated date
        print('  read date')
        if( isfile(fRaw) ): 
            with open(fRaw, 'r') as file:
                page_content = file.read()
        else: return []
        lst_data = []
        c_tree = html.fromstring(page_content)
        u_dates = c_tree.xpath('//p/text()')
        for l_date in u_dates:
            if('Report Date: ' in l_date):
                #print('    data is updated,', l_date)
                n_start = l_date.find(l_date)
                s_date = l_date[n_start:].split(':')
                #print ('    date:', s_date[1]) # an example,  May 24, 2020
                mdy_date = s_date[1].split(',')
                md_date = mdy_date[0].split(' ')
                # Only use first 3 letters of month name
                dt_obj = datetime.datetime.strptime(md_date[1][:3]+md_date[2]+mdy_date[1], "%b%d %Y")
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                #print('    name_file is updated:', self.name_file)
                break
        # read tables
        print ('  read data table of counties')
        # read 1st table: Overall Confirmed COVID-19 Cases by County
        u_scripts = c_tree.xpath('//script/text()')
        for l_script in u_scripts:
            if('Jurisdiction' in l_script and 'Cases' in l_script and 'Deaths' in l_script):
                #print('  ###############################################  counties data:', l_script)
                lst_data = self.parseJsonString(l_script)
                
        return lst_data
    ## parse from exel format to list 
    def parseJsonString(self, j_str):
        print('    parseJsonString')
        lst_data = []
        j_data = json.loads(j_str.replace(' County', ''))  # is a json string
        l_raw_data = j_data['x']['data']		# fixed keys
        #print('  ############################################### ', l_raw_data)

        l_raw_data = l_raw_data[:2] + l_raw_data[3:]  	# remove 3rd column of Hospitalizations


        lst_data = zip(*l_raw_data)			# transpose the matrix
        #print('seeeeeeeeeee', lst_data)        
        #print('    counties', len(lst_data))
        lst_dateee = lst_data[:5] + lst_data[7:]
        #print('$$$$$$$$$$44', lst_dateee)
        return lst_dateee

    # southwest counties
    def open4WebsiteSwu(self, fRaw, lst_data):  	# https://swuhealth.org/covid/
        csv_url = self.l_state_config[5][3]
        #print('  open4WebsiteSwu', csv_url)
        
        # save html file, can not use urllib.urlretrieve
        r = requests.get(csv_url)
        fRaw = fRaw.replace('.html', 'swu.html')
        with open(fRaw, 'wb') as f:
            f.write(r.content)

        # read updated date
        print('  read date')
        if( isfile(fRaw) ): 
            with open(fRaw, 'r') as file:
                page_content = file.read()
        else: return []
        lst_data = lst_data[0:-1]  # remove total row
        lst_data_sw = []
        # reset subtotal of SW
        for a_item in lst_data:
            if('Southwest Utah' in a_item[0]):
                lst_data_sw.append(['Southwest Utah', 0, a_item[2]])
            else:
                lst_data_sw.append(a_item)
        
        #-----------------------------------get date----------
        c_tree = html.fromstring(page_content)
        print('    look for updated date and county data')
        sw_dates = c_tree.xpath('//ul//li//strong/text()')   # ('//div[@class="col-xs-12 button--wrap"]')
        #sw_dates = c_tree.xpath('//ul//li/text()')  
        print('11111111111', sw_dates)
        for sw_data in sw_dates:
            if('COVID-19 CASES' in sw_data):
                l_detail1 = sw_data.split('(')
                print('      ..............updated date', l_detail1)
        #-----------------------------------get data----------
        c_tree = html.fromstring(page_content)
        print('    look for county data')
        sw_dates2 = c_tree.xpath('//ul//li/text()')
        print('222222222222222', sw_dates2)
        death= []
        total_death =0
        for sw_data in sw_dates2:
            
            if('recovered,' in sw_data):
                start = sw_data.find('recovered,')
                data = sw_data[start: ]

                dea = data.split(' ')
                print('33333333333333', dea)
                if len(dea) >= 3:
                    death.append(int(dea[1]))
                    total_death += int(dea[1])
                    print('333333', death)

        
        sw_dates3 = c_tree.xpath('//ul//li//strong/text()')
        num = []
        name = []
        total_confirmed = 0
        for sw_data in sw_dates3:
            print('4444444444444444', sw_data)
            if(' County:' in sw_data):
                print('..........', sw_data)
                sw_s = sw_data.split(' ')
                print(',,,,,,,,,', sw_s)
                name.append(sw_s[0])
                num.append(int(sw_s[2].replace(',', '')))



        #print('8888888', name)
        #print('8888888', num)
        #print('8888888', death)
        l_data = np.vstack((name, num, death)).T 
        #print('ppppppp', l_data)        
        # calculate total------------------------------------------------
        #total = (['Total', total_confirmed, total_death])
        #l_data= np.append(l_data, total)

        return l_data

    def open4WebsiteSeu(self, fRaw, lst_data):
        csv_url = self.l_state_config[5][2]
        print('  open4WebsiteSeu', csv_url)
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(10)
        # county
        countyNames = siteOpen.find_elements_by_xpath('//tr//th//div[@class="_3-_lH"]')
        print('==================', countyNames)
        for c_name in countyNames:
            dStringList = c_name.text  #.split()
            print('4444444444444444444444444', dStringList)
            print('  countyNames', dStringList, len(dStringList))
            break
        # cases
        caseNumbers = siteOpen.find_elements_by_xpath('//div[@class="_3-_lH"]')
        for case_num in caseNumbers:
            dStringList_num = case_num.text.split()
            print('77777777777777', dStringList_num)
            print('  caseNumbers', dStringList_num, len(dStringList))
            break

        time.sleep(3)
        siteOpen.close()

        name= []
        for dS in dStringList:
            if dS == 'Cases': continue
            if dS == 'County': continue
            if dS == 'Totals': continue
            else:
                name.append(dS)
        #print('5555555............', name)

        case = []
        for i in range(0, 10):
            if dStringList_num[i] == 'Total':
                case.append(int(dStringList_num[i+1]))
                case.append(int(dStringList_num[i+2]))
                case.append(int(dStringList_num[i+3]))
        #print('666666666', case)

        death = []
        for i in range(0, 40):
            if dStringList_num[i] == 'Deaths':
                death.append(int(dStringList_num[i+1]))
                death.append(int(dStringList_num[i+2]))
                death.append(int(dStringList_num[i+3]))
        #print('777777777', death)

        l_data = np.vstack((name, case, death)).T 
        return l_data

    # southeast counties
    def open4WebsiteSeu01(self, fRaw, lst_data):	# https://www.seuhealth.com/covid-19
        #------------------------------------open website and find date------
        csv_url = self.l_state_config[5][2]
        #print('  open4WebsiteSeu', csv_url)
        # save html file
        fRaw = fRaw.replace('.html', 'seu.html')
        if(not isfile(fRaw) ): 
            urllib.urlretrieve(csv_url, fRaw)

        # read updated date
        #print('  read date')
        if( isfile(fRaw) ): 
            with open(fRaw, 'r') as file:
                page_content = file.read()
        else: return []
        lst_data = lst_data[0:-1]  # remove total row
        lst_data_se = []
        # reset subtotal of SE
        for a_item in lst_data:
            if('Southeast Utah' in a_item[0]):
                lst_data_se.append(['Southeast Utah', 0, a_item[2]])
            else:
                lst_data_se.append(a_item)

    
        #----------------------------------------find data ---------------------
        #print('  download4Website', csv_url)
        '''
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(2)
        page_text = driver.page_source

        c_tree = html.fromstring(page_text)
        l_text_data = c_tree.xpath('//div//div//div//p//span/text()')
        a_data = []
        #print('ddddddddd', l_text_data[0])
        for a_not in l_text_data:
              if 'County'  in a_not:
                  #print('111111111', a_not)
                  if 'death' in a_not:
                      #print('22222222', a_not)
                      a_data.append(a_not)
        a_data = a_data[:3]
        carbon_c = a_data[0].split(' ')
        emery_c = a_data[1].split(' ')
        grand_c = a_data[2].split(' ')
        #print('ggggggggg', grand_c)
        ccc= carbon_c[2].replace(u'\xa0', ' ').encode('utf-8')
        eee= emery_c[2].replace(u'\xa0', ' ').encode('utf-8')
        ggg= grand_c[2].replace(u'\xa0', ' ').encode('utf-8')

        ccc= ccc.split(' ')
        eee= eee.split(' ')
        ggg= ggg.split(' ')
        l_data1 = np.vstack((carbon_c[0], ccc[0], carbon_c[6])).T 
        l_data2 = np.vstack((emery_c[0], eee[0], emery_c[6])).T 
        l_data3 = np.vstack((grand_c[0], ggg[0], grand_c[8])).T 
        #print('11111111111', l_data1)
        #print('2222222222', l_data2)
        #print('3333333333', l_data3)
        total_confirmed = int(ccc[0])+int(eee[0])+int(ggg[0])
        total_death= int(carbon_c[6]) + int(emery_c[6]) + int(grand_c[8])
        #------------------------------------------------------------
        lst_data_se= []
        lst_data_se= np.append(lst_data_se, l_data1)
        lst_data_se= np.append(lst_data_se, l_data2)
        lst_data_se= np.append(lst_data_se, l_data3)
        yoyal= (['Total', total_confirmed, total_death])
        lst_data_se= np.append(lst_data_se, yoyal)
        lst_data_se = np.reshape(lst_data_se, (len(lst_data_se)/3, 3)).T
        l_data = np.vstack((lst_data_se[0], lst_data_se[1], lst_data_se[2])).T 
        #print('*******', l_data)
        '''
        return l_data
    
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
            return(lst_data, self.name_file, self.now_date)  #add in l_d_all



