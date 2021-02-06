   
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
from datetime import date
import datetime 
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabMa(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config


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
    def parseDfData(self, df, df2, fName=None):
        # for data
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
        print('ccccccccccccccccc', lst_data[-14:])


        # for death
        (n_rows, n_columns) = df2.shape
        lst_deaths = []
        for ii in range(n_rows):
            a_case = []
            for jj in range(n_columns):
                #is the 'iloc(select rows and columns by number)' is ' nan(not a number)'
                if( str(df.iloc[ii, jj]) == 'nan'  ): 
                    a_case.append( 0 )
                    continue
                #a_case will have all the data from the 'data'
                a_case.append( df.iloc[ii, jj] )
            lst_deaths.append( a_case )
        print('aaaaaaaaaaaaaaa', lst_deaths[-14:])

        # save to a database file
        #if the file do not already exist
        if(fName is not None): self.save2File( lst_data, fName )
        #return the data that turned in to a ?? now you can use it?
        return lst_data


    ## save downloaded data to daily or overal data 
    def saveLatestDateTx(self, l_raw_data, name_file):
        l_overall = []
        offset = 0   # after 5/5 changed from 1 to 0
        total_cases, total_death = 0, 0
        l_overall.append(['County', 'Cases', 'Deaths'])
        for a_item in l_raw_data:
            if ('Confirmed' in a_item[1]): pass
            else: continue
            total_cases += a_item[2]
            total_death += a_item[3]
                
            l_overall.append([a_item[0], a_item[2], a_item[3]])  
        l_overall.append(['Total', total_cases, total_death])  
        print ('  Total', total_cases, total_death)
        print('333333333333333333333333333333333', l_overall)
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall
    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        l_data = []
        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            print('  sheet_names--------', xl_file.sheet_names)

            #for cacies
            nfx = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('County_Daily' in (sheet)):
                    print('  select sheet', sheet)
                    nfx = sheet
                    break
                else: 
                    print('sheet not found')
                    return []
            df = xl_file.parse( nfx )

        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            print('  sheet_names--------', xl_file.sheet_names)
            #for death
            nhk = ''
            for sheet in xl_file.sheet_names:  # try to find known name of sheet
                if ('CountyDeaths' in (sheet)):
                    print('  select sheet', sheet)
                    nhk = sheet
                    break
                else: 
                    print('sheet not found')
                    return []
            df2 = xl_file.parse( nhk )


            
            l_data = self.parseDfData(df, df2)
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
        l_dates = c_tree.xpath('//div//div//ul//li//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('COVID-19 Raw Data' in l_date.text_content()):
                a_address = 'https://www.mass.gov' + l_date.get('href')
                print(' $$$$$$$$$ find .xls at', a_address)
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
            # step C: read data file and convert to standard file and save
            lst_raw_data = self.open4Xlsx(f_n_total)

            lst_data = self.saveLatestDateTx(lst_raw_data, self.name_file)

            today = (date.today())
            self.name_file = today.strftime('%Y%m%d')
            self.now_date = today.strftime('%m/%d/%Y')
            return(lst_data, self.name_file, self.now_date)  
