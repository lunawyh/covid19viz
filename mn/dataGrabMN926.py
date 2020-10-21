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
import numpy as np

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for dataGrab
class dataGrabMN(object):
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
        l_dates = c_tree.xpath('//ul//li//strong//a')  # ('//div[@class="col-xs-12 button--wrap"]')
        print('   dddd', l_dates)
        a_address = ''
        for l_date in l_dates:
            #print(l_date.text_content())
            if('Weekly COVID-19 Report') in l_date.text_content(): 
                print('   sss', l_date)
                a_address = 'https://www.health.state.mn.us' + l_date.get('href')
                print('  find pdf at', a_address)

        l_2dates = c_tree.xpath('//ul//li//strong//a/text()')
        for l_date in l_2dates:
            #print(l_date.text_content())
            if('Weekly COVID-19 Report') in l_date: 
                print('ccccccccccccccc', l_date)
                n_start = l_date.find('Report:')
                if(n_start >= 0): 
                    s_date = l_date[n_start+7:] 
                    n_end = s_date.find('(PDF)')
                if(n_end >= 0):
                        s_date = s_date[1: 11].replace ('00:00:00', '')

                        dt_obj = datetime.datetime.strptime(s_date, '%m/%d/%Y')
                        print('  updated on', dt_obj)
                        #nums = int(n_start)
                        self.name_file = dt_obj.strftime('%Y%m%d')
                        self.now_date = dt_obj.strftime('%m/%d/%Y')
        print('11111111111111', a_address)
           
        return a_address
    ## paser data FL
    def dataDownload(self, name_target):
            print('  A.dataDownload', name_target)
            f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+name_target+'.pdf'
            if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')
            # step A: downlowd and save
            if( True): 
                a_address = self.open4Website(f_namea)

                if(a_address == ''): 
                    print ('    No address of downloading PDF is found')
                    return ('')

                f_namea = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.pdf'
                

                if(not isfile(f_namea) ):
                    result = self.download4Website(a_address, f_namea)
                    print('  downloaded', result, f_namea)
                    print('__________________')
                else:
                    print('  already exiting', f_namea)
                    print('__________________')

            return f_namea
    ## look for page containing confirmed data
    def lookForConfirmedPage(self, pdfReader):
        for page in range(4, 9):
            pageObj = pdfReader.getPage(page)
            pageTxt = pageObj.extractText()
            # locate page
            n_start = pageTxt.find('Florida counties have')
            if(n_start >= 0): print('  found at page ', page) 
            else: continue
            # get time
            n_start = pageTxt.find('Data through')
            if(n_start >= 0):
                n_end = pageTxt.find('verified')
                s_date = pageTxt[n_start+12+1: n_end-1]
                print('    updating date', s_date)
                dt_obj = datetime.datetime.strptime(s_date, '%b %d, %Y')
                print('    updated on', dt_obj)
                #nums = int(n_start)
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                return pageTxt
        return ''
    ## paser data FL
    def dataReadConfirmed(self, f_name):
            print('  B.dataReadConfirmed on page 5-10', f_name)
            # step B: parse and open
            #print('    nnn', f_name)
            pdfFileObj = open(f_name, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            # look for page containing confirmed data
            pageTxt = self.lookForConfirmedPage(pdfReader)
            if(pageTxt == ''): return ([], pdfReader)

            # get text in the table list
            n_start = pageTxt.find('All 67 Florida counties have cases')
            if(n_start < 0):
                n_start = pageTxt.find('All 67 Florida counties have cases')
                if(n_start < 0):
                    return ([], pdfReader)
                #return ([], pdfReader)
            pageTxt = pageTxt[n_start + 17:]

            n_start = pageTxt.find('rate')
            if(n_start < 0):
                return ([], pdfReader)
            pageTxt = pageTxt[n_start + 6:]
            n_start = pageTxt.find('rate')
            if(n_start < 0):
                return ([], pdfReader)
            n_end = pageTxt.find('FL resident cases')
            pageTxt = pageTxt[n_start + 5: n_end-1]
            pageTxt2 = pageTxt.split('\n')
            nam_num_case = []
            for a_ccc in pageTxt2:
                if '%' in a_ccc: pass
                else: nam_num_case.append(a_ccc)
            #print('lllllllllllll', (nam_num_case))  
            #print('................', len(nam_num_case))  


            l_cases2 = np.reshape(nam_num_case, (len(nam_num_case)/5, 5)).T
            l_data = np.vstack((l_cases2[0], l_cases2[3], l_cases2[4])).T 
            #print('--------------', l_data)
            #l_data[-2], l_data[-1] = l_data[-1], l_data[-2]
            l_data2= l_data[:-2]
            l_data2= np.append(l_data2, l_data[-1])
            l_data2= np.append(l_data2, l_data[-2])
            #print(';;;;;;;;;', l_data2)

            l_cases3 = np.reshape(l_data2, (len(l_data2)/3, 3)).T
            l_data = np.vstack((l_cases3[0], l_cases3[1], l_cases3[2])).T 
            l_datas = np.core.defchararray.replace(l_data, ',', '')

            print(';;;;;;;;;;;', l_datas)
            return (l_datas)
    ## paser data FL
    def getNumberConfirmed(self, l_numbers, a_name=''):
        #print('    getNumberConfirmed', l_numbers)
        bFound = False
        if(len(l_numbers) == 1): 
            rowTxt = l_numbers[0]
            n_start = rowTxt.find('%')
            if(n_start < 0): 
                print('    error 1 numbers', rowTxt)
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
                print('    error 2 numbers', l_numbers)
                return int(l_numbers[1])
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
            if('%' in l_numbers[1]): non_resident = 0
            else: non_resident = int( re.sub("[^0-9]", "", l_numbers[1]) )
            n_total = int( re.sub("[^0-9]", "", l_numbers[2]) )
            if(n_total == n_resident + non_resident): 
                        bFound = True
                        #print('    find', n_resident, non_resident, n_total)
                        return n_total
        elif(len(l_numbers) == 4): 
            n_resident = int( re.sub("[^0-9]", "", l_numbers[0]) )
            non_resident = int( re.sub("[^0-9]", "", l_numbers[2]) )
            n_total = int( re.sub("[^0-9]", "", l_numbers[3]) )
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
		                if(a_digital <= 0): print('    at a_row', a_name)
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
            if('Total' in a_name): 
                case_total_rd =  a_digital
                print('    Total is read', a_digital)
            else:
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
    def dataReadDeath4Pages(self, l_d_sort, f_name):
        print('  C.dataReadDeath4Pages from', f_name)
        # read death in county
        pdfFileObj = open(f_name, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        p_s, p_e = 1, 99
        #p_s, p_e = 31, 43 # page number in PDF for 4/19/2020
        #p_s, p_e = 30, 48 # page number in PDF for 4/24/2020
        case_total = 0
        for page in range(p_s-1, p_e+1):
		    pageObj = pdfReader.getPage(page)
		    pageTxt = pageObj.extractText()
		    l_pageTxt = pageTxt.split('\n')
		    if('line list of deaths in Florida residents' in l_pageTxt[0]): pass
		    else: break

		    #print('    pdf page is found', page)
		    state_machine = 100
		    for a_row in l_pageTxt:
		        #print('    dataReadDeath4Pages:', a_row)    
		        if(state_machine == 100):
		            if('today' in a_row):
		                state_machine = 200
		            if('provisional' in a_row):
		                state_machine = 200
		        elif(state_machine == 200 ):
		            if( a_row.lower().islower() ): pass
 		            else: continue
 		            #print('    dataReadDeath4Pages:', a_row) 
 		            #if( 'Unknown' in a_row ): continue
 		            if('Dade' in a_row): a_row = 'Miami-Dade'
 		            for a_d_row in l_d_sort:
 		                if a_d_row[0] in a_row:
 		                    a_d_row[2] += 1
 		                    case_total += 1
 		                    break
		    print('    found PDF page on', page+1, case_total)
		    #break
        l_d_sort[-1][2] = case_total
        return l_d_sort 
    ## paser data FL
    def dataReadDeath(self, l_d_sort, pdfReader):
            print('  C.dataReadDeath')
            # read death in county
            lst_cases = []
            a_name = ''
            a_number = 0
            case_total_append = 0
            case_total_rd = 0

            pageObj = pdfReader.getPage(3)
            pageTxt = pageObj.extractText()
            l_pageTxt = pageTxt.split('\n')
            #print('   l_pageTxt ',l_pageTxt )
            case_total = 0
            if('Coronavirus: line list of deaths in Florida residents' in l_pageTxt[0]): pass
            #else: continue
            state_machine = 1
            for a_row in l_pageTxt:
		        print('dataReadDeath', a_row)    
		        if(state_machine == 1):
		            if('%' in a_row):
		                state_machine = 2
		        
		        elif(state_machine == 2 ):
		            if('%' in a_row):
		                state_machine = 3
		        elif(state_machine == 3 ):
		            if('%' in a_row):
		                state_machine = 4
		        elif(state_machine == 4 ):
		            #print('   VVVVV_________________________________' ,a_row)
		            if 'COVID-19: ' in a_row: break
		            if '%' in a_row:
		            	print('    _________% :', a_row)
		            	
		            elif a_row.isalpha() == True :
		            	#print('  ++++++letters :', a_row)
		            	a_name = a_row
		            	lst_cases.append([a_name, a_number, 0])
		            else:
		            	#print('----numbers :', a_row)
		            	if ',' in a_row:
		            		a_row = a_row.split(',')
		            		print (' *************', a_row)
		            		#a_row[0] = a_row[0][0:1 ]
		            		print (' =======' ,a_row[0] + a_row[1])
		            		a_row = a_row[0] + a_row[1]
		            		a_number = int(a_row)
		            		case_total_rd = a_number
		            		lst_cases.append([a_name, a_number, 0])
		            		break
		            	a_number = int(a_row)
		            	case_total_append += a_number
		            	lst_cases.append([a_name, a_number, 0])
            print('    dataReadDeath', lst_cases)
            return l_d_sort 
    ## paser data FL
    def parseData(self, name_target, date_target, type_download):
            self.name_file = name_target
            self.now_date = date_target
            #Step A download and save as raw PDF files
            f_targeta, f_targetb = self.dataDownload(name_target)
            if(f_targeta == ''): return ([], name_target, '')
            #Step B read confirmed cases
            l_d_sort = self.dataReadConfirmed(f_targeta)
            #Step C read death cases
        

            return(l_d_sort, self.name_file, self.now_date)  

## end of file
