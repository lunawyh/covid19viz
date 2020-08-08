#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabOh.py
#
#	grab data from OH state websites
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
import requests
from lxml import html
import zipfile
import StringIO
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabNj(object):
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
    def downloadFileMa(self, link_name):
        urllib.urlopen(link_name)

    def save2File(self, l_data, csv_name):
        csv_data_f = open(csv_name, 'wb')
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
        # print('parseDfData', df.title)
        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                if (str(df.iloc[ii, jj]) == 'nan'):
                    a_case.append(0)
                    continue
                a_case.append(df.iloc[ii, jj])
            lst_data.append(a_case)
        # save to a database file
        if (fName is not None): self.save2File(lst_data, fName)
        return lst_data

    ## open a csv
    def open4File(self, csv_name):
        if (isfile(csv_name)):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else:
            return []
        return l_data
    ## open a csv
    def open4FileBuffer(self, csv_data):
        lst_data = []
        reader = csv.reader(csv_data)
        for row in reader:
            lst_data.append(row)
        return lst_data

    ## save to csv
    def saveLatestDateMa(self, l_data):
        print('  saveLatestDateMa ...')
        l_d_sort = sorted(l_data, key=lambda k: k[0], reverse=False)
        # find different date time
        l_date = []
        for a_item in l_d_sort:
            if('/' in a_item[0]): pass
            else: continue
            bFound = False
            for a_date in l_date:
                if(a_date in a_item[0]):
                    bFound = True
                    break
            if(not bFound):
                l_date.append(a_item[0])
        print('  data in days', len(l_date) )
        # generate all daily data
        l_daily_latest = []
        max_name_file = '20200101'
        for a_date in l_date:
            l_daily, n_name_file  = self.saveDataFromDlMa(l_d_sort, a_date, bDaily=False)
            if(n_name_file > max_name_file): 
                max_name_file = n_name_file
                l_daily_latest = l_daily
                dt_obj = datetime.datetime.strptime(n_name_file, '%Y%m%d')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
        return l_daily_latest

    def saveDataFromDlMa(self, l_data, a_test_date, bDaily=True):
        initial_test_date = None
        #
        l_overral = []
        #
        total_overral = 0
        total_overral_deaths = 0
        n_name_file = '20200101'
        for a_item in l_data:
            #if (a_test_date is None):
            if (initial_test_date is None and a_test_date in a_item[0]):
                initial_test_date = a_test_date
                dt_obj = datetime.datetime.strptime(a_test_date, '%m/%d/%Y')
                n_name_file = dt_obj.strftime('%Y%m%d')
                
            elif (a_test_date in a_item[0]):
                pass
            else:
                continue
            if('' == a_item[2]): a_item[2] = 0
            if('' == a_item[3]): a_item[3] = 0
            total_overral += int(a_item[2])
            total_overral_deaths += int(a_item[3])
            #
            l_overral.append([a_item[1], a_item[2], a_item[3]])
        l_overral.sort(key=lambda county: county[0])
        #
        l_overral.append(['Total', total_overral, total_overral_deaths])
        #
        if (not os.path.isdir(self.state_dir + 'data/')): os.mkdir(self.state_dir + 'data/')
        #
        self.save2File(l_overral,
                       self.state_dir + 'data/' + self.state_name.lower() + '_covid19_' + n_name_file + '.csv')

        return l_overral, n_name_file

    def downloadAndParseLink(self,link_address,fRaw):
        siteOpen = webdriver.Chrome()
        siteOpen.get(link_address)
        time.sleep(10)
        iframe = siteOpen.find_element_by_xpath("//iframe[@class='embedContainer stretch']")
        siteOpen.switch_to.frame(iframe)
        with open(fRaw, 'w') as f:
            f.write(siteOpen.page_source.encode('utf8'))
            f.close()
        downloadButtons = siteOpen.find_elements_by_xpath('//div[@class="external-html"]')
        allList = []
        totalPositives = 0
        totalDeaths = 0
        for dbutton in downloadButtons[2:len(downloadButtons)]:
            dStringList = dbutton.text.split()
            countyList = ''
            for w in dStringList:
                if w == "County":
                    break
                else:
                    countyList = str(countyList + " " + str(w))
            del dStringList[0:(dStringList.index('County')+1)]
            allList.append([countyList,int(str(dStringList[3]).replace(',','')),int(str(dStringList[6]).replace(',',''))])
            totalPositives = totalPositives + int(str(dStringList[3]).replace(',',''))
            totalDeaths = totalDeaths + int(str(dStringList[6]).replace(',', ''))
        allList.append(['Total',totalPositives,totalDeaths])
        siteOpen.close()
        return allList


    ## download a website
    def saveData(self, fRaw, sRaw):
        page_url = self.l_state_config[5][1]
        print('  download4Website ...')
        nj_info = self.downloadAndParseLink(page_url,fRaw)
        with open(sRaw, 'wb') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for c in nj_info:
                wr.writerow(c)
            myfile.close()
        print('  saved to', sRaw)

    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            s_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.saveData(f_name, s_name)
            return(data_csv, self.name_file, self.now_date)

## end of file
