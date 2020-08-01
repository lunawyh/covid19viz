#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabIl.py
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
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabIl(object):
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
            #print("l_data", len(l_data))
        else: return []
        return l_data
    ## save to csv
    def saveLatestDateIl(self, l_data):
        self.save2File(l_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        return l_data
    ## is validated or not 
    def isValidDate(self, src, dst, bDaily=True):
        if(bDaily):
            if( src in dst): return True
            else: return False
        else:
            if( 'Unknown' in src): return False
            if( 'Unknown' in dst): return False
            dt_obj = datetime.datetime.strptime(src, '%m/%d/%Y')
            dt_src = int( dt_obj.strftime('%Y%m%d') )
            dt_obj = datetime.datetime.strptime(dst, '%m/%d/%Y')
            dt_dst = int( dt_obj.strftime('%Y%m%d') )
            if( dt_src >= dt_dst): return True
            else: return False
    ## save downloaded data to daily or overal data 
    def saveDataFromDlOh(self, l_data, a_date, bDaily=True):
        l_daily = []
        total_daily = 0
        total_death = 0
        item_count_base = 6
        for a_item in l_data:
            if(a_item[3] in 'Total'): continue
            #
            if( self.isValidDate(a_date, a_item[3], bDaily=bDaily) ):
                pass
            else:
                continue
            total_daily += int( a_item[item_count_base] )            
            bFound = False
            for a_daily in l_daily:
                if(a_daily[0] in a_item[0]): 
                    bFound = True
                    a_daily[1] += int(a_item[item_count_base])
            if(not bFound):
                l_daily.append([a_item[0], int(a_item[item_count_base]), 0])
                #print([a_item[0], int(a_item[item_count_base]), 0])
        #print(' --------', self.now_date)
        for a_item in l_data:
            if(str(a_item[4]) in 'Total'): continue
            if(str(a_item[4]) in '0'): continue
            #
            if( self.isValidDate(a_date, a_item[4], bDaily=bDaily) ):
                bFound = False
                for a_daily in l_daily:                    
                    if(a_daily[0] in a_item[0]): 
                        bFound = True
                        a_daily[2] += int(a_item[item_count_base+1])
                if(not bFound):
                    l_daily.append([a_item[0], 0, int(a_item[item_count_base+1]) ])
                    #print([a_item[0], 0, int(a_item[item_count_base+1]) ])

                total_death += int( a_item[item_count_base+1] )            

        l_daily = sorted(l_daily, key=lambda k: k[0], reverse=False)
        l_daily.append(['Total', total_daily, total_death])
        # save to file
        dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
        self.name_file = dt_obj.strftime('%Y%m%d')
        self.now_date = dt_obj.strftime('%m/%d/%Y')
        if(bDaily): return l_daily
        else: type_dir = 'data/'
        if(not os.path.isdir(self.state_dir + type_dir) ): os.mkdir(self.state_dir + type_dir)
        self.save2File(l_daily, self.state_dir + type_dir+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        #print(' Total', total_daily, total_death, a_date)
        #print('   saved to', self.state_dir + type_dir+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        return l_daily

    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape, df.title, 
        print('  parseDfData', df.shape)
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
    ## download a website 
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

        return page_text
    ## download a website 
    def download4Website(self, fRaw):
        # save raw html file
        if(isfile(fRaw) ): 
            f = file(fRaw, 'r')
            page_content = f.read().decode('utf8')
        else:    
            page_content = self.saveWebsite(fRaw)
            print('  saved to', fRaw)
        # read updated data
        c_tree = html.fromstring(page_content)
        print('    look for updated date') 
        se_dates = c_tree.xpath('//span[@id="updatedDate"]/text()') # span id="updatedDate"
        for se_data in se_dates:
            if('2020' in se_data):
                print('      updated date', se_data)
                # update file name
                dt_obj = datetime.datetime.strptime(se_data, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
        print('    look for county data') 
        n_start = page_content.find('<tbody>')
        if(n_start >= 0): 
            l_county = []
            l_cases = []
            l_data = []
            n_end = page_content.find('</tbody>')
            #print('  page_content:', page_content[n_start:n_end+8])
            c_tree = html.fromstring(page_content[n_start:n_end+8])
            se_dates = c_tree.xpath('//a/text()') 
            print('      county', len(se_dates))
            for se_data in se_dates:
                #print('      ', se_data)
                l_county.append(se_data)
            se_dates = c_tree.xpath('//td/text()') 
            print('      cases', len(se_dates))
            for se_data in se_dates:
                #print('      ', se_data)
                l_cases.append(int(se_data))
            l_cases2 = np.reshape(l_cases, (len(l_cases)/3, 3)).T
            print('      cases reshaped', len(l_cases2))
            total_cases = (sum(map(int, l_cases2[1])))
            total_death = (sum(map(int, l_cases2[2])))
            
            l_data = np.vstack((np.array(l_county), l_cases2[1], l_cases2[2]))
            print('      l_data', len(l_data))
            return np.vstack((l_data.T, np.array(['Total', total_cases, total_death])))
        return []
    ## paser data CA
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            f_name = self.state_dir + 'data_html/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
            if(not os.path.isdir(self.state_dir + 'data_html/') ): os.mkdir(self.state_dir + 'data_html/')
            # step A: downlowd and save
            lst_raw_data = self.download4Website(f_name)
            # step B: parse and open
            #lst_raw_data = [] # self.open4File(f_name)
            # step C: convert to standard file and save
            lst_data = self.saveLatestDateIl(lst_raw_data)
            return(lst_data, self.name_file, self.now_date)  

## end of file
