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
import math

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
                ['Bay',		3, 690, 695, (64,240,64)],
                ['Berrien',     10, 436, 955, (64,240,64)],
                ['Calhoun',     6, 569, 934, (64,240,64)],
                ['Charlevoix',	4, 577, 482, (64,240,64)],
                ['Chippewa',    1, 577, 310, (0,0,255)],
                ['Clare',       1, 590, 677, (0,0,255)],
                ['Clinton',     6, 615, 836,(64,240,64)],
                ['Detroit City',705, 808, 935, (64,240,64)],
                ['Emmet',       2, 609, 455, (0,0,255)],
                ['Eaton',	3, 591, 883, (0,0,255)],
                ['Genesee',	46, 710, 832, (64,240,64)],
                ['Gladwin',	2, 640, 681, (0,0,255)],
                ['Grand Traverse',3, 511, 577, (0,0,255)],
                ['Hillsdale',    2, 620, 992, (64,240,64)],
                ['Ingham',	18, 642, 887, (64,240,64)],
                ['Iosco',	1, 718, 629, (64,240,64)],
                ['Isabella',	2, 591, 735, (0,0,255)],
                ['Jackson',	12, 632, 934, (64,240,64)],
                ['Kalamazoo',	5, 540, 932, (64,240,64)],
                ['Kalkaska',	2, 567, 578, (64,240,64)],
                ['Kent',	36, 515, 834, (64,240,64)],
                ['Lapeer',	1, 767, 820, (0,0,255)],
                ['Leelanau',	1, 485, 537, (0,0,255)],
                ['Lenawee',	1, 671, 991, (64,240,64)],
                ['Livingston',	16, 710, 882, (64,240,64)],
                ['Luce',	1, 508, 313, (64,240,64)],
                ['Macomb',	281, 804, 882, (64,240,64)],
                ['Manistee',	1, 468, 606, (0,0,255)],
                ['Marquette',	1, 266, 309, (64,240,64)],
                ['Midland',     6, 643,732, (0,0,255)],
                ['Monroe',	18, 732, 986, (64,240,64)],
                ['Montcalm',	2, 566, 781, (64,240,64)],
                ['Muskegon',	3, 450, 760, (0,0,255)],
                ['Newaygo',	1, 488, 758, (0,0,255)],
                ['Oakland',	543, 744, 880, (64,240,64)],
                ['Otsego',	6, 615, 526, (64,240,64)],
                ['Ottawa',	16, 467, 836, (64,240,64)],
                ['Roscommon',	1, 641, 629, (0,0,255)],
                ['Saginaw',	9, 668, 780, (64,240,64)],
                ['Sanilac',	2, 814, 780, (64,240,64)],
                ['St. Clair',	10, 844, 842, (64,240,64)],
                ['Tuscola',	2, 739, 767, (64,240,64)],
                ['Van Buren',	2, 466, 936, (64,240,64)],
                ['Washtenaw',	72, 694, 935, (64,240,64)],
                ['Wayne',	417, 753, 933, (64,240,64)],
                ['Wexford',	1, 511, 628, (0,0,255)],
                ['Out of State', 7, 25, 85, (64,240,64)],
                ['Not Reported',0, 753, 933, (64,240,64)]
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
            cv2.imwrite('./results/mi_county20200000.png', self.img_overlay)
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
        line_h=13	
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
		        0.53,
		        map_data[4],
		        1) 
                cv2.putText(img, str(a_case[1]), 
		        (170, ii*line_h+offset_h), 
		        cv2.FONT_HERSHEY_SIMPLEX, 
		        0.53,
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
                info_date = 'COVID-19 on ' + self.now_date + ' in MI'
            else:
                info_cases = '%d Overall Confirmed'%(n_total)
                info_date = 'COVID-19 until ' + self.now_date + ' in MI'
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
        cmap=plt.get_cmap("gist_rainbow")
        # draw list
        for ii in range( len(l_d_sort) ):
            fov = Wedge((0, 0-l_max_v/2), l_d_sort[ii][1]+50, 
                int(ii*360.0/len_data)+90, int((ii+1)*360.0/len_data+90), 
                color=cmap(1.0-(float(ii)/len_data*0.9+0.0)), 
                alpha=1.0)
            ax.add_artist(fov)
            #
            theta = (int(ii*360.0/len_data)+90) / 180.0*math.pi
            radian = l_d_sort[ii][1]+50 + 5
            plt.text(radian*math.cos(theta), radian*math.sin(theta)-l_max_v/2, 
                l_d_sort[ii][0], rotation=int(ii*360.0/len_data)+90,
                color=cmap(1.0-(float(ii)/len_data*0.9+0.0)), 
                rotation_mode='anchor')
                #horizontalalignment='center', verticalalignment='bottom')
            if(l_d_sort[ii][1] < 10): digi_len = 0
            elif(l_d_sort[ii][1] < 100): digi_len = 1
            elif(l_d_sort[ii][1] < 1000): digi_len = 2
            else: digi_len = 3
            radian = l_d_sort[ii][1]+50 - 5 - digi_len*5
            plt.text(radian*math.cos(theta), radian*math.sin(theta)-l_max_v/2, 
                '%d'%(l_d_sort[ii][1]), rotation=int(ii*360.0/len_data)+90,
                color='w', 
                rotation_mode='anchor')
        if(self.data_daily):
            plt.text(-150, 20, 'Daily confirmed COVID-19')
            plt.text(-150, 0, 'On '+self.now_date + ' in MI')
        else:
            plt.text(-200, 20, 'Overall confirmed COVID-19')
            plt.text(-200, 0, 'Until '+self.now_date + ' in MI')
        plt.axis([-l_max_v, l_max_v, -l_max_v, l_max_v])
        plt.show()
        #if(self.data_daily):
        #    fig.savefig('./results/mi_county'+self.name_file+'_daily.png')
	    	
    ## exit node
    def exit_hook(self):
        print("bye bye, node virusviz")

## the entry of this application
if __name__ == '__main__':
        runVirusViz()
        cv2.destroyAllWindows()
        pass

## end of file
