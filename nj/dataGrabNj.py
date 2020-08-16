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

    def downloadAndParseLink(self,link_address,fRaw):
        siteOpen = webdriver.Chrome()
        siteOpen.get(link_address)
        time.sleep(10)
        iframe = siteOpen.find_element_by_xpath("//iframe[@class='embedContainer stretch']")
        siteOpen.switch_to.frame(iframe)
        with open(fRaw, 'w') as f:
            f.write(siteOpen.page_source.encode('utf8'))
            f.close()
        caseNumbers = siteOpen.find_elements_by_xpath('//div[@class="external-html"]')
        allList = []
        allList.append(['County','Cases','Deaths'])
        totalPositives = 0
        totalDeaths = 0
        for cNum in caseNumbers[2:len(caseNumbers)-1]:
            dStringList = cNum.text.split()
            countyString = ''
        for dbutton in caseNumbers[2:]:
            dStringList = dbutton.text.split()
            countyList = ''
            bFound = False
            for w in dStringList:
                if w == "County":
                    bFound = True
                    break
                else:
                    countyString = str(countyString + " " str(w))
                    countyList = str(countyList + " " + str(w))
            if(not bFound): continue
            del dStringList[0:(dStringList.index('County')+1)]
            allList.append([countyString,int(str(dStringList[3]).replace(',','')),int(str(dStringList[6]).replace(',',''))])
            totalPositives = totalPositives + int(str(dStringList[3]).replace(',',''))
            totalDeaths = totalDeaths + int(str(dStringList[6]).replace(',', ''))
        allList.append(['Total',totalPositives,totalDeaths])
        print('  downloadAndParseLink', len(allList), len(allList[0]))
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
        return nj_info

    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            s_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_csv = self.saveData(f_name, s_name)
            print('  total list of cases', len(data_csv))
            return(data_csv, self.name_file, self.now_date)

## end of file
