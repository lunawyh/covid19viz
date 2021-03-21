#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			dataGrabZZ.py
#
#	grab data from ZZ state websites
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

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ============================================================================== 
# save downloaded data to daily or overal data 
# class for dataGrabZZ
class dataGrabZZ(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):
        # create a node
        print("welcome to dataGrabZZ")
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

    ## open a website 
    def open4Website(self, name_file, date_target):
        data_url = self.l_state_config[5][1]
        print("  open4Website", data_url)
        if('http' not in data_url): return '', None

        siteOpen = webdriver.Chrome()
        
        # check sign in
        ref_signin = 'https://bsaonline.com/Account/LogOn?uid=406'
        '''
        # <div class="site-vert-navigation-item" class="Sign into your BS&amp;A Online account"><a href="/Account/LogOn">Sign In</a></div>
        ref_navigations = siteOpen.find_elements_by_xpath('//a')
        for a_ref_navi in ref_navigations:  # this is names------------------------------------
            if('Sign In' in a_ref_navi.text):
                ref_signin = a_ref_navi.get_attribute('href')                
                #print('  ref_signin', ref_signin)
                break
        '''
        # sign in at first
        if(ref_signin != ''):
            siteOpen.get(ref_signin)
            time.sleep(3)
            # <input class="text-box-single-line valid" data-val="true" data-val-required="The User Name field is required." id="UserName" name="UserName" style="width: 200px" tabindex="0" type="text" value="">
            # <input class="text-box-single-line valid" data-val="true" data-val-required="The Password field is required." id="Password" name="Password" style="width: 200px" type="password" value="">
            inputs = siteOpen.find_elements_by_xpath('//input')
            for a_input in inputs:
                if(a_input.get_attribute('id') == 'UserName'):
                    siteOpen.execute_script("arguments[0].setAttribute('value','wzijian')", a_input)
                    #a_input.setAttribute('value', 'wzijian')  
                if(a_input.get_attribute('id') == 'Password'):
                    siteOpen.execute_script("arguments[0].setAttribute('value','zzy403!')", a_input)
                    #a_input.setAttribute('value', 'zzy403')     
            time.sleep(1) 
            # <input class="t-button t-state-default bsa-button" id="" name="signIn" value="Sign In" type="submit">   
            for a_input in inputs:
                if(a_input.get_attribute('name') == 'signIn'):
                    a_input.click()
                    break
        # get tab
        time.sleep(3)
        siteOpen.get(data_url)
        time.sleep(5)

        c_content = None
        f_raw_name = self.state_dir + 'data_raw/'+self.state_name.lower()+'_covid19_'+self.name_file+'.html'
        if(not os.path.isdir(self.state_dir + 'data_raw/') ): os.mkdir(self.state_dir + 'data_raw/')

        #
        time.sleep(7)  
        siteOpen.close()

        siteOpen.quit()  # close the window
        return f_raw_name, c_content

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
        f_raw_name, contents = self.open4Website(name_file, date_target)
        # step B: filter data and convert to a raw list
        l_raw_data = self.grabData4Content(f_raw_name, contents)
        # step C:  convert to a standard list and save
        lst_data = self.saveData4Raw(l_raw_data, self.name_file)       
        return(lst_data, self.name_file, self.now_date)  
## end of file

