   
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
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== ## save downloaded data to daily or overal data 
# class for dataGrab
class dataGrabMI(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to dataGrab")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config

    def saveLatestDateMi(self, l_raw_data):
        l_overall = []
        
        l_overall.append(['County', 'Cases', 'Deaths'])
        for a_item in l_raw_data:
            
            l_overall.append(a_item[:3])
        #for a_item in l_overall:
        #    print (a_item)
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv')
        return l_overall

    ## save to csv 
    def save2File(self, l_data, csv_name):
        '''
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        '''
        l_overall = []
        offset = 0   # after 5/5 changed from 1 to 0
        # make sure the 1st row is colum names
        if('County' in str(l_data[0][0])): pass
        else: csvwriter.writerow(['County', 'Cases', 'Deaths'])
        for a_item in l_data:
            if 'County' in str(a_item[offset]):continue
            #if str(a_item [1]) in '0':
            #    a_item[1]='Total'
                
            l_overall.append(a_item[offset:])  
        #for a_item in l_overall:
        #    print (a_item)
        self.save2File(l_overall, self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+name_file+'.csv')
        return l_overall
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data
    ## open a website 
    def open4Website(self, fRaw):
        #csv_url = "https://www.michigan.gov/coronavirus/0,9753,7-406-98163-520743--,00.html"
        #csv_url = 'https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html'
        csv_url = self.l_state_config[5][1]
        # save html file
        urllib.urlretrieve(csv_url, fRaw)
        # save html file
        c_page = requests.get(csv_url)
        c_tree = html.fromstring(c_page.content)
        l_dates = c_tree.xpath('//strong/text()')
        for l_date in l_dates:
            if('Confirmed COVID-19 Cases by Jurisdiction updated' in l_date):
                a_date = l_date.replace('Confirmed COVID-19 Cases by Jurisdiction updated ', '')
                dt_obj = datetime.datetime.strptime(a_date, '%m/%d/%Y')
                self.name_file = dt_obj.strftime('%Y%m%d')
                self.now_date = dt_obj.strftime('%m/%d/%Y')
                break
        # read tables
        s_date = ''
        if(isfile(fRaw) ):
            xl_file = pd.ExcelFile(fRaw)
            #print(xl_file.sheet_names)
            nfx = ''
            for sheet in xl_file.sheet_names:
                if 'Sheet 1' in (sheet):
                    nfx = sheet
                    break

            if nfx == '':return [], s_date
            df = xl_file.parse( nfx )
            print('^^^^^^^^^^^^', df)
            n_date = df.columns[0].find('COUNTY')
            if(n_date >= 0):
                s_date = df.columns[ :0] + columns[1: ]
                print(' @@@@@@@@@@@@@@@@@@@2s_date', s_date)
            l_data = self.parseDfData(df)
        else: return [], s_date
        return l_data, s_date
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


