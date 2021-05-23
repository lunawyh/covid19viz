#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabYY.py
#
#	grab data from YY state websites
#
#

# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
from __future__ import print_function
import os
from os.path import isfile, join
import csv
import urllib
import datetime 
from lxml import html
import requests
from selenium import webdriver
import time
from shutil import copyfile
import pandas as pd
import openpyxl
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== 
# save downloaded data to daily or overal data 
# class for dataGrabYY
class dataGrabYY(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):
        # create a node
        print("welcome to dataGrabYY")
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
    ## save to csv with a list
    def save_csv24(self, csv_data, csv_name):
        #
        csv_data_f = open(csv_name, "w")
        # create the csv writer
        csvwriter = csv.writer(csv_data_f)
        # csv 1st row as header
        n_col_max = 0
        for a_row in csv_data:
            if len(a_row) > n_col_max:
                n_col_max = len(a_row)
        csvwriter.writerow(range(1, n_col_max + 1))
        if n_col_max < 1:
            csvwriter.writerow(range(1, 3 + 1))
        # csv writes objects
        for a_row in csv_data:
            csvwriter.writerow(a_row)
        # close the csv writer
        csv_data_f.close()
        print("  save_csv24 to", csv_name)
    ## read csv
    def csv_sheet_read(self, csv_data, csv_f):
        print("  csv_sheet_read", csv_f)
        df = pd.read_csv(csv_f)
        (n_rows, n_columns) = df.shape
        for ii in range(n_rows):
            a_row = []
            for jj in range(n_columns):
                if str(df.iloc[ii, jj]) == "nan":
                    break
                a_row.append(df.iloc[ii, jj])
            csv_data.append(a_row)
    ## save to csv
    def get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'Downloads')
    ## save to csv
    def save2datapublic(self, f_data_raw):
        f_dl_name = self.get_download_path() + '/report.pdf'
        # copy
        copyfile(f_dl_name, f_data_raw)
        print('  save2datapublic', f_data_raw)

    ## open a website 
    def open4Website(self):        
        print("  open4Website")

        siteOpen = webdriver.Chrome()
        #
        l_books = []
        if(isfile('./yy/dat2/bible_book0_catalogue.csv')): 
            self.csv_sheet_read(l_books, './yy/dat2/bible_book0_catalogue.csv')
        # catalogue
        if(len(l_books) < 1):
            siteOpen.get(self.l_state_config[5][1])
            time.sleep(3)
            
            #<a class="btn btn-sm btn-secondary" href="1-1.htm">	创世记</a>
            sections = siteOpen.find_elements_by_xpath('//a[@class="btn btn-sm btn-secondary"]')
            for a_sec in sections:
                l_sec = a_sec.text
                link = a_sec.get_attribute('href')
                
                l_books.append([1, l_sec, link.split('/')[-1].split('-')[0], link, 0])  
            time.sleep(1) 
            # 
            #self.save_csv24(l_books, './yy/dat2/bible_cat.csv')
        # chapter
        
        for a_book in l_books:
            #if( int(a_book[2]) != 61 ): continue
            l_chapters = []
            if(isfile('./yy/dat2/bible_book%s_chapters.csv'%(a_book[2]))):
                self.csv_sheet_read(l_chapters, './yy/dat2/bible_book%s_chapters.csv'%(a_book[2]))
            if(len(l_chapters) < 1):
                siteOpen.get(a_book[3])
                time.sleep(4)
                n_total_chapter = 1
                l_chapters.append([a_book[0], a_book[1], a_book[2], a_book[3], 0, 1, a_book[3], 0])
                # <a class="lk" href="1-2.htm">2</a>       
                sections = siteOpen.find_elements_by_xpath('//a[@class="lk"]')
                for a_sec in sections[1:]:
                    l_sec = a_sec.text
                    if(l_sec == '1'):
                        break
                    link = a_sec.get_attribute('href')
                    
                    l_chapters.append([a_book[0], a_book[1], a_book[2], a_book[3], 0, l_sec, link, 0])  
                    n_total_chapter += 1
                # 
                self.save_csv24(l_chapters, './yy/dat2/bible_book%s_chapters.csv'%(a_book[2]))
                a_book[4] = n_total_chapter            
            a_wb = openpyxl.Workbook()
            n_sheet = 0
            # chapter
            for a_chapter in l_chapters:
                a_sheet = a_wb.create_sheet(index = n_sheet , title = a_book[1] + str(a_chapter[-3]) )
                
                siteOpen.get(a_chapter[-2])
                time.sleep(5) 
                l_sections = []
                #<td style="padding-left: 1.7em; text-indent: -1.7em;">
                sections = siteOpen.find_elements_by_xpath('//td[@style="padding-left: 1.7em; text-indent: -1.7em;"]')
                for a_sec in sections:
                    l_sec = a_sec.text.split()
                    if( len(l_sec) < 2):
                        continue 
                    m_sec = []
                    m_sec.append(l_sec[0])                
                    for n_sec in l_sec[2:]:
                        l_sec[1] += ' ' + n_sec
                    m_sec.append(l_sec[1])
                    l_sections.append( m_sec )
                    #print(dStringList)  
                    a_sheet.append(m_sec)
                time.sleep(1) 
                # 
                #self.save_csv24(l_sections, './yy/dat2/bible_book%s_chapter%s.csv'%(a_book[2], a_chapter[-3]))   
                n_sheet += 1             
                
            a_wb.save('./yy/dat2/bible_book%s_chapter_all.xlsx'%(a_book[2]))
            
        #self.save_csv24(l_books, './yy/dat2/bible_book0_catalogue.csv')

        #
        time.sleep(3)  
        siteOpen.close()
        time.sleep(1)
        siteOpen.quit()  # close the window
        return True

    ## read a html string and filter the data, then put into a list 
    def grabData4Content(self, f_raw_name, page_content):
        print("  filterData4Content")
        # open the raw data file or directly use page_content
        if(isfile(f_raw_name)): 
            with open(f_raw_name, "r") as fp:
                page_content = fp.read()

        l_raw_data = []
        if(page_content is not None):
            c_tree = html.fromstring(page_content)
            l_data_raw = c_tree.xpath('//div//div//div//table//tbody//tr//td//a/text()')
        return l_raw_data

    ## save downloaded data to daily data file
    def saveData4Raw(self, l_raw_data, name_file):
        print("  saveData4Raw")
        l_overall = []
        total_cases, total_death = 0, 0

        l_overall.append(['County', 'Cases', 'Deaths'])

        for a_item in l_raw_data:
            l_overall.append([a_item[0], a_item[1], a_item[2]])  

        l_overall.append(['Total', total_cases, total_death])  
        print ('  Total', total_cases, total_death)

        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall

    ## paser data ZZ
    def parseData(self, name_file, date_target, type_download):
        print("  parseData")
        self.name_file = name_file
        self.now_date = date_target
        # step A: read date and save the raw data into a file
        self.open4Website()
             
        return([], self.name_file, self.now_date)  
## end of file

