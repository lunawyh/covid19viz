#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			predictionviz.py
#
#	visualize data in raibnow
#
#

from __future__ import print_function


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import numpy as np
import pandas as pd
import csv
from os.path import isfile, join
import matplotlib.pyplot as plt
from os import listdir
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import datetime 
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for prediction
class predictionViz(object):
    ## the start entry of this class
    def __init__(self, n_state):

        # create a node
        print("welcome to predictionViz")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.pl_timer = None
    ## parse from exel format to list 
    def parseDfData(self, df, fName=None):
        (n_rows, n_columns) = df.shape 
        # check shape
        #print('parseDfData', df.shape)
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
    # refer to https://github.com/HCui91/covid-19-model	    	
	#   https://zhuanlan.zhihu.com/p/104645873
    def SIR(self, t, beta, gamma):
        # Total population, N.
        N = 1000000.0
        # Initial number of infected and recovered individuals, I0 and R0.
        I0, R0 = 65.0, 65.0/239.0*25.0
        # Everyone else, S0, is susceptible to infection initially.
        S0 = N - I0 - R0

        # The SIR model differential equations.
        # @njit
        def deriv(y, t, N, beta, gamma):
            S, I, R = y
            dSdt = -beta * S * I / N
            dIdt = beta * S * I / N - gamma * I
            dRdt = gamma * I / N    # add dividing by N
            return dSdt, dIdt, dRdt

        # Initial conditions vector
        y0 = S0, I0, R0
        # Integrate the SIR equations over the time grid, t.
        ret = odeint(deriv, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T
        return I

    #    ## open a xlsx 
    def open4Xlsx(self, xlsx_name):
        if(isfile(xlsx_name) ):
            xl_file = pd.ExcelFile(xlsx_name)
            df = xl_file.parse('COVID-19 Cases')
            l_data = self.parseDfData(df)
        else: return []
        return l_data
    def close_event(self):
        self.pl_timer.stop()
        plt.close() #timer calls this function after 3 seconds and closes the window 
    def predictByModelSir(self, save_file=None, timeout=0):
        print('predictByModelSir...')
        day_mmdd = []
        lst_data_overall = []
        if (self.state_name in 'TX'):
            # read all data_raw file
            csv_data_files = sorted( [f for f in listdir(self.state_dir + 'data_raw') if isfile(join(self.state_dir + 'data_raw', f))] )
            if( len(csv_data_files) < 1): return False
            if( 'total' in csv_data_files[-1]): 
                print("  ./tx/data_raw/"+csv_data_files[-1])
                l_data_day = self.open4Xlsx("./tx/data_raw/"+csv_data_files[-1])
            else: return False
            for a_day in l_data_day:
                #print(a_day)
                if 'Total' in str(a_day[0]) or '56' in str(a_day[0]):
                    lst_data_overall = a_day[11:]
                    print(' Total is read', a_day[0])
                    #    lst_data_overall.append(int(a_number))
                if 'County Name' in str(a_day[0]) or 'Cases' in str(a_day[0]):
                    for a_date in a_day[11:]:
                        day_mmdd.append(a_date.replace('Cases \n', ''))
                    print(' Date is read', a_day[0])
                    #day_mmdd = a_day[0:]
            if( len(day_mmdd) < 1): return False
            dt_s = datetime.datetime.strptime('2020-'+day_mmdd[-1], '%Y-%m-%d')         
        else:
            # read all data file
            csv_data_files = sorted( [f for f in listdir(self.state_dir + 'data') if isfile(join(self.state_dir + 'data', f))] )
            if( len(csv_data_files) < 1): return False

            offset = 11	
            # read total number from data file
            for ff in csv_data_files:             
                l_data_day = self.open4File(join(self.state_dir + 'data', ff))
                for a_day in l_data_day:
                    if 'Total' in str(a_day[0]):
                        lst_data_overall.append(a_day[1])
                        dt_s = datetime.datetime.strptime(ff[offset:offset+8], '%Y%m%d')
                        day_mmdd.append( dt_s.strftime('%m/%d') )
                        break
        #print(lst_data_overall)
        # get daily new cases
        lst_data_daily = []
        #lst_data_daily.append(0)
        for ii in range(len(lst_data_overall)):
            if ii < 1: continue  # lst_data_daily.append(lst_data_overall[ii])     
            else: lst_data_daily.append( float(lst_data_overall[ii] - lst_data_overall[ii-1]) )
        day_mmdd = day_mmdd[1:]  # the 1st day is removed

        # predict the future
        if(self.state_name in 'OH'): preDay = 19
        elif(self.state_name in 'MI'): 
            preDay = 23  # len(lst_data_daily) - 15
            print('  preDay %d length %d'%( preDay, len(lst_data_daily) - preDay) )
        else: preDay = 0
        postDay = 0
        data = lst_data_daily[preDay:]  #[0:-1] postDay
        day_mmdd = day_mmdd[preDay:]    # postDay   
        #if(self.state_name in 'MI'): data[-2] = data[-1] * 1.15 # updated on 4/12/2020
        if(len(data) < 2): return False
        days = np.arange(0.0, len(data), 1.0)
        popt, pcov = curve_fit(self.SIR, days, data)
        print(' contact parameter, recovery rate:', popt)
        print(" R0:", 1/popt[0], "Recovery days:", 1/popt[1])
        print(' Covariance matrix:', pcov)

        fig = plt.figure(0)
        fig.set_figheight(10)
        fig.set_figwidth(20)
        if(timeout > 10):
            self.pl_timer = fig.canvas.new_timer(interval = timeout) #creating a timer object and setting an interval of xxx milliseconds
            self.pl_timer.add_callback(self.close_event)
        plt.scatter(day_mmdd, data, label="Actual new cases per day", color='r')

        date_len = int(len(data)+30)
        day_future = np.arange(0, date_len, 1)
        for jj in range(date_len-len(data)):
            dt_s += datetime.timedelta(days=1) 
            day_mmdd.append( dt_s.strftime('%m/%d') )
            
        plt.plot(day_mmdd, self.SIR(day_future, *popt), label="Predicted new cases per day(unreal)")
        plt.legend()
        plt.xlabel('Date in 2020')
        plt.ylabel('Confirmed Daily New Cases')
        plt.title("COVID-19 Prediction of daily new cases in " + self.state_name)
        plt.xticks(rotation=45)
        fig.tight_layout()      
        if(timeout > 10):
            self.pl_timer.start()
        plt.show()
        if(save_file is not None):
            fig.savefig(save_file)
            return True
        return False

## end of file
