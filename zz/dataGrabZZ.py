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
from shutil import copyfile
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
    def downloadWaterBill(self, index, pdf_target, siteOpen):
        data_url = self.l_state_config[5][index]
        print('    downloadWaterBill', data_url)
        f_dl_name = self.get_download_path() + '/report.pdf'
        # delete if existing
        if os.path.isfile(f_dl_name):
            os.remove(f_dl_name)
        # get tab        
        siteOpen.get(data_url)
        time.sleep(19)
        # Utility Bill Info.
        # <input class="t-button t-state-default bsa-button" id="138f66fb-5887-46b9-a3ec-af2ae18e3a0c" 
        # onclick="javascript:DisplayUBReportImagePopup(3973, 'CAMR-005246-0000-01', '1700435', 'true', '3/15/2021 12:00:00 AM', '6151271');" onkeydown="function(e){ if(e.keyCode == 90){ javascript:DisplayUBReportImagePopup(3973, 'CAMR-005246-0000-01', '1700435', 'true', '3/15/2021 12:00:00 AM', '6151271'); } }" name="PrintUBBillButton" 
        # value="Click here for your current Utility Bill" type="button">
        ref_tabs = siteOpen.find_elements_by_xpath('//a')
        for a_ref_tab in ref_tabs:  
            if('Utility Bill Info.' in a_ref_tab.text):
                #ref_utility = a_ref_tab.get_attribute('href')                
                #print('  ref_utility', ref_utility)
                a_ref_tab.click()
                time.sleep(18)
                inputs = siteOpen.find_elements_by_xpath("//input[@value='Click here for your current Utility Bill']")
                for a_input in inputs:  
                    print('    a_input:', a_input.get_attribute('value'))                     
                    a_input.click()
                    time.sleep(17)
                    # <div onclick="RedirectToNewPage('/Reporting/ViewSavedReport?application=10&amp;reportGuid=9b3a5a53-36b8-45ab-b995-6749bc568cfb&amp;saveToDisk=true'); return false;" onkeydown="function(e){ if(e.keyCode == 90){ RedirectToNewPage('/Reporting/ViewSavedReport?application=10&amp;reportGuid=9b3a5a53-36b8-45ab-b995-6749bc568cfb&amp;saveToDisk=true'); return false; } }" 
                    # id="pdfButton" class="action-container"><div class="action-text">Save As PDF</div>
                    downloads = siteOpen.find_elements_by_xpath("//div[@id='pdfButton']")
                    for a_download in downloads:
                        print('    a_download:', a_download.get_attribute('id'))                     
                        a_download.click()
                        time.sleep(5)
                        #    
                        self.save2datapublic('../cloudH/house/uploaded_files/h'+pdf_target+'_waterbill.pdf')                             
                        break
                    break
                break
    ## open a website 
    def open4Website(self):        
        print("  open4Website")

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
                    time.sleep(3)
                    break
        #
        self.downloadWaterBill(1, '5246', siteOpen)
        self.downloadWaterBill(2, '846', siteOpen)
        self.downloadWaterBill(3, '820', siteOpen)
        self.downloadWaterBill(4, '1720', siteOpen)
        #
        # check 3256
        # https://bsaonline.com/OnlinePayment/OnlinePaymentSearch?PaymentApplicationType=10&uid=305&showEmbeddedView=true
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

