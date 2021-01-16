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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabMa(object):
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
        urllib.urlopen(link_nameg)

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
        print('lst_data;;;;;;;;;;;;;;;;;;;;;;;', lst_data)
        # save to a database file
        if (fName is not None): self.save2File(lst_data, fName)
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

    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        print('open4Xlsx')
        l_data = []
        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            print('  sheet_names', xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('County_Weekly' in (sheet)):
                    print('  select sheet', sheet)
                    nfx = sheet
                    break
                else: 
                    print('sheet name not found')
                    return []
            df = xl_file.parse( nfx )
            
            l_data = self.parseDfData(df)
            #print('  l_data', l_data)

        return l_data



    def downloadAndParseLink(self,fRaw):
        htmlPage = requests.get(fRaw)
        tree = html.fromstring(htmlPage.content)
        division = tree.xpath('//p//a/@href')
        link = division[0]
        link = "https://www.mass.gov" + link
        print("  get link: " + link)
        l_date = link.split('/')[4].split('-')
        print("  get date: ", l_date[4:])
        return link

    ## download a website
    def download4Website(self, fRaw):
        xlsx_url = self.l_state_config[5][1]
        # get the updated date from the website
        # update self.name_file and self.now_date
        print('  download4Website ...')
        # save csv file
        data_xlsx = self.downloadAndParseLink(xlsx_url)
        return data_xlsx

    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            #l_name = self.state_dir + 'data_raw/'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            data_xlsx = self.download4Website(f_name)
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            urllib.urlretrieve(data_xlsx, f_n_total)
            # step B: parse and open
            lst_raw_data = self.open4Xlsx(data_xlsx)
            # step C: convert to standard file and save
            lst_data = self.saveLatestDateMa(lst_raw_data)
            print(lst_data)
            return(lst_data, self.name_file, self.now_date)

## end of file
