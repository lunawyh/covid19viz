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
    def predictByModelSir(self, save_file=None):
        print('predictByModelSir...')
        # read all data file
        csv_data_files = sorted( [f for f in listdir(self.state_dir + 'data') if isfile(join(self.state_dir + 'data', f))] )
        if( len(csv_data_files) < 1): return False
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
        data = lst_data_daily[5:]  #[0:-1]
        #print(lst_data_overall)
        #data.append( int(data[-1] * 0.9) )
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
        plt.title("COVID-19 Prediction of daily new cases in " + self.state_name)
        plt.xticks(rotation=45)
        fig.tight_layout()      
        plt.show()
        if(save_file is not None):
            fig.savefig(save_file)
            return True
        return False

## end of file
