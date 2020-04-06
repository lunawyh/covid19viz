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
import urllib
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import gmplot

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
        self.state_dir = './mi/'
        # Only the coordinates are used by code
        self.l_mi_county_coord= self.open4File (self.state_dir +'mi_county_cordination.csv')				
        #data of coordination

        # import image of map
        self.img_map = cv2.resize(cv2.imread(self.state_dir+'mi_county2019.png'), (VIZ_W, VIZ_H))
        self.img_overlay = self.img_map.copy()
        self.data_daily = False   # otherwise overall
        # read latest data
        self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(999999)

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
        elif(key == 65471 or key == 1114047 or key == 7405568):   # F2 key refresh newest from website
            self.data_daily, self.l_mi_cases = self.readDataDaily(True)
            pass
        elif(key == 65472 or key == 1114048 or key == 7405569):   # F3 key gmaps
            self.showGmaps()
            pass  
        elif(key == 65474 or key == 1114050):   # F5 key refresh newest from website
            self.data_daily = False

            pos, self.l_mi_cases, self.l_cases_yest = self.cmdGrabDataFromWebsite()
            if(len(self.l_mi_cases) > 0):
                self.img_overlay = self.img_map.copy()
                self.infoShowCases(self.img_overlay, self.l_mi_cases)
                cv2.imwrite(self.state_dir + 'results/mi_county'+self.name_file+'.png', self.img_overlay)
                if(self.isNameOnToday(self.name_file)):
                    cv2.imwrite(self.state_dir + 'results/mi_county20200000.png', self.img_overlay)
            pass  
        elif(key == 65477 or key == 1114053 or key == 7798784):   # F8 key next day
            self.data_daily = False
            self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(0) 
        elif(key == 65478 or key == 1114054 or key == 7864320):   # F9 key previous day
            self.data_daily = False
            self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(self.csv_pos_now-1)   
        elif(key == 65479 or key == 1114055 or key == 7929856):   # F10 key next day
            self.data_daily = False
            self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(self.csv_pos_now+1) 
        elif(key == 65480 or key == 1114056 or key == 7995392):   # F11 key next day
            self.data_daily = False
            self.csv_pos_now, self.l_mi_cases, self.l_cases_yest = self.readDataByDay(9999999999) 
        elif(key == 65481 or key == 1114057 or key == 7995393):   # F12 key next day
            self.predictByModelSir()
        elif(key == 114 or key == 1048690):  # r key
            if self.data_daily == True: type_data=1
            else: type_data =2
            self.infoShowRainbow(type_data, self.l_mi_cases) 
        elif(key == 100 or key == 1048676):  # d key
            if(self.data_daily): return
            list_death= self.getDataListDeath(self.l_mi_cases)
            self.infoShowRainbow(3, list_death) 
        elif(key == 115 or key == 1048691):  # s key
            cv2.imwrite(self.state_dir + 'results/mi_county'+self.name_file+'.png', self.img_overlay)
            if(self.isNameOnToday(self.name_file)):
                cv2.imwrite(self.state_dir + 'results/mi_county20200000.png', self.img_overlay)
            pass
        elif(key == 27 or key == 1048603):  # esc
            self.now_exit = True
            pass  
        else:   
            print (key)
    ## step 2
    ## read data file given day offset
    def readDataByDay(self, pos):
        print('readDataByDay...', pos)
        data_dir = self.state_dir + 'data'
        csv_data_files = sorted( [f for f in listdir(data_dir) if isfile(join(data_dir, f))] )
        #print('-----------', csv_data_files)
        if(pos >= len(csv_data_files) ): pos = len(csv_data_files) - 1
        elif(pos < 0): pos = 0
        if( len(csv_data_files[pos]) != 23): return (pos, [])
        offset = 11	
        year = int(csv_data_files[pos][offset:offset+4])
        month = int(csv_data_files[pos][offset+4:offset+6])
        day = int(csv_data_files[pos][offset+6:offset+8])
        self.name_file = '%d%02d%02d'%(year, month, day)
        self.now_date = '%d/%d/%d'%(month, day, year)
        #read data to list
        lst_data = self.open4File(self.state_dir + 'data/mi_covid19_'+self.name_file+'.csv')
        
        #read data on yesterday 
        name_last = self.getOverallYesterday(self.name_file)
        if(name_last is not None):
            lst_data_last = self.open4File(self.state_dir + 'data/' + name_last)
        else:
            lst_data_last = []
        return (pos, lst_data, lst_data_last)
    ## save to csv 
    def save2File(self, l_data, csv_name):
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        # make sure the 1st row is colum names
        if('County' in l_data[0][0]): pass
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
    ## open a website 
    def open4Website(self, fRaw):
        #csv_url = "https://www.michigan.gov/coronavirus/0,9753,7-406-98163-520743--,00.html"
        csv_url = 'https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html'
        # save html file
        urllib.urlretrieve(csv_url, fRaw)
        # read tables
        cov_tables = pd.read_html(csv_url)
        # read 1st table: Overall Confirmed COVID-19 Cases by County
        return cov_tables[0]
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
        dt_now = datetime.datetime.now()
        dt_name_file = '%d%02d%02d'%(dt_now.year, dt_now.month, dt_now.day)
        if f_name == dt_name_file:
            return True
        else:
            return False
    ## step 1
    ## grab data from goverment website
    def cmdGrabDataFromWebsite(self):
        print('cmdGrabDataFromWebsite...')
        # update date time
        dt_now = datetime.datetime.now()
        self.name_file = '%d%02d%02d'%(dt_now.year, dt_now.month, dt_now.day)
        self.now_date = '%d/%d/%d'%(dt_now.month, dt_now.day, dt_now.year)
        f_name = self.state_dir + 'data_html/mi_covid19_'+self.name_file+'.html'
        df_a = self.open4Website(f_name)
        f_name = self.state_dir + 'data/mi_covid19_'+self.name_file+'.csv'
        lst_data = self.parseDfData(df_a, fName=f_name)

        #read data on yesterday 
        name_last = self.getOverallYesterday(self.name_file)
        if(name_last is not None):
            lst_data_last = self.open4File(self.state_dir + 'data/' + name_last)
        else:
            lst_data_last = []
        return (0, lst_data, lst_data_last)
    def getOverallYesterday(self, today):
        data_dir = self.state_dir + 'data'
        csv_data_files = sorted( [f for f in listdir(data_dir) if isfile(join(data_dir, f))] )
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
        csv_daily = self.state_dir + 'daily/mi_covid19_'+self.name_file+'.csv'
        csv_all_today = self.state_dir + 'data/mi_covid19_'+self.name_file+'.csv'
        csv_all_last = self.getOverallYesterday(self.name_file)
        if(csv_all_last is None): return False
        else: print('  ', csv_daily, csv_all_today, csv_all_last)
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
        self.save2File(l_daily, csv_daily)
        return True
    def readDataDaily(self, bDaily):
        csv_name = self.state_dir + 'daily/mi_covid19_'+self.name_file+'.csv'
        print('readDataDaily', csv_name)
        if(isfile(csv_name) ):
            lst_data = self.open4File(csv_name)
        else:
            if( self.generateDataDaily(True)): 
                lst_data = self.open4File(csv_name)
            else: return (False, [])
        
        return (True, lst_data)
    ## look up table to get pre-set information
    def lookupMapData(self, c_name, lst_data):
        c_name_clean = c_name.replace('*', '').replace('.', '')
        for cov in lst_data:
            if c_name_clean in cov[0]:
                return True, cov
        #print ('Not found', c_name)
        return False, [' ', 0, 10, 30, (0,0,255)]
    ## look up table to get pre-set information
    def getColorByCompare(self, case_today, lst_data=None):
        if(self.data_daily): return ( (0,255,0) )
        bfound, case_last = self.lookupMapData(case_today[0], self.l_cases_yest)
        if( int(case_today[1]) - int(case_last[1]) > 0): return ( (0,255,0) )
        else: return ( (0,0,255) )

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
        offset_h = VIZ_H - line_h * len(l_cases)/2-25
        for a_case in l_cases:
            if('County' in a_case[0]):
                continue
            elif('Total' in a_case[0]):
                wish_total = int(a_case[1])
                continue
            else:
                if(ii < len(l_cases)/2): 
                    posx = 10
                    posy = ii*line_h+offset_h
                else: 
                    posx = 180+10
                    posy = (ii-len(l_cases)/2)*line_h+offset_h
                n_total += int( a_case[1] )
                bFound, map_data = self.lookupMapData(a_case[0], self.l_mi_county_coord)
                nColor = self.getColorByCompare(a_case)
                # draw the list on the left
                cv2.putText(img, a_case[0], 
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
                if('Out of State' in a_case[0]): continue
                if('Other' in a_case[0]): continue
                if('Not Reported' in a_case[0]): continue
                if('Unknown' in a_case[0]): continue
                # draw on the map, select the location
                cv2.putText(img, str(a_case[1]), 
		        (map_data[2],map_data[3]), 
		        cv2.FONT_HERSHEY_DUPLEX, 
		        0.7,
		        nColor,
		        1) 
                if(map_data[2] < 200 and map_data[3] < 200): print('Missing', a_case)
                continue
        #print('total:', wish_total, n_total)
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
        else:
            print( '  wished total: %d, listed total: %d'%( wish_total, n_total) )
        cv2.putText(img, 'press F5 to refresh', 
		    (782,205), 
		    cv2.FONT_HERSHEY_SIMPLEX, 
		    0.3,
		    (255,64,0),
		    1) 
            
    ## This shows one list such as an example
    # for example: self.infoShowCoronaVirus(self.l_mi_county_coord)
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
            if('Other' in cov[0]): continue
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
    def infoShowRainbow(self, type_data, lst_data):
        print('infoShowRainbow...', type_data)
        fig=plt.figure()
        ax=fig.add_subplot(111)
        fig.set_figheight(10)
        fig.set_figwidth(10)

        # select colum
        if (type_data==3):col=2
        else : col=1
        # clean list
        l_d_clean = []
        l_max_v = 0
        for a_case in lst_data:
            if('Total' in a_case[0]): continue
            if('Out of State' in a_case[0]): continue
            if('Unknown' in a_case[0]): continue
            if('Other' in a_case[0]): continue
            if('Not Reported' in a_case[0]): continue
            if('County' in a_case[0]): continue
            l_d_clean.append(a_case)
            if(int(a_case[col]) > l_max_v): l_max_v = int(a_case[col])
        n_total=0		
        for a_case in lst_data:
            if('Total' in a_case[0]): continue
            if('County' in a_case[0]): continue
            n_total += int(a_case[col])

        l_max_v += 100 + 50  # base 50*2 + name 25*2
        center_y = -(l_max_v/2 - 75)
        l_max_v = (int(l_max_v / 50.0+1) * 50) / 2
        # sort list
        l_d_sort = sorted(l_d_clean, key=lambda k: int(k[col]))
        len_data = len(l_d_sort)
        cmap=plt.get_cmap("gist_rainbow")
        # draw list
        for ii in range( len(l_d_sort) ):
            l_value = int(l_d_sort[ii][col])
            fov = Wedge((0, 0+center_y), l_value+50, 
                int(ii*360.0/len_data)+90, int((ii+1)*360.0/len_data+90), 
                color=cmap(1.0-(float(ii)/len_data*0.9+0.0)), 
                alpha=1.0)
            ax.add_artist(fov)
            #
            theta = (int(ii*360.0/len_data)+90) / 180.0*math.pi
            radian = l_value+50 + 5
            plt.text(radian*math.cos(theta), radian*math.sin(theta)+center_y, 
                l_d_sort[ii][0], rotation=int(ii*360.0/len_data)+90,
                color=cmap(1.0-(float(ii)/len_data*0.9+0.0)), 
                rotation_mode='anchor')
                #horizontalalignment='center', verticalalignment='bottom')
            if(l_value < 10): digi_len = 0
            elif(l_value < 100): digi_len = 1
            elif(l_value < 1000): digi_len = 2
            else: digi_len = 3
            radian = l_value+50 - 10 - digi_len*l_max_v/40
            plt.text(radian*math.cos(theta), radian*math.sin(theta)+center_y, 
                '%d'%(l_value), rotation=int(ii*360.0/len_data)+90,
                color='w', 
                rotation_mode='anchor')
        if(type_data==1):
            plt.text(-l_max_v+5, l_max_v-30, '%d Daily confirmed COVID-19'%(n_total))
            plt.text(-l_max_v+5, l_max_v-60, 'On '+self.now_date + ' in MI')
        elif type_data ==2:
            plt.text(-l_max_v+10, l_max_v-40, '%d Overall confirmed COVID-19'%(n_total))
            plt.text(-l_max_v+10, l_max_v-80, 'Until '+self.now_date + ' in MI')
        elif type_data ==3:
            plt.text(-l_max_v+10, l_max_v-20, '%d Overall deaths COVID-19'%(n_total))
            plt.text(-l_max_v+10, l_max_v-40, 'Until '+self.now_date + ' in MI')
        plt.axis([-l_max_v, l_max_v, -l_max_v, l_max_v])
        plt.show()
        if(type_data==1):
            fig.savefig(self.state_dir + 'results/mi_county'+self.name_file+'_daily.png')
            if(self.isNameOnToday(self.name_file)):
                fig.savefig(self.state_dir + 'results/mi_county20200000_daily.png')
        elif(type_data==3):
            fig.savefig(self.state_dir + 'results/mi_county'+self.name_file+'_death.png')
            if(self.isNameOnToday(self.name_file)):
                fig.savefig(self.state_dir + 'results/mi_county20200000_death.png')
    # refer to https://github.com/HCui91/covid-19-model	    	
	#   https://zhuanlan.zhihu.com/p/104645873
    def SIR(self, t, beta, gamma):
	    # Total population, N.
	    N = 1000000
	    # Initial number of infected and recovered individuals, I0 and R0.
	    I0, R0 = 65, 65.0/239.0*25.0
	    # Everyone else, S0, is susceptible to infection initially.
	    S0 = N - I0 - R0

	    # The SIR model differential equations.
	    # @njit
	    def deriv(y, t, N, beta, gamma):
		S, I, R = y
		dSdt = -beta * S * I / N
		dIdt = beta * S * I / N - gamma * I
		dRdt = gamma * I
		return dSdt, dIdt, dRdt

	    # Initial conditions vector
	    y0 = S0, I0, R0
	    # Integrate the SIR equations over the time grid, t.
	    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
	    S, I, R = ret.T
	    return I

    #
    def predictByModelSir(self, type_data=0):
        print('predictByModelSir...', type_data)
        # read all data file
        csv_data_files = sorted( [f for f in listdir(self.state_dir + 'data') if isfile(join(self.state_dir + 'data', f))] )
        lst_data_overall = []
        # read total number from data file
        offset = 11	
        for ff in csv_data_files:             
            l_data_day = self.open4File(join(self.state_dir + 'data', ff))
            for a_day in l_data_day:
                if 'Total' in a_day[0]:
                    lst_data_overall.append(a_day[1])
                    break

        # get daily new cases
        lst_data_daily = []
        #lst_data_daily.append(0)
        for ii in range(len(lst_data_overall)):
            if ii < 1: continue  # lst_data_daily.append(lst_data_overall[ii])     
            else: lst_data_daily.append(lst_data_overall[ii] - lst_data_overall[ii-1])  

        # predict the future
        data = lst_data_daily
        #print(lst_data_overall)
        #data.append( int(data[-1] * 0.98) )
        days = np.arange(0, len(data), 1)
        popt, pcov = curve_fit(self.SIR, days, data)
        print(' contact parameter, recovery rate:', popt)
        print(" R0:", 1/popt[0], "Recovery days:", 1/popt[1])
        print(' Covariance matrix:', pcov)

        fig = plt.figure(0)
        fig.set_figheight(10)
        fig.set_figwidth(20)
        plt.scatter(days, data, label="Actual new cases per day", color='r')
        date_s = 18
        date_len = int(2*len(data))
        day_future = np.arange(0, date_len, 1)
        day_mmdd = []
        for jj in range(date_len):
            if(jj<=13): month, day = 3, (date_s + jj)%32 
            elif(jj<=43): month, day = 4, (date_s + jj - 31)%31  
            elif(jj<=74): month, day = 5, (date_s + jj - 31 - 30)%32  
            else: month, day = 6, (date_s + jj - 31 - 30 - 31)%31  
            day_mmdd.append( '%d/%d'%(month,day) )
            
        plt.plot(day_mmdd, self.SIR(day_future, *popt), label="Predicted new cases per day(unreal)")
        plt.legend()
        plt.xlabel('Date in 2020')
        plt.ylabel('Confirmed Daily New Cases')
        plt.title("COVID-19 Prediction of daily new cases in Michigan")
        plt.xticks(rotation=45)
        plt.show()
        if(self.isNameOnToday(self.name_file)):
            fig.savefig(self.state_dir + 'results/mi_county20200000_predict.png')

    ## GMAPS
    def showGmaps(self):
        print('showGmaps...')
        with open('../google_api_key20.txt') as f:
            api_key1 = f.readline()
            #print('api_key', api_key1)
            f.close
        gmap = gmplot.GoogleMapPlotter(44.838134, -86.428187, 7)
        gmap.apikey = api_key1
        golden_gate_park_lats, golden_gate_park_lons = zip(*[
	    (42.595074, -83.184570),
	    (42.594671, -83.183937),
	    (42.591369, -83.186737),
	    (42.592167, -83.187971),
	    (42.595074, -83.184570)
	    ])
        gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)
        gmap.draw( "./gmaps2020a.html" )
        '''
        gmaps.configure(api_key=api_key1)
        #Define location 1 and 2
        Durango = (37.2753,-107.880067)
        SF = (37.7749,-122.419416)
        #Create the map
        fig = gmaps.figure()
        #create the layer
        layer = gmaps.directions.Directions(Durango, SF,mode='car')
        #Add the layer
        fig.add_layer(layer)
        fig
        '''
    ## exit node
    def exit_hook(self):
        print("bye bye, node virusviz")

## the entry of this application
if __name__ == '__main__':
        runVirusViz()
        cv2.destroyAllWindows()
        pass

## end of file
