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
import ssl
import PyPDF2
import re
import requests
from lxml import html
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabFl(object):
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
        csv_url = self.l_state_config[5][1]
        print('  search website', csv_url)
        # save html file
        #urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('See state report' in l_date.text_content()):
                a_address = l_date.get('href')
                print('  find pdf at', l_date.get('href'))
                break
        return a_address
    ## paser data FL
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): # not isfile(f_name) ): 
                a_address = self.open4Website(None)
                if(a_address == ''): return ([], None, None)
                n_start = a_address.find('report-')
                if(n_start >= 0): 
                    s_date = a_address[n_start + 7: ] 
                    n_end = s_date.find('09')
                    print(' *********************** ', s_date)
                    if(n_end < 0): n_end = s_date.find('-')
                    s_date = s_date[: n_end] 
                    print(' ^^^^^^^^^^^^^^ ', s_date)
                    s_date = re.sub("[^0-9]", "", s_date)
                    print(' &&&&&&&&&&&&&&&&&&&&&&&&& ', s_date)

                    dt_obj = datetime.datetime.strptime(s_date, '%Y%m%d')
                    print('  updated on', dt_obj)
                    #nums = int(n_start)
                    self.name_file = dt_obj.strftime('%Y%m%d')
                    self.now_date = dt_obj.strftime('%m/%d/%Y')
                    f_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                    if(not isfile(f_name) ):
                        result = self.download4Website(a_address, f_name)
                        print('  downloaded', result)
                    else:
                        print('  already exiting')
                else: f_name = ''
            return f_name
    ## paser data FL
    def dataReadConfirmed(self, f_name):
            print('  B.dataReadConfirmed on page 5', f_name)
            # step B: parse and open
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            pageObj = pdfReader.getPage(4)
            pageTxt = pageObj.extractText()
            #print('  pageTxt 5:', pageTxt)
            # get text in the table list
            n_start = pageTxt.find('confirmed cases')
            if(n_start < 0):
                return ([], pdfReader)
            pageTxt = pageTxt[n_start + 17:]
            n_start = pageTxt.find('Total')
            if(n_start < 0):
                return ([], pdfReader)
            pageTxt = pageTxt[n_start + 6:]
            n_start = pageTxt.find('Total')
            if(n_start < 0):
                return ([], pdfReader)
            pageTxt = pageTxt[n_start + 6:]

            tableTxt = ''
            pre_char = '\n'
            for a_char in pageTxt:
                if( a_char.isalpha() ):
                    if( pre_char.isdigit() ): tableTxt += '\n'
                pre_char = a_char
                tableTxt += a_char
            #print('  tableTxt on 5:', tableTxt)
            l_d_sort = self.parseTableConfirmed(tableTxt)
            return (l_d_sort, pdfReader)
    ## paser data FL
    def getNumberConfirmed(self, l_numbers, a_name=''):
        #print('    getNumberConfirmed', l_numbers)
        bFound = False
        if(len(l_numbers) == 1): 
            rowTxt = l_numbers[0]
            n_start = rowTxt.find('%')
            if(n_start < 0): 
                print('  error numbers', rowTxt)
                return 0
            len_row = len(rowTxt)
            for ii in range(1, n_start):
                for jj in range(n_start+1, len_row):
                    n_resident = int( re.sub("[^0-9]", "", rowTxt[:n_start-ii]) )
                    txt_resident = ( re.sub("[^0-9]", "", rowTxt[n_start:jj]) )
                    if(len(txt_resident) <= 0): non_resident = 0
                    else: non_resident = int(txt_resident)
                    n_total = int( re.sub("[^0-9]", "", rowTxt[jj:]) )
                    #print('    guess', n_resident, non_resident, n_total, a_name)
                    if(n_total == n_resident + non_resident): 
                        bFound = True
                        #print('    find', n_resident, non_resident, n_total)
                        return n_total
        elif(len(l_numbers) == 2): 
            n_resident = int( re.sub("[^0-9]", "", l_numbers[0]) )
            rowTxt = l_numbers[1]
            n_start = rowTxt.find('%')
            if(n_start < 0): 
                print('  error numbers', l_numbers[0])
                return 0
            len_row = len(rowTxt)
            for jj in range(n_start+1, len_row):
                    txt_resident = ( re.sub("[^0-9]", "", rowTxt[n_start:jj]) )
                    if(len(txt_resident) <= 0): non_resident = 0
                    else: non_resident = int(txt_resident)
                    n_total = int( re.sub("[^0-9]", "", rowTxt[jj:]) )
                    #print('    guess', n_resident, non_resident, n_total, a_name)
                    if(n_total == n_resident + non_resident): 
                        bFound = True
                        #print('    find', n_resident, non_resident, n_total)
                        return n_total
        elif(len(l_numbers) == 3): 
            n_resident = int( re.sub("[^0-9]", "", l_numbers[0]) )
            non_resident = int( re.sub("[^0-9]", "", l_numbers[1]) )
            n_total = int( re.sub("[^0-9]", "", l_numbers[2]) )
            if(n_total == n_resident + non_resident): 
                        bFound = True
                        #print('    find', n_resident, non_resident, n_total)
                        return n_total

        print('    getNumberConfirmed NOT find number', l_numbers, a_name)
        return 0
    ## paser data FL
    def parseTableConfirmed(self, pageTxt):
            case_total = 0
            case_total_rd = 0
            l_overall = [] 
            #l_overall.append(['County', 'Cases', 'Deaths'])

            l_pageTxt = pageTxt.split('\n')
            state_machine = 1
            a_name = ''
            a_digital = 0
            l_numbers = []
            for a_row in l_pageTxt:
		        #print('  a_row', a_row)
		        if(state_machine == 1):
		            if( a_row.lower().islower() ):
		                # a county
		                a_name = a_row
		                l_numbers = []
		                state_machine = 2
		        elif(state_machine == 2):
		            if( a_row.lower().islower() ):
		                print('  error county name', a_row)
		            else:
		                # a line of numbers
		                l_numbers.append(a_row)
		                state_machine = 3
		        elif(state_machine == 3):
		            if( a_row == '' ):
		                pass
		            elif( a_row.lower().islower() ):
		                # one or two lines of numbers
		                a_digital = self.getNumberConfirmed(l_numbers, a_name)
		                if(a_digital <= 0): print('  a_row', a_name)
		                if('Total' in a_name): 
		                    case_total_rd =  a_digital
		                    print('    Total is read', a_digital)
		                else:
		                    case_total += a_digital
		                    if(a_name in 'Dade'): a_name = 'Miami-Dade'
		                    l_overall.append([a_name, a_digital, 0])
		                # another county
		                a_name = a_row
		                l_numbers = []
		                state_machine = 2
		                # to next county
		            else:
		                # a line of numbers
		                l_numbers.append(a_row)
		                state_machine = 3
            # the last name and number
            a_digital = self.getNumberConfirmed(l_numbers)
            l_overall.append([a_name, a_digital, 0])
            case_total += a_digital
            
            l_d_sort = sorted(l_overall, key=lambda k: k[0])
            if(case_total == case_total_rd): 
                l_d_sort.append(['Total', case_total, 0])
                print('  Total is confirmed', case_total, case_total_rd)
            else: 
                l_d_sort.append(['Total', case_total_rd, 0])
                print('  Total is mismatched', case_total, case_total_rd)
            return (l_d_sort)
    ## paser data FL
    def dataReadDeath(self, l_d_sort, pdfReader):
            print('  C.dataReadDeath')
            # read death in county
            p_s, p_e = 20, 78
            #p_s, p_e = 31, 43 # page number in PDF for 4/19/2020
            #p_s, p_e = 30, 48 # page number in PDF for 4/24/2020
            case_total = 0
            for page in range(p_s-1, p_e+1):
		    pageObj = pdfReader.getPage(page)
		    pageTxt = pageObj.extractText()
		    l_pageTxt = pageTxt.split('\n')
		    if('Coronavirus: line list of deaths in Florida residents' in l_pageTxt[0]): pass
		    else: continue
		    state_machine = 1
		    for a_row in l_pageTxt:
		        #print(a_row)    
		        if(state_machine == 1):
		            if('today' in a_row):
		                state_machine = 2
		        elif(state_machine == 2 ):
		            if( a_row.lower().islower() ): pass
 		            else: continue
		            if( 'Unknown' in a_row ): continue
 		            if('Dade' in a_row): a_row = 'Miami-Dade'
		            for a_d_row in l_d_sort:
				if a_d_row[0] in a_row:
				    a_d_row[2] += 1
				    case_total += 1
				    break
		    print('    PDF page on', page+1, case_total)
		    #break
            l_d_sort[-1][2] = case_total
            return l_d_sort 
    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            f_target = self.dataDownload(name_target)
            if(f_target == ''): return ([], name_target, '')
            l_d_sort, pdfReader = self.dataReadConfirmed(f_target)
            if(len(l_d_sort) > 0): l_d_all = self.dataReadDeath(l_d_sort, pdfReader)
            else: l_d_all = []
            return(l_d_all, self.name_file, self.now_date)  

## end of file
