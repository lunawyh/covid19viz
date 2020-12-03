   
#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabTx.py
#
#	grab data from TX state websites
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
import urllib
import ssl
import datetime 
from lxml import html
import requests
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import numpy as np
import datetime 
# ==============================
#================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabCA(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.now_date = ''
        self.name_file = ''


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


    def saveWebsite(self, fRaw):
        csv_url = self.l_state_config[5][1]
        print('  download4Website', csv_url)
        driver = webdriver.Chrome()
        driver.get(csv_url)
        time.sleep(5)
        driver.find_elements_by_link_text('By County')[0].click()
        '''do we need to add 
        driver.find_elements_by_link_text('All')[0].click() 
        ? '''
        #time.sleep(1)
        #driver.find_element_by_id("input-filter").send_keys("Alexander")
        time.sleep(1)
        #driver.find_element_by_id("myDiv").click()
        #ActionChains(driver).double_click(qqq).perform()
        driver.execute_script('createTableRows(99);')
        time.sleep(1)
        page_text = driver.page_source
        with open(fRaw, "w") as fp:
            fp.write(page_text.encode('utf8'))
        time.sleep(1)
        driver.quit()  # close the window
        #f = file('test', 'r')
        #print f.read().decode('utf8')


    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        #print('parseDfData', df.title)
        lst_data = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                #is the 'iloc(select rows and columns by number)' is ' nan(not a number)'
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )

                    continue
                #a_case will have all the data from the 'data'
                a_case.append( df.iloc[ii, jj] )
            lst_data.append( a_case )
        # save to a database file
        #if the file do not already exist
        if(fName is not None): self.save2File( lst_data, fName )
        #return the data that turned in to a ?? now you can use it?
        print(';;;;;;;;;;;', lst_data)
        return lst_data
    ## save downloaded data to daily or overal data 
    def saveLatestDateTx(self, l_raw_data, name_file):
        l_overall = []
        state_name =[]
        state_case = []
        for a_raw in l_raw_data:
            if '*' in a_raw[0]: continue
            if '^' in a_raw[0]: continue
            if 'County' in a_raw[0]: continue
            else: 
                state_name.append(a_raw[0])
                state_case.append(a_raw[7])
        print('111111111', state_name)
        print('111111111', state_case)
        zeros= [0]*len(state_name)
        l_data = np.vstack((state_name, state_case, zeros)).T 

        total_num = 0
        total_death = 0
        for a_ll in l_data:
            total_num += int(a_ll[1])

        l_cases3 = np.append(l_data, [['Total', total_num, total_death]], axis=0)
        print(';;;;;;;;;;;;;;;;', l_cases3)
        self.save2File(l_cases3, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')


        return l_cases3
    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        l_data = []
        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            print('  sheet_names', xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('County Tiers and Metrics' in (sheet)):
                    print(' --------------- select sheet', sheet)
                    nfx = sheet
                    break
            if nfx == '': # if not found, use the 1st sheet
                if(len(xl_file.sheet_names) > 0): nfx = xl_file.sheet_names[0]
                else: return []
            df = xl_file.parse( nfx )
            
            l_data = self.parseDfData(df)
            #print('  l_data', l_data)

        return l_data

    ## $^&&
    def open4excel(self, name_file):
        csv_url = self.l_state_config[5][1]
        print('  #$$search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//li//p//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        a_address = ''
        for l_date in l_dates:
            print(l_date.get('href'))
            if('California Blueprint Data Chart' in l_date.text_content()):
                a_address = 'https://www.cdph.ca.gov' + l_date.get('href')
                #https://www.michigan.gov/documents/coronavirus/Cases_and_Deaths_by_County_693160_7.xlsx
                print(' $$$$$$$$$ find .xls at', a_address)
                break

        l_day = c_tree.xpath('//hs/text()')
        print('----------', l_day)
        for l_date in l_day:
            print('*******************', l_date)
            if('Updates as of' in l_date):
                a_date = l_date.replace('Updates as of ', '').replace(' ', '').replace(',', '')
                print('  ....................a_date', a_date)
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break

        return a_address



    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
        self.name_file = name_file
        # step A: read date
        urlData = self.open4excel(name_file)
        #self.open4excel(name_file)
        # step B: save raw
        f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
        f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.xlsx'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
        # 
        urllib.urlretrieve(urlData, f_n_total)
        urllib.urlretrieve(self.l_state_config[5][1], f_name)
        # step C: read data file and convert to standard file and save
        lst_raw_data = self.open4Xlsx(f_n_total)

        lst_data = self.saveLatestDateTx(lst_raw_data, self.name_file)




        csv_url = self.l_state_config[5][1]
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_day = c_tree.xpath('//hs/text()')
        print('----------', l_day)
        for l_date in l_day:
            print('*******************', l_date)
            if('Updates as of' in l_date):
                a_date = l_date.replace('Updates as of ', '').replace(' ', '').replace(',', '')
                print('  ....................a_date', a_date)
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break

        return(lst_data, self.name_file, self.now_date)  


