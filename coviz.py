#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			coviz.py
#
#	show data of COVID-19 in USA
#
######     in GUI
#             press key s to save
#             press key esc to exit
#

from __future__ import print_function


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import cv2
import numpy as np
import pandas as pd
import datetime 
import csv
import os
from os import listdir
from os.path import isfile, join
import math

from shutil import copyfile
from rainbowviz21 import *
from predictionviz22 import *

import sys
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for mapping
class runCoViz(object):
    ## the start entry of this class
    def __init__(self):

        # create an application
        print("welcome to virusviz")
        a_state = self.selectState() 
        self.initState(a_state) 
        self.run() 
    ## select
    def selectState(self):
        #choose one state in US
        self.states_valid = []
        self.states_pos = 0
        if( isfile('../state.txt')):
            with open('../state.txt', 'r') as f:
                self.states_valid = f.readlines()
        a_state = 'MI'
        if( len(self.states_valid) > 0):
                a_state = self.states_valid[0][0:2]
        print('  state', a_state)
        self.stateMachine = 0 
        self.stateMaSub = 0 
        return a_state
    ## set variables
    def initState(self, a_state):
        #initialize with one state in US
        self.state_name = a_state
        self.state_dir = './'+self.state_name.lower()+'/'
        if(not os.path.isdir(self.state_dir) ): os.mkdir(self.state_dir)

        #configuration parameters
        state_cfg = self.state_dir +'state_config.csv'
        if(not isfile(state_cfg)):
            nxt_type = self.getMaxDownloadType()
            print('  next type_download', nxt_type)
            #copyfile('./doc/state_config.csv', state_cfg)  # src, dst)	
            self.l_state_config = self.open4File('./doc/state_config.csv')
            self.l_state_config[4][1] = '%d'%(nxt_type)
            self.save2CfgFile(self.l_state_config, state_cfg)
            # data grabbing file
            data_grab_file = self.state_dir +'dataGrab' + self.state_name + '.py'
            with open('./doc/dataGrabXyz.py', 'r') as file:
                data = file.read().replace('Xyz', self.state_name)
            with open(data_grab_file, 'w') as file:
                file.write(data)
            self.updateDownloadType(nxt_type)	
        else: self.l_state_config= self.open4File (state_cfg)	
        			
        VIZ_W = int( self.l_state_config[0][1] )
        VIZ_H = int( self.l_state_config[1][1] )   
        
        #initialize showing variables
        size = VIZ_H, VIZ_W, 3
        self.img_map = np.zeros(size, dtype=np.uint8)	        # map image
        self.img_overlay = np.zeros(size, dtype=np.uint8)	# overlay image
        self.map_data_updated = 1	                        # being updated
        self.now_exit = False
        # Only the coordinates are used by code
        #print(' l_state_config', self.l_state_config)
        self.l_mi_county_coord= self.open4File (self.state_dir +self.l_state_config[3][1])				
        #data of coordination

        # import image of map
        if( isfile(self.state_dir+self.l_state_config[2][1]) ):
            self.img_map = cv2.resize(cv2.imread(self.state_dir+self.l_state_config[2][1]), (VIZ_W, VIZ_H))
        self.img_overlay = self.img_map.copy()
        self.data_daily = False   # otherwise overall
        # read latest data
        self.name_file = ''
        self.now_date = ''
        self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(999999)
        self.data_grab = None
    ## run
    def run(self):
        # main loop for processing
        t_wait = 1000
        while (not self.now_exit):
            self.cmdProcess( cv2.waitKeyEx(t_wait), 0 )
            if(self.map_data_updated > 0):
                if(len(self.l_mi_cases) > 0):
                    self.img_overlay = self.img_map.copy()
                    self.infoShowCases(self.img_overlay, self.l_mi_cases)
                cv2.imshow("COVIZ of COVID-19 in "+self.state_name, self.img_overlay)
                self.map_data_updated = 0
            t_wait = self.stateManage(0)
        self.exit_hook()
    ## key process
    def cmdProcess(self, key, t0):
        #print("cmdProcess")
        if(key == -1):  
            pass
        else:  
            self.map_data_updated += 1
            pass

        if(key == -1):  
            pass
        elif(key == 65471 or key == 1114047 or key == 7405568):   # F2 key refresh newest from website
            self.data_daily, self.l_mi_cases = self.readDataDaily(True)
            pass
        elif(key == 65472 or key == 1114048 or key == 7405569 or key == 7471104):   # F3 key gmaps
            from mapviz20 import *
            map_viz = mapViz(self.l_state_config, self.state_name)	
            save_file = None
            if self.data_daily == True: type_data=1
            else: 
                type_data =2
                if(self.isNameOnToday(self.name_file)): 
                    save_file = self.state_dir + 'results/mi_county20200000.png'
                    if(not os.path.isdir(self.state_dir + 'results/') ): os.mkdir(self.state_dir + 'results/')
            map_viz.showCountyInMap(self.l_mi_cases, 
                l_type=type_data, l_last = self.l_cases_yest, 
                save_file=save_file, date=self.now_date, timeout=t0)
            pass  
        elif(key == 65473 or key == 1114049 or key == 7602175):   # F4 key parse history data
            pass  
        elif(key == 65474 or key == 1114050 or key == 7602176):   # F5 key refresh newest from website
            self.data_daily = False

            pos, self.l_mi_cases, self.l_cases_yest = self.cmdGrabDataFromWebsite()
            if(len(self.l_mi_cases) > 0):
                self.img_overlay = self.img_map.copy()
                self.infoShowCases(self.img_overlay, self.l_mi_cases)
            pass  
        elif(key == 65476 or key == 1114052 or key == 7798783 or key == 7733248):   # F7 key run all commands
            self.stateMachine = 100 
        elif(key == 65478 or key == 1114054 or key == 7864320):   # F9 key previous day
            self.data_daily = False
            self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(self.csv_pos_now-1)   
        elif(key == 65479 or key == 1114055 or key == 7929856):   # F10 key next day
            self.data_daily = False
            self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(self.csv_pos_now+1) 
        elif(key == 65481 or key == 1114057 or key == 7995393 or key == 8060928 or key == 63247):   # F12 key next day
            save_file = None
            if(self.isNameOnToday(self.name_file)):
                save_file = self.state_dir + 'results/mi_county20200000_predict.png'
            prediction_viz = predictionViz(self.state_name)	

            if( prediction_viz.predictByModelSir(save_file, timeout=t0) ):
                l_img = cv2.imread(self.state_dir + 'results/mi_county20200000_predict.png')
                s_img = cv2.imread('./doc/app_qrcode_logo.jpg')
                x_offset, y_offset=80, 45
                l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img
                cv2.imwrite(self.state_dir + 'results/mi_county20200000_predict.png', l_img)
        elif(key == 114 or key == 1048690):  # r key
            if self.data_daily == True: type_data=1
            else: type_data =2
            save_file = None
            if(type_data==1):
                if(self.isNameOnToday(self.name_file)):
                    save_file = self.state_dir + 'results/mi_county20200000_daily.png'
                    if(not os.path.isdir(self.state_dir + 'results/') ): os.mkdir(self.state_dir + 'results/')
            rainbow_viz = rainbowViz(self.state_name)	
            rainbow_viz.infoShowRainbow(type_data, self.l_mi_cases,
                save_file=save_file, date=self.now_date, timeout=t0)
        elif(key == 100 or key == 1048676):  # d key
            if(self.data_daily): return
            list_death= self.getDataListDeath(self.l_mi_cases)
            save_file = None
            if(self.isNameOnToday(self.name_file)):
                save_file = self.state_dir + 'results/mi_county20200000_death.png'
                if(not os.path.isdir(self.state_dir + 'results/') ): os.mkdir(self.state_dir + 'results/')
            rainbow_viz = rainbowViz(self.state_name)	
            rainbow_viz.infoShowRainbow(3, list_death,
                save_file=save_file, date=self.now_date, timeout=t0)
        elif(key == 115 or key == 1048691):  # s key
            #cv2.imwrite(self.state_dir + 'results/mi_county'+self.name_file+'.png', self.img_overlay)
            pass
        elif(key == 119 or key == 1048695):  # w key, for test only
            #cov_tables = pd.read_html('https://www.ipl.org/div/stateknow/popchart.html')
            #print(cov_tables[0])  
            #self.parseDfData(cov_tables[2], './ne_maps/us_states_land.csv')  
            pass
        elif(key == 27 or key == 1048603):  # esc
            self.stateMachine = 0 
            self.now_exit = True
            pass  
        else:   
            print (key)
    ## manage state machine
    def stateManage(self, state):
        #print('stateMaSub...', state)
        if(self.stateMaSub == 100010):
            if(self.data_grab is not None):
                ret, f_data = self.data_grab.parseData()
                if(ret): 
                    print('  new data in LA')                    
                    self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(999999) 
                    self.stateMaSub = 0
                    self.map_data_updated += 1
        #print('stateManage...', state)
        if(self.stateMachine == 100):
                self.stateMachine += 50
                self.cmdProcess(65474, 5000)  # press F5 grab data
                self.stateMachine += 50
        elif(self.stateMachine == 200):
                if(self.stateMaSub > 0): return 1000
                self.stateMachine += 50
                self.cmdProcess(100, 5000)  # press d show rainbow of death
                self.stateMachine += 50
        elif(self.stateMachine == 300):
                self.stateMachine += 50
                self.cmdProcess(65472, 5000)  # press F3 show base map
                self.stateMachine += 50
        elif(self.stateMachine == 400):
                self.stateMachine += 50
                self.cmdProcess(65481, 5000)  # press F12 show prediction
                self.stateMachine += 50
        elif(self.stateMachine == 500):
                self.stateMachine += 50
                self.cmdProcess(65471, 0)  # press F2 daily data
                self.stateMachine += 50
        elif(self.stateMachine == 600):
                self.stateMachine += 50
                self.cmdProcess(114, 5000)  # press r show rainbow of daily
                self.stateMachine += 50
        elif(self.stateMachine == 700):
                self.stateMachine += 50
                self.csv_pos_now = 999999
                self.cmdProcess(65479, 0)  # press F10 show overall
                self.stateMachine += 50
        elif(self.stateMachine == 800):
                self.stateMachine += 50
                if( self.states_pos < len(self.states_valid)-1 ):
                    self.states_pos += 1
                    if( self.states_valid[self.states_pos][0] == '#' ): 
                        self.stateMachine = 0
                        return 1000
                    cv2.destroyAllWindows()
                    self.initState( self.states_valid[self.states_pos][0:2] ) 
                    self.stateMachine += 50
                    return 10
                else:
                    self.stateMachine = 0
        elif(self.stateMachine == 900):
                self.stateMachine = 100
        return 1000
    ## step 2
    ## read data file given day offset
    def readDataByDay(self, pos):
        print('readDataByDay...', pos)
        data_dir = self.state_dir + 'data'
        if(not os.path.isdir(data_dir) ): os.mkdir(data_dir)
        csv_data_files = sorted( [f for f in listdir(data_dir) if isfile(join(data_dir, f))] )
        #print('-----------', csv_data_files)
        if(0 == len(csv_data_files) ): return (0, [], [])
        if(pos >= len(csv_data_files) ): pos = len(csv_data_files) - 1
        elif(pos < 0): pos = 0
        #print('  ', csv_data_files[pos])
        #if( len(csv_data_files[pos]) != 23): return (pos, [])
        offset = 11	
        dt_obj = datetime.datetime.strptime(csv_data_files[pos][offset:offset+8], '%Y%m%d')
        self.name_file = dt_obj.strftime('%Y%m%d')
        #print('  ', self.name_file)
        self.now_date = dt_obj.strftime('%m/%d/%Y')
        #read data to list
        name_today = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
        lst_data = self.open4File(name_today)
        print('  today', name_today)
        
        #read data on yesterday 
        name_last = self.getOverallYesterday(self.name_file)
        if(name_last is not None):
            lst_data_last = self.open4File(self.state_dir + 'data/' + name_last)
            print('  last ', self.state_dir + 'data/' + name_last)
        else:
            lst_data_last = []
        return (pos, lst_data, lst_data_last)
    ## save downloaded data to daily or overal data 
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
    def save2CfgFile(self, l_data, csv_name):
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        # make sure the 1st row is colum names
        csvwriter.writerow(['name', 'value', 'lon', 'quantity', 'offset'])
        for a_row in l_data:
            csvwriter.writerow(a_row)
        csv_data_f.close()
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
    ## open a csv 
    def open4File(self, csv_name):
        if(isfile(csv_name) ):
            df = pd.read_csv(csv_name)
            l_data = self.parseDfData(df)
        else: return []
        return l_data
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
    def isNameOnToday(self, f_name):
        data_dir = self.state_dir + 'data'
        csv_data_files = sorted( [f for f in listdir(data_dir) if isfile(join(data_dir, f))] )
        if( len(csv_data_files) < 1): return False
        if f_name in csv_data_files[-1]:
            return True		# if is the latest data
        else:
            return False
        '''
        if(self.state_name in 'NY'): return True
        if(self.state_name in 'OH'): return True
        if(self.state_name in 'MS'): return True
        dt_now = datetime.datetime.now()
        dt_name_file = dt_now.strftime('%Y%m%d') 
        if f_name == dt_name_file:
            return True
        else:
            return False
        '''
    ## step 1
    ## grab data from goverment website
    def cmdGrabDataFromWebsite(self):
        print('cmdGrabDataFromWebsite...')
        lst_data = []
        # update date time
        dt_now = datetime.datetime.now()
        self.name_file = dt_now.strftime('%Y%m%d') 
        #print(' grab today', self.name_file)
        self.now_date  = dt_now.strftime('%m/%d/%Y')   
        type_download = int(self.l_state_config[4][1])
        if( type_download == 5 or type_download == 15):   # download only
            sys.path.insert(0, "./oh")
            from dataGrabOh15 import *
            # create new class
            data_grab = dataGrabOh(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
        elif( type_download == 18):   # download only
            sys.path.insert(0, "./il")
            from dataGrabIl18 import *
            # create new class
            data_grab = dataGrabIl(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
        elif( type_download == 25):   # download only
            sys.path.insert(0, "./tx")
            from dataGrabTx25 import *
            # create new class
            data_grab = dataGrabTx(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
        elif( type_download == 35):   # download only
            sys.path.insert(0, "./fl")
            from dataGrabFl35 import *
            # create new class
            data_grab = dataGrabFl(self.l_state_config, self.state_name)	
            # download as a raw file 
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            # save
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 333):   # download only
            sys.path.insert(0, "./or")
            from dataGrabOr333 import *
            # create new class
            data_grab = dataGrabFl(self.l_state_config, self.state_name)	
            # download as a raw file 
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            # save
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 159):   # download only
            sys.path.insert(0, "./pa")
            from dataGrabPA159 import *
            # create new class
            data_grab = dataGrabPA(self.l_state_config, self.state_name)	
            # download as a raw file 
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            # save
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )


        elif( type_download == 109):   # download only
            sys.path.insert(0, "./tn")
            from dataGrabTN109 import *
            # create new class
            data_grab = dataGrabtn(self.l_state_config, self.state_name)	
            # download as a raw file 
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            # save
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 131):   # download only
            sys.path.insert(0, "./wa")
            from dataGrabWA131 import *
            # create new class
            data_grab = dataGrabwa(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 666):   # download only
            sys.path.insert(0, "./nc")
            from dataGrabNC666 import *
            # create new class
            data_grab = dataGrabnc(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 999):   # download only
            sys.path.insert(0, "./md")
            from dataGrabMD999 import *
            # create new class
            data_grab = dataGrabmd(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 105):   # download only
            sys.path.insert(0, "./ks")
            from dataGrabKS105 import *
            # create new class
            data_grab = dataGrabks(self.l_state_config, self.state_name)	
            # download as a raw file 
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            # save
            #step C, save data, and update time
            if(len(lst_data) > 5): 
                self.name_file, self.now_date = name_file, now_date
                f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                self.save2File( lst_data, f_name )

        elif( type_download == 101 ):   # download counties in the list
            sys.path.insert(0, "./ca")
            from dataGrab58 import *
            # create new class
            data_grab = dataGrab(self.l_state_config, self.state_name)	
            # download as a raw file
            lst_data, name_file, now_date = data_grab.parseDataCa(self.name_file, self.now_date, type_download)		
            # save
            if(len(lst_data) > 0):
                self.name_file, self.now_date = name_file, now_date
                #f_name = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
                #self.save2File( lst_data, f_name )
        elif( type_download == 23):   # download only
            sys.path.insert(0, "./ms")
            from dataGrabMS23 import *
            # create new class
            data_grab = dataGrabMS(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
        elif( type_download == 44):   # download only
            sys.path.insert(0, "./ut")
            from dataGrabUt44 import *
            # create new class
            data_grab = dataGrabUT(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
            ########
        elif( type_download == 19):   # download only
            sys.path.insert(0, "./wy")
            from dataGrabWY19 import *
            # create new class
            data_grab = dataGrabWY(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)		
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
            ########
 
        elif( type_download == 2):   # download only
            sys.path.insert(0, "./mi")
            from dataGrabMI2 import *
            # create new class
            data_grab = dataGrabMI(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date

        elif( type_download == 10):   # download only
            sys.path.insert(0, "./la")
            from dataGrabLA10 import *
            # create new class
            data_grab = dataGrabLa(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date

        elif( type_download == 102):   # download only
            sys.path.insert(0, "./ar")
            from dataGrabAR102 import *
            # create new class
            data_grab = dataGrabAR(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date

        elif( type_download == 10):   # download only
            sys.path.insert(0, "./la")
            from dataGrabLA10 import *
            # create new class
            self.data_grab = dataGrabLa(self.l_state_config, self.state_name)	
            self.data_grab.browseData(self.name_file)	
            # download as a raw file and save
            self.stateMaSub = 100010
            return (0, [], [])
        elif( type_download == 33):   # download only
            sys.path.insert(0, "./ga")
            from dataGrabGA33 import *
            # create new class
            self.data_grab = dataGrabGa(self.l_state_config, self.state_name)	
            lst_data, self.name_file, self.now_date = self.data_grab.parseData(self.name_file, self.now_date, type_download)		
            
        elif (type_download == 50):  # download only
            sys.path.insert(0, "./ct")
            from dataGrabCt15 import *
            # step A: create new class
            data_grab = dataGrabCt(self.l_state_config, self.state_name)
            # step B: parse to standard file
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)
        elif (type_download == 14):  # download only
            sys.path.insert(0, "./vt")
            from dataGrabVt import *
            # step A: create new class
            data_grab = dataGrabVt(self.l_state_config, self.state_name)
            # step B: parse to standard file
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)
        elif (type_download == 22):  # download only
            sys.path.insert(0, "./ma")
            from dataGrabMa import *
            # step A: create new class
            data_grab = dataGrabMa(self.l_state_config, self.state_name)
            # step B: parse to standard file
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)
        elif (type_download == 325):  # download only
            sys.path.insert(0, "./me")
            from dataGrabMe import *
            # step A: create new class
            data_grab = dataGrabMe(self.l_state_config, self.state_name)
            # step B: parse to standard file
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)
        elif (type_download == 97):  # download only
            sys.path.insert(0, "./nj")
            from dataGrabNj import *
            # step A: create new class
            data_grab = dataGrabNj(self.l_state_config, self.state_name)
            # step B: parse to standard file
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)
        elif( type_download == 194):   # download only
            sys.path.insert(0, "./nh")
            from dataGrabNh import *
            # create new class
            data_grab = dataGrabNh(self.l_state_config, self.state_name)	
            # download as a raw file and save
            lst_data, name_file, now_date = data_grab.parseData(self.name_file, self.now_date, type_download)	
            #len(the number of characters is a string/object)
            if(len(lst_data) > 0): 
                self.name_file, self.now_date = name_file, now_date
        elif (type_download == 8273): 
            sys.path.insert(0, "./ri") 
            from dataGrabRI import * 
            # step A: create new class 
            data_grab = dataGrabRI(self.l_state_config, self.state_name) 
            # step B: parse to standard file 
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download) 
        ### This is a template entry into one state, to COPY and MODIFY, do NOT REMOVE or CHANGE
        '''  
        elif (type_download == 1):  # download only
            sys.path.insert(0, "./Xyz")
            from dataGrabXyz import *
            # step A: create new class
            data_grab = dataGrabXyz(self.l_state_config, self.state_name)
            # step B: parse to standard file
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download)
        '''
        #read data on yesterday 
        name_last = self.getOverallYesterday(self.name_file)
        if(name_last is not None):
            lst_data_last = self.open4File(self.state_dir + 'data/' + name_last)
        else:
            lst_data_last = []
        print('  done')
        return (0, lst_data, lst_data_last)
    def getOverallYesterday(self, today):
        data_dir = self.state_dir + 'data'
        csv_data_files = sorted( [f for f in listdir(data_dir) if isfile(join(data_dir, f))] )
        if( len(csv_data_files) < 2): return None
        f_last, bFound = csv_data_files[0], False
        for ff in csv_data_files:
            if(today in ff): 
                bFound = True
                break
            f_last = ff
        if(not bFound): f_last=None
        return f_last
    def generateDataDaily(self, bDaily):
        print(' generateDataDaily...')
        # files name
        #csv_daily = self.state_dir + 'daily/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
        csv_all_today = self.state_dir + 'data/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
        csv_all_last = self.getOverallYesterday(self.name_file)
        if(csv_all_last is None): return False, []
        else: print('  compare', csv_all_today, csv_all_last)
        csv_all_last = self.state_dir + 'data/' + csv_all_last
        # read data
        l_all_today = self.open4File(csv_all_today)
        l_all_last = self.open4File(csv_all_last)
        # compare data
        l_daily = []
        l_daily.append(['County', 'Cases', 'Deaths'])
        Total_now = [0, 0]
        Total_wish = [0, 0]
        Total_plus = [0, 0]
        for a_case_today in l_all_today:
            if("Total" in a_case_today[0]): a_case_today[0] = 'Total'  # use the same name
            bFound, a_case_last = self.lookupMapData(a_case_today[0], l_all_last)
            if(bFound):
                num2 = int(a_case_today[1]) - int(a_case_last[1])
                num3 = int(a_case_today[2]) - int(a_case_last[2])
                if("Total" in a_case_today[0]): 
                    Total_wish = [num2, num3] 
                    continue
                if(num2 > 0 or num3 > 0): 
                    l_daily.append([a_case_today[0], num2, num3])
                    #print(a_case_today, num2, num3)
                    Total_plus[0] += num2
                    Total_plus[1] += num3
                Total_now[0] += num2
                Total_now[1] += num3
                
            else:
                Total_now[0] += int(a_case_today[1])
                Total_now[1] += int(a_case_today[2])
                Total_plus[0] += int(a_case_today[1])
                Total_plus[1] += int(a_case_today[2])
                l_daily.append(a_case_today)
                #print(a_case_today)
        if(Total_now[0] != Total_wish[0] or Total_now[1] != Total_wish[1]):
            print(" generateDataDaily total number is wrong", Total_now, Total_wish)
            #return False
        l_daily.append(["Total", Total_plus[0], Total_plus[1]])
        # save data
        #if(not os.path.isdir(self.state_dir + 'daily/') ): os.mkdir(self.state_dir + 'daily/')
        #self.save2File(l_daily, csv_daily)
        return True, l_daily
    def readDataDaily(self, bDaily):
        csv_name = self.state_dir + 'daily/'+self.state_name.lower()+'_covid19_'+self.name_file+'.csv'
        print('readDataDaily', csv_name)
        if(isfile(csv_name) ):
            lst_data = self.open4File(csv_name)
        else:
            bFound, l_data = self.generateDataDaily(True)
            if( bFound ): 
                lst_data = l_data
            else: return (False, [])
        
        return (True, lst_data)
    ## look up table to get pre-set information
    def lookupMapData(self, c_name, lst_data):
        c_name_clean = str(c_name).replace('*', '').replace('.', '')
        for cov in lst_data:
            if c_name_clean in str(cov[0]).replace('*', '').replace('.', ''):
                return True, cov
        #print ('Not found', c_name)
        return False, [' ', 0, 10, 30, (0,0,255)]
    ## look up table to get pre-set information
    def getColorByCompare(self, case_today, lst_data=None):
        if(self.data_daily): return ( (0,255,0) )
        bfound, case_last = self.lookupMapData(case_today[0], self.l_cases_yest)
        if( int(case_today[1]) - int(case_last[1]) > 0): return True
        else: False

    ## look up table to get pre-set information for death
    def getDataListDeath(self, snd_data):
        lst_out = []
        for cov in snd_data:
            if cov[2]>0:
                lst_out.append(cov)
        return lst_out
 
    ## step 3
    ## show cases on the map
    def infoShowCases(self, img, l_cases):
        wish_total = 0
        n_total, ii = 0, 0
        line_h=13	
        offset_h = int( self.l_state_config[1][1] ) - line_h * len(l_cases)/2-25
        for a_case in l_cases:
            if(str(a_case[0]) in 'County'):
                continue
            elif('Total' in str(a_case[0])):
                wish_total = int(a_case[1])
                continue
            else:
                if(ii < len(l_cases)/2): 
                    posx = 10
                    posy = int( ii*line_h+offset_h )
                else: 
                    posx = 180+10
                    posy = int( (ii-len(l_cases)/2)*line_h+offset_h )
                n_total += int( a_case[1] )
                if( self.getColorByCompare(a_case) ): nColor = (0,255,0)
                else: nColor = (0,0,255)
                # draw the list on the left
                cv2.putText(img, str(a_case[0]), 
		        (posx, posy), 
		        cv2.FONT_HERSHEY_SIMPLEX, 
		        0.53,
		        nColor,
		        1) 
                cv2.putText(img, str(a_case[1]), 
		        (130+posx, posy), 
		        cv2.FONT_HERSHEY_SIMPLEX, 
		        0.53,
		        nColor,
		        1) 
                ii += 1
                bFound, map_data = self.lookupMapData(a_case[0], self.l_mi_county_coord)
                if(not bFound): continue
                # draw on the map, select the location
                cv2.putText(img, str(a_case[1]), 
		        (map_data[2],map_data[3]), 
		        cv2.FONT_HERSHEY_DUPLEX, 
		        0.7,
		        nColor,
		        1) 
                
        #print('total:', wish_total, n_total)
        if(wish_total == n_total):
            if(self.data_daily):
                info_cases = '%d Daily Confirmed'%(n_total)
                info_date = 'COVID-19 on ' + self.now_date + ' in '+self.state_name
            else:
                info_cases = '%d Overall Confirmed'%(n_total)
                info_date = 'COVID-19 until ' + self.now_date + ' in '+self.state_name
            cv2.putText(img,info_cases, 
		    (300,30), 
		    cv2.FONT_HERSHEY_DUPLEX, 
		    1,
		    (255,64,0),
		    1) 
            cv2.putText(img, info_date, 
		    (300,65), 
		    cv2.FONT_HERSHEY_DUPLEX, 
		    0.7,
		    (255,64,0),
		    1) 
        else:
            print( '  wished total: %d, listed total: %d'%( wish_total, n_total) )
        cv2.putText(img, 'press F5 to refresh', 
		    (782,205), 
		    cv2.FONT_HERSHEY_SIMPLEX, 
		    0.3,
		    (255,64,0),
		    1) 
    # check and return maximum type_download
    def getMaxDownloadType(self):
        # calculate from self.state_name
        return (ord(self.state_name[0])*100 + ord(self.state_name[1]))
        # otherwise, choose a unique number
        l_types = []
        with open('./coviz.py') as f:
                a_content = f.readlines()  
        for a_line in a_content:  
                n_start = a_line.find('type_download ==')
                if(n_start >= 0): 
                    #print('  getMaxDownloadType', a_line)
                    n_end = a_line.find(')', n_start+16)
                    if(n_end >= 0): 
                        b_line = a_line[n_start+16+1:n_end].replace(' ', '')
                        if(b_line.isdigit()): l_types.append(int(b_line))
        if(len(l_types) > 0):
            max_type = sorted(l_types)[-1] + 1
            return max_type	
        return 1

    # insert and update
    def updateDownloadType(self, n_type):
        # coviz.py this file
        s_target = '        elif (type_download == 8): \n\
            sys.path.insert(0, \"./abc\") \n\
            from dataGrabXyz import * \n\
            # step A: create new class \n\
            data_grab = dataGrabXyz(self.l_state_config, self.state_name) \n\
            # step B: parse to standard file \n\
            lst_data, self.name_file, self.now_date = data_grab.parseData(self.name_file, self.now_date, type_download) \n'
        s_target = s_target.replace('8', '%d'%(n_type)).replace('Xyz', self.state_name).replace('abc', self.state_name.lower())
        with open('./coviz.py') as f:
            a_content = f.readlines()  
        n_line = 0
        b_lines = []
        for a_line in a_content:  
            n_start = a_line.find('### This is a template entry into one state, to COPY and MODIFY, do NOT REMOVE or CHANGE')
            if(n_start >= 0): 
                b_lines = a_content[:n_line]
                b_lines.append(s_target)
                b_lines += a_content[n_line:]
                break
            n_line += 1
        if(len(b_lines) > 500): 
            with open('./coviz.py', 'w') as f:
                f.writelines(b_lines)	

    ## exit node
    def exit_hook(self):
        print("bye bye, node virusviz")

## the entry of this application
if __name__ == '__main__':
        runCoViz()
        cv2.destroyAllWindows()
        pass

## end of file
