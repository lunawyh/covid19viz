#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			virusviz.py
#
#	show data of COVID-19 in Michigan
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
from os import listdir
from os.path import isfile, join
import matplotlib
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt

VIZ_W  = 880
VIZ_H  = 1000
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for mapping
class runVirusViz(object):
    ## the start entry of this class
    def __init__(self):

        # create a node
        print("welcome to node virusviz")
        #initialize variables
        size = VIZ_H, VIZ_W, 3
        self.img_map = np.zeros(size, dtype=np.uint8)	        # map image
        self.img_overlay = np.zeros(size, dtype=np.uint8)	# overlay image
        self.map_data_updated = 1	                        # being updated
        self.now_exit = False
        #
        self.l_mi_covid20=[
                ['Allegan',     1, 466, 885, (0,0,255)],
                ['Barry',       1, 540, 883, (0,0,255)],
                ['Bay',		2, 690, 695, (64,240,64)],
                ['Berrien',     8, 436, 955, (64,240,64)],
                ['Calhoun',     4, 569, 934, (64,240,64)],
                ['Charlevoix',	3, 577, 482, (64,240,64)],
                ['Chippewa',    1, 577, 310, (0,0,255)],
                ['Clare',       1, 590, 677, (0,0,255)],
                ['Clinton',     5, 615, 836,(64,240,64)],
                ['Detroit City',568, 808, 935, (64,240,64)],
                ['Emmet',       2, 609, 455, (64,240,64)],
                ['Eaton',	3, 591, 883, (64,240,64)],
                ['Genesee',	34, 710, 832, (64,240,64)],
                ['Gladwin',	2, 640, 681, (64,240,64)],
                ['Grand Traverse',3, 511, 577, (64,240,64)],
                ['Hillsdale',    1, 620, 992, (64,240,64)],
                ['Ingham',	15, 642, 887, (64,240,64)],
                ['Isabella',	2, 591, 735, (64,240,64)],
                ['Jackson',	1, 632, 934, (64,240,64)],
                ['Kalamazoo',	3, 540, 932, (0,0,255)],
                ['Kalkaska',	1, 567, 578, (64,240,64)],
                ['Kent',	28, 515, 834, (64,240,64)],
                ['Lapeer',	1, 767, 820, (64,240,64)],
                ['Leelanau',	1, 485, 537, (0,0,255)],
                ['Livingston',	9, 710, 882, (64,240,64)],
                ['Macomb',	175, 804, 882, (64,240,64)],
                ['Manistee',	1, 468, 606, (64,240,64)],
                ['Midland',     5, 643,732, (0,0,255)],
                ['Monroe',	7, 732, 986, (64,240,64)],
                ['Montcalm',	1, 566, 781, (0,0,255)],
                ['Muskegon',	1, 450, 760, (64,240,64)],
                ['Newaygo',	1, 488, 758, (64,240,64)],
                ['Oakland',	329, 744, 880, (64,240,64)],
                ['Otsego',	3, 615, 526, (64,240,64)],
                ['Ottawa',	11, 467, 836, (64,240,64)],
                ['Roscommon',	1, 641, 629, (0,0,255)],
                ['Saginaw',	2, 668, 780, (64,240,64)],
                ['St. Clair',	7, 844, 842, (64,240,64)],
                ['Tuscola',	1, 739, 767, (0,0,255)],
                ['Washtenaw',	42, 694, 935, (64,240,64)],
                ['Wayne',	227, 753, 933, (64,240,64)],
                ['Wexford',	1, 511, 628, (0,0,255)],
                ['Out of State', 4, 25, 85, (64,240,64)],
                ['Not Reported',2, 753, 933, (64,240,64)]
        ]							
        #data of coordination

        # import image of map
	self.img_map = cv2.resize(cv2.imread('mi_county2019.png'), (VIZ_W, VIZ_H))
	self.img_overlay = self.img_map.copy()
	self.data_daily = False   # otherwise overall
	# read latest data
	self.csv_pos_now, self.l_mi_cases = self.readDataByDay(9999999999)

        # main loop for processing
        while (not self.now_exit):
            self.cmdProcess( cv2.waitKeyEx(300), 19082601 )
            if(self.map_data_updated > 0):
                if(len(self.l_mi_cases) > 0):
                    self.img_overlay = self.img_map.copy()
                    self.infoShowCases(self.img_overlay, self.l_mi_cases)
                cv2.imshow("COVID-19 %.0f in Michigan"%2020, self.img_overlay)
                self.map_data_updated = 0
        self.exit_hook()
    ## key process
    def cmdProcess(self, key, t0):
        #print("cmdProcess")
        if(key == -1):  
            pass
        else:  
            self.map_data_updated = self.map_data_updated + 1
            pass

        if(key == -1):  
            pass
        elif(key == 65471 or key == 1114047):   # F2 key refresh newest from website
            self.data_daily = True
            self.cmdGrabDataFromWebsite(True)
            pass  
        elif(key == 65474 or key == 1114050):   # F5 key refresh newest from website
            self.data_daily = False
            self.cmdGrabDataFromWebsite(False)
            pass  
        elif(key == 65477 or key == 1114053):   # F8 key next day
            self.csv_pos_now, self.l_mi_cases = self.readDataByDay(0) 
        elif(key == 65478 or key == 1114054):   # F9 key previous day
            self.csv_pos_now, self.l_mi_cases = self.readDataByDay(self.csv_pos_now-1)   
        elif(key == 65479 or key == 1114055):   # F10 key next day
            self.csv_pos_now, self.l_mi_cases = self.readDataByDay(self.csv_pos_now+1) 
        elif(key == 65480 or key == 1114056):   # F11 key next day
            self.csv_pos_now, self.l_mi_cases = self.readDataByDay(9999999999) 
        elif(key == 114 or key == 1048690):  # r key
            self.infoShowRainbow(None, self.l_mi_cases) 
        elif(key == 115 or key == 1048691):  # s key
            cv2.imwrite('./results/mi_county'+self.name_file+'.png', self.img_overlay)
            pass
        elif(key == 27 or key == 1048603):  # esc
            self.now_exit = True
            pass  
        else:   
            print (key)
    ## step 2
    ## read data file given day offset
    def readDataByDay(self, pos):
        csv_data_files = sorted( [f for f in listdir('./data') if isfile(join('./data', f))] )
        #print('-----------', csv_data_files)
        if(pos >= len(csv_data_files) ): pos = len(csv_data_files) - 1
        elif(pos < 0): pos = 0
        offset = 11	
        year = int(csv_data_files[pos][offset:offset+4])
        month = int(csv_data_files[pos][offset+4:offset+6])
        day = int(csv_data_files[pos][offset+6:offset+8])
        self.name_file = '%d%02d%02d'%(year, month, day)
        self.now_date = '%d/%d/%d'%(month, day, year)
        #read data to list
        df_today = self.open4File()
        lst_data = self.parseDfData(df_today)
        self.data_daily = False
        return (pos, lst_data)
    ## save to csv 
    def save2File(self, l_data):
        if(self.data_daily):
            csv_name = './daily/mi_covid19_'+self.name_file+'.csv'
        else:
            csv_name = './data/mi_covid19_'+self.name_file+'.csv'        
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        for a_row in l_data:
            csvwriter.writerow(a_row)
        csv_data_f.close()
    ## open a csv 
    def open4File(self):
        csv_name = './data/mi_covid19_'+self.name_file+'.csv'
        df = pd.read_csv(csv_name)
        return df
    ## open a website 
    def open4Website(self, bDaily):
        if(bDaily):
            cov_tables = pd.read_html("https://www.michigan.gov/coronavirus/")
        else:
            cov_tables = pd.read_html("https://www.michigan.gov/coronavirus/0,9753,7-406-98163-520743--,00.html")
        # read 1st table: Overall Confirmed COVID-19 Cases by County
        return cov_tables[0]
    ## parse from exel format to list 
    def parseDfData(self, df, bSave=False):
        (n_rows, n_columns) = df.shape 
        # check shape

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
	if(bSave): self.save2File(lst_data)
	return lst_data
    ## step 1
    ## grab data from goverment website
    def cmdGrabDataFromWebsite(self, bDaily):
        # update date time
        dt_now = datetime.datetime.now()
	self.name_file = '%d%02d%02d'%(dt_now.year, dt_now.month, dt_now.day)
	self.now_date = '%d/%d/%d'%(dt_now.month, dt_now.day, dt_now.year)
        df = self.open4Website(bDaily)
        self.l_mi_cases = self.parseDfData(df, bSave=True)

    ## look up table to get pre-set information
    def lookupMapData(self, c_name):
        for cov in self.l_mi_covid20:
            if c_name in cov[0]:
                return cov
        print ('Not found', c_name)
        return [' ',	67, 10, 30, (0,0,255)]
    ## step 3
    ## show cases on the map
    def infoShowCases(self, img, l_cases):
        wish_total = 0
        n_total, ii = 0, 0
        line_h=14	
        offset_h = VIZ_H - line_h * len(l_cases)+25
        for a_case in l_cases:
            if('County' in a_case[0]):
                continue
            elif('Total' in a_case[0]):
                wish_total = int(a_case[1])
                continue
            else:
                n_total += int( a_case[1] )
                map_data = self.lookupMapData(a_case[0])
                # draw the list on the left
                cv2.putText(img, a_case[0], 
		        (10, ii*line_h+offset_h), 
		        cv2.FONT_HERSHEY_SIMPLEX, 
		        0.54,
		        map_data[4],
		        1) 
                cv2.putText(img, str(a_case[1]), 
		        (170, ii*line_h+offset_h), 
		        cv2.FONT_HERSHEY_SIMPLEX, 
		        0.54,
		        map_data[4],
		        1) 
                ii += 1
                if('Out of State' in a_case[0]): continue
                if('Not Reported' in a_case[0]): continue
                # draw on the map, select the location
                cv2.putText(img, str(a_case[1]), 
		        (map_data[2],map_data[3]), 
		        cv2.FONT_HERSHEY_DUPLEX, 
		        0.7,
		        map_data[4],
		        1) 
                continue
        print('total:', wish_total, n_total)
        if(wish_total == n_total):
            if(self.data_daily):
                info_cases = '%d Daily Confirmed'%(n_total)
                info_date = 'On ' + self.now_date + ' in MI'
            else:
                info_cases = '%d Overall Confirmed'%(n_total)
                info_date = 'Until ' + self.now_date + ' in MI'
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
        cv2.putText(img, 'press F5 to refresh', 
		    (782,205), 
		    cv2.FONT_HERSHEY_SIMPLEX, 
		    0.3,
		    (255,64,0),
		    1) 
            
    ## This shows one list such as an example
    # for example: self.infoShowCoronaVirus(self.l_mi_covid20)
    #
    def infoShowCoronaVirus(self, img, lst_data):

	n_total, ii = 0, 0		
        for cov in lst_data:
            n_total += cov[1]
            cv2.putText(img,cov[0] + '    %d'%(cov[1]), 
                (10, ii*15+360), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.5,
                cov[4],
                1) 
            ii += 1
            if('Out of State' in cov[0]): continue
            cv2.putText(img,'%d'%(cov[1]), 
                (cov[2],cov[3]), 
                cv2.FONT_HERSHEY_DUPLEX, 
                0.7,
                cov[4],
                1) 
        cv2.putText(img,'%d Confirmed Cases'%(n_total), 
            (240,30), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1,
            (255,64,0),
            1) 
        cv2.putText(img, self.now_date, 
            (405,65), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1,
            (255,64,0),
            1) 

    #
    def infoShowRainbow(self, img, lst_data):
        fig=plt.figure()
        ax=fig.add_subplot(111) 

        # clean list
        l_d_clean = []
        l_max_v = 0
        for a_case in lst_data:
            if('Total' in a_case[0]): continue
            if('Out of State' in a_case[0]): continue
            if('Not Reported' in a_case[0]): continue
            l_d_clean.append(a_case)
            if(a_case[1] > l_max_v): l_max_v = a_case[1]

        l_max_v = (int(l_max_v / 100.0) * 100 + 100 + 50)
        # sort list
        l_d_sort = sorted(l_d_clean, key=lambda k: k[1])
        len_data = len(l_d_sort)
        cmap=plt.get_cmap("jet")
        # draw list
        for ii in range( len(l_d_sort) ):
            fov = Wedge((0, 0), l_d_sort[ii][1]+50, 
                int(ii*360.0/len_data)+90, int((ii+1)*360.0/len_data+90), 
                color=cmap(float(ii)/len_data*0.6+0.2), alpha=1.0)
            ax.add_artist(fov)
            #
        plt.axis([-l_max_v, l_max_v, -l_max_v, l_max_v])
        plt.show()	    	
    ## exit node
    def exit_hook(self):
        print("bye bye, node virusviz")

## the entry of this application
if __name__ == '__main__':
        runVirusViz()
        cv2.destroyAllWindows()
        pass

## end of file
