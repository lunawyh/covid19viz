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
<<<<<<< HEAD
<<<<<<< HEAD
import urllib
import ssl
from lxml import html
import requests
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import numpy as np
import datetime 
import time
import openpyxl
from openpyxl import load_workbook
from itertools import islice
import webbrowser
from pathlib import Path
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import re
from datetime import date
import PyPDF2
import pytesseract


# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
=======
import datetime 
=======
>>>>>>> 3cb83a1a9978df701a57bd2d1a534f395d23eec5
import urllib
import ssl
from lxml import html
import requests
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import numpy as np
import datetime 
import time
import openpyxl
from openpyxl import load_workbook
from itertools import islice
import webbrowser
from pathlib import Path
import shutil
from PIL import Image
import matplotlib.pyplot as plt
import cv2
import re
from datetime import date
import PyPDF2
import pytesseract


# ==============================================================================
# -- codes -------------------------------------------------------------------
<<<<<<< HEAD
# ==============================================================================

>>>>>>> 6337489a8b1fe08500c24132eb5a24f03cfe0f99
=======
# ============================================================================== ## save downloaded data to daily or overal data 
>>>>>>> 3cb83a1a9978df701a57bd2d1a534f395d23eec5
# class for dataGrab
class dataGrabnc(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
<<<<<<< HEAD
<<<<<<< HEAD


=======
        self.name_file = ''
        self.now_date = ''
>>>>>>> 6337489a8b1fe08500c24132eb5a24f03cfe0f99
=======


>>>>>>> 3cb83a1a9978df701a57bd2d1a534f395d23eec5
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
<<<<<<< HEAD
<<<<<<< HEAD


    ## $^&&
    def open4pdf(self, name_file):
        csv_url = 'https://covid19.ncdhhs.gov/dashboard'
        print('  #$$search website', csv_url)
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(2)
        today = (date.today())
        self.name_file = today.strftime('%Y%m%d')
        #self.now_date = today.strftime('%m/%d/%Y')

        d_name = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.pdf'

        #move the files from download to data_raw
        my_file = Path('/home/lunawang/Downloads/NCDHHS_COVID-19_Dashboard_Summary.pdf')
        file_2 = Path('/home/lunawang/Documents/luna2020/covid19viz/' + d_name)
        #file_2 = path('/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.pdf')
        if my_file.is_file() == True:
            print('--------------pdf in download')
            shutil.move('/home/lunawang/Downloads/NCDHHS_COVID-19_Dashboard_Summary.pdf', '/home/lunawang/Documents/luna2020/covid19viz/' + d_name)
            print('----------------pdf now in data_raw')
        if file_2.is_file() == True:
            print('----------------pdf in data_raw')
        else:
            # save html file
            c_page = requests.get(csv_url)
            c_tree = html.fromstring(c_page.content)
            time.sleep(2)

            # click, full screan
            from pynput.mouse import Button, Controller
            mouse = Controller()
            print(mouse.position)
            mouse.position = (955, 57)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, refresh
            mouse = Controller()
            print(mouse.position)
            mouse.position = (151, 75)
            mouse.click(Button.left, 1)
            time.sleep(3)

            #scrow down
            height = siteOpen.execute_script("return document.documentElement.scrollHeight")
            siteOpen.execute_script("window.scrollTo(0, " + str(height//2) + ");")
            time.sleep(9)

            # click, arrow --- 1067, 464
            mouse = Controller()
            print(mouse.position)
            mouse.position = (1067, 464)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, pdf --- 791, 714
            mouse = Controller()
            print(mouse.position)
            mouse.position = (791, 714)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, view --- 
            mouse = Controller()
            print(mouse.position)
            mouse.position = (761, 614)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, dashboard view --- 781, 654
            mouse = Controller()
            print(mouse.position)
            mouse.position = (781, 654)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, select all --- 774, 780
            mouse = Controller()
            print(mouse.position)
            mouse.position = (774, 780)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, download --- 877, 936
            mouse = Controller()
            print(mouse.position)
            mouse.position = (877, 936)
            mouse.click(Button.left, 1)
            time.sleep(15)

            print('finished the clickings. the PDF is downloaded')

            shutil.move('/home/lunawang/Downloads/NCDHHS_COVID-19_Dashboard_Summary.pdf', '/home/lunawang/Documents/luna2020/covid19viz/' + d_name)

        print('=====================')
        print(os.getcwd())
        print('------------')




        # extract text from pdf

        pdf_document = '/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/nc_covid19_start_20210513.pdf'

        import textract
        text = textract.process(pdf_document)
        print('tttttttttttttttt', text)

        pageTxt = text.decode()


        n_start = pageTxt.find('Alamance')
        n_end = pageTxt.find('\x0cWhich counties have laboratory-confirmed cases and deaths?')
        s_date = pageTxt[n_start: n_end]
        #print(',,,,,,,,,,,,,,,,,,,,', s_date)
        

        data = s_date.split("\n")
        #print('.....................', data)

        # add the list together================================
        data_2 =' '.join(data)
        print('2222222222222222', data_2)

        data_3 = data_2.replace(',', '').split('  ')
        print('33333333333333 :', data_3)

        name = data_3[0] + ' ' + data_3[11][3:] + ' ' + data[20][-2] + ' ' + data[20][-1] 
        cases = data_3[3] + ' ' + data_3[5] + ' ' + data_3[7] + ' ' + data_3[14] + ' ' + data_3[16] + ' ' + data_3[18]
        death = data_3[4] + ' ' + data_3[6] + ' ' + data_3[8] + ' ' + data_3[15][3:] + ' ' + data_3[17] + ' ' + data_3[19]


        name_2 = name.split(' ')
        cases_2 = cases.split(' ')
        death_2 = death.split(' ')



        name_3 = []
        for aaa in name_2[:-2]:
            if aaa == 'nty': continue
            elif aaa == 'New': continue
            elif aaa == 'Hanover': 
                name_3.append('New Hanover')
            else: name_3.append(aaa)
            



        print('name ------------------', name_3)
        print('name ------------------', len(name_3))

        print('cases ------------------', cases_2[:52] +cases_2[55:])
        print('cases ------------------', len(cases_2[:52] +cases_2[55:]))

        print('death ------------------', death_2[:52] + death_2[54:])
        print('death ------------------', len(death_2[:52] + death_2[54:]))


        cases_3 = cases_2[:52] +cases_2[55:]
        death_3 = death_2[:52] + death_2[54:]


        all_list = np.vstack((name_3, cases_3, death_3)).T 
        print('llllllllllll', all_list)  

        case = 0
        death = 0
        for a_da in all_list:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(all_list, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        siteOpen.close()
        return l_cases3




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
        print('  save2File', csv_name)

    ## paser data or
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.cvs'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv') 
            #urllib.urlretrieve(urlData, f_n_total)
            #urllib.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            #self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(urlData, self.name_file, str(today))  

=======
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
        else: return []
        return l_data

    ## download a website 
    def download4Website(self, csv_url, fRaw):
        #csv_url = self.l_state_config[5][1]
        # save csv file
        urllib.urlretrieve(csv_url, fRaw)
        return True
    ## open a website 
    def open4Website(self, fRaw):
        csv_url = 'https://covid19.ncdhhs.gov/dashboard#main-content' s#self.l_state_config[5][1] #'https://maryland.maps.arcgis.com/apps/opsdashboard/index.html#/d83b7887227e45728e6daf51a6c91c9f'
        print('  download4Website', csv_url)
        
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(5)
        #iframe = siteOpen.find_element_by_xpath('//iframe[@style="height: 1200px"]')
        iframe = siteOpen.find_element_by_xpath('//iframe[@style="display: block; width: 700px; height: 1627px; margin: 0px; padding: 0px; border: none;"]')
        siteOpen.switch_to.frame(iframe)
        time.sleep(10)
        caseNumbers = siteOpen.find_elements_by_xpath('//span[@style="font-size:11px"]')
        return l_cases3
=======
>>>>>>> 3cb83a1a9978df701a57bd2d1a534f395d23eec5


    ## $^&&
    def open4pdf(self, name_file):
        csv_url = 'https://covid19.ncdhhs.gov/dashboard'
        print('  #$$search website', csv_url)
        siteOpen = webdriver.Chrome()
        siteOpen.get(csv_url)
        time.sleep(2)
        today = (date.today())
        self.name_file = today.strftime('%Y%m%d')
        #self.now_date = today.strftime('%m/%d/%Y')

        d_name = self.state_dir + 'data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.pdf'

        #move the files from download to data_raw
        my_file = Path('/home/lunawang/Downloads/NCDHHS_COVID-19_Dashboard_Summary.pdf')
        file_2 = Path('/home/lunawang/Documents/luna2020/covid19viz/' + d_name)
        #file_2 = path('/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/' + self.state_name.lower() + '_covid19_start_'+self.name_file+ '.pdf')
        if my_file.is_file() == True:
            print('--------------pdf in download')
            shutil.move('/home/lunawang/Downloads/NCDHHS_COVID-19_Dashboard_Summary.pdf', '/home/lunawang/Documents/luna2020/covid19viz/' + d_name)
            print('----------------pdf now in data_raw')
        if file_2.is_file() == True:
            print('----------------pdf in data_raw')
        else:
            # save html file
            c_page = requests.get(csv_url)
            c_tree = html.fromstring(c_page.content)
            time.sleep(2)

            # click, full screan
            from pynput.mouse import Button, Controller
            mouse = Controller()
            print(mouse.position)
            mouse.position = (955, 57)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, refresh
            mouse = Controller()
            print(mouse.position)
            mouse.position = (151, 75)
            mouse.click(Button.left, 1)
            time.sleep(3)

            #scrow down
            height = siteOpen.execute_script("return document.documentElement.scrollHeight")
            siteOpen.execute_script("window.scrollTo(0, " + str(height//2) + ");")
            time.sleep(9)

            # click, arrow --- 1067, 464
            mouse = Controller()
            print(mouse.position)
            mouse.position = (1067, 464)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, pdf --- 791, 714
            mouse = Controller()
            print(mouse.position)
            mouse.position = (791, 714)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, view --- 
            mouse = Controller()
            print(mouse.position)
            mouse.position = (761, 614)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, dashboard view --- 781, 654
            mouse = Controller()
            print(mouse.position)
            mouse.position = (781, 654)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, select all --- 774, 780
            mouse = Controller()
            print(mouse.position)
            mouse.position = (774, 780)
            mouse.click(Button.left, 1)
            time.sleep(3)

            # click, download --- 877, 936
            mouse = Controller()
            print(mouse.position)
            mouse.position = (877, 936)
            mouse.click(Button.left, 1)
            time.sleep(15)

            print('finished the clickings. the PDF is downloaded')

            shutil.move('/home/lunawang/Downloads/NCDHHS_COVID-19_Dashboard_Summary.pdf', '/home/lunawang/Documents/luna2020/covid19viz/' + d_name)

        print('=====================')
        print(os.getcwd())
        print('------------')




        # extract text from pdf

        pdf_document = '/home/lunawang/Documents/luna2020/covid19viz/nc/data_raw/nc_covid19_start_20210513.pdf'

        import textract
        text = textract.process(pdf_document)
        print('tttttttttttttttt', text)

        pageTxt = text.decode()


        n_start = pageTxt.find('Alamance')
        n_end = pageTxt.find('\x0cWhich counties have laboratory-confirmed cases and deaths?')
        s_date = pageTxt[n_start: n_end]
        #print(',,,,,,,,,,,,,,,,,,,,', s_date)
        

        data = s_date.split("\n")
        #print('.....................', data)

        # add the list together================================
        data_2 =' '.join(data)
        print('2222222222222222', data_2)

        data_3 = data_2.replace(',', '').split('  ')
        print('33333333333333 :', data_3)

        name = data_3[0] + ' ' + data_3[11][3:] + ' ' + data[20][-2] + ' ' + data[20][-1] 
        cases = data_3[3] + ' ' + data_3[5] + ' ' + data_3[7] + ' ' + data_3[14] + ' ' + data_3[16] + ' ' + data_3[18]
        death = data_3[4] + ' ' + data_3[6] + ' ' + data_3[8] + ' ' + data_3[15][3:] + ' ' + data_3[17] + ' ' + data_3[19]


        name_2 = name.split(' ')
        cases_2 = cases.split(' ')
        death_2 = death.split(' ')



        name_3 = []
        for aaa in name_2[:-2]:
            if aaa == 'nty': continue
            elif aaa == 'New': continue
            elif aaa == 'Hanover': 
                name_3.append('New Hanover')
            else: name_3.append(aaa)
            



        print('name ------------------', name_3)
        print('name ------------------', len(name_3))

        print('cases ------------------', cases_2[:52] +cases_2[55:])
        print('cases ------------------', len(cases_2[:52] +cases_2[55:]))

        print('death ------------------', death_2[:52] + death_2[54:])
        print('death ------------------', len(death_2[:52] + death_2[54:]))


        cases_3 = cases_2[:52] +cases_2[55:]
        death_3 = death_2[:52] + death_2[54:]


        all_list = np.vstack((name_3, cases_3, death_3)).T 
        print('llllllllllll', all_list)  

        case = 0
        death = 0
        for a_da in all_list:
            case += int(a_da[1])
            death += int(a_da[2])
        l_cases3 = np.append(all_list, [['Total', case, death]], axis=0)
        print('[[[[[[[[[[[[[[[[[[[[', l_cases3)
        siteOpen.close()
        return l_cases3




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
        print('  save2File', csv_name)

    ## paser data or
    def parseData(self, name_file, date_target, type_download):
            self.name_file = name_file
            # step A: read date
            urlData = self.open4pdf(name_file, )
            # step B: save raw
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
            f_n_total = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.cvs'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            self.save2File(urlData, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv') 
            #urllib.urlretrieve(urlData, f_n_total)
            #urllib.urlretrieve(self.l_state_config[5][1], f_name)
            # step C: read data file and convert to standard file and save
            #self.save2File(lst_raw_data, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
            today = date.today()

            return(urlData, self.name_file, str(today))  

<<<<<<< HEAD
## end of file
>>>>>>> 6337489a8b1fe08500c24132eb5a24f03cfe0f99
=======
>>>>>>> 3cb83a1a9978df701a57bd2d1a534f395d23eec5
