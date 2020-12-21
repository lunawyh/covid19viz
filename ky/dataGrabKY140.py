   
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
import PyPDF2
from datetime import date
import re 
import numpy as np
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabKY(object):
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
        return lst_data
        

    ## open a pdf 
    def open4ppdf(self, pdf_name):
        pdfFileObj = open(pdf_name, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for page in range(2,3):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
        #print('...................', pageTxt)

        n_start = pageTxt.find('Jefferson')
        n_end = pageTxt.find('COVID-19 New Cases')
        pagesss = pageTxt[n_start: n_end ]
        pageTxt = pagesss.split('%')
        data_txt= []
        for a_ll in pageTxt:
            if a_ll =='': continue
            else: data_txt.append(a_ll.replace(',', ''))
        #print('//////////////', data_txt)

        f_cases = []
        for a_dt in data_txt:
            if 'Jefferson' in a_dt:
                f_cases.append(a_dt[: -4 ])
            else:
                f_cases.append(a_dt[:-3])

        g_cases=f_cases[:-1]
        #print('aaaaaaaaaaaaaa', g_cases)

        c_cases= []
        for ff in g_cases:
            #print('**********', ff)
            temp = re.compile("([a-zA-Z]+)([0-9]+)") 
            res = temp.match(ff).groups() 
            #print('~~~~~~~~~~~~~~~`' , (res))
            c_cases.append(res)
        #print('::::::::::::::::::', c_cases)

        a_cases= []
        for aa in c_cases:
            print('^^^', aa)

            for bb in aa:
                #print('&&', bb)
                a_cases.append(bb.replace('CountyCasesPercent', ''))

        #print('@@@@@@@@@@@@@222', a_cases)
        #-----------------------got the case list-----------now find the death list-------------
        for page in range(4,5):
            pageObj = pdfReader.getPage(page)
            pageTxt2 = pageObj.extractText()
        #print('...................', pageTxt2)

        n_start = pageTxt2.find('Jefferson')
        n_end = pageTxt2.find('COVID-19 New Cases')
        pagesss = pageTxt2[n_start: n_end ]
        pageTxt2 = pagesss.split('%')
        a_data_txt= []
        for a_ll in pageTxt2:
            if a_ll =='': continue
            else: a_data_txt.append(a_ll.replace(',', ''))
        #print('//////////////', a_data_txt)

        x_cases = []
        for a_dt in a_data_txt:
            if 'Jefferson' in a_dt:
                x_cases.append(a_dt[: -4 ])
            else:
                x_cases.append(a_dt[:-3])

        z_cases=x_cases[:-1]
        #print('aaaaaaaaaaaaaa', z_cases)

        w_cases= []
        for ff in z_cases:
            #print('**********', ff)
            temp = re.compile("([a-zA-Z]+)([0-9]+)") 
            res = temp.match(ff).groups() 
            #print('~~~~~~~~~~~~~~~`' , (res))
            w_cases.append(res)
        #print('::::::::::::::::::', w_cases)

        q_cases= []
        for aa in w_cases:
            print('^^^', aa)
            for bb in aa:
                #print('&&', bb)
                q_cases.append(bb)

        #print('!!!!!!!!!!!!!!!!!!!!!!!!111111', q_cases)


        #finished death list, now group them-------------------------------------------------
        a_l_cases = np.reshape(a_cases, (len(a_cases)/2, 2)).T
        b_l_cases = np.reshape(q_cases, (len(q_cases)/2, 2)).T

        l_data = np.vstack((a_l_cases[0], a_l_cases[1], b_l_cases[1])).T
        #print('+++++++++++++',  l_data)


        case = 0
        death = 0
        for a_da in l_data:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(l_data, [['Total', case, death]], axis=0)
        #print(l_cases3)   

        return l_cases3


    ## $^&&
    def open4pdf(self, name_file):
        csv_url = self.l_state_config[5][1]
        print('  #$$search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//ul//li//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('KY COVID-19 Daily Report' in l_date.text_content()):
                print('///////////////', l_date.get('href'))
                a_address = l_date.get('href')
                #https://www.michigan.gov/documents/coronavirus/Cases_and_Deaths_by_County_693160_7.xlsx
                print(' $$$$$$$$$ find .xls at', a_address)
                break
        return a_address
    ## paser data CA
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            #self.open4pdf(name_file)
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            f_n_total = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # 
            urllib.urlretrieve(urlData, f_n_total)
            #urllib.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            lst_raw_data = self.open4ppdf(f_n_total)
            self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(lst_raw_data, self.name_file, str(today))  



