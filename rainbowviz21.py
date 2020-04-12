#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			rainbowviz.py
#
#	visualize data in raibnow
#
#

from __future__ import print_function


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import pandas as pd
import csv
from os.path import isfile, join
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt
import math
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for rainbow
class rainbowViz(object):
    ## the start entry of this class
    def __init__(self, n_state):

        # create a node
        print("welcome to rainbowViz")
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
    #
    def isRealCounty(self, c_name, lst_counties):
        for a_county in lst_counties:
            if(c_name in a_county[3]): return True
        return False
    #
    def infoShowRainbow(self, type_data, lst_data, save_file=None, date=''):
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
        l_counties = []
        coord_f = self.state_dir + 'state_county_coord.csv'
        if(isfile(coord_f) ):
            l_counties = self.open4File(coord_f)

        for a_case in lst_data:
            if(self.isRealCounty(a_case[0], l_counties)): pass
            else: continue
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
            plt.text(-l_max_v+5, l_max_v-60, 'On '+date + ' in '+self.state_name)
        elif type_data ==2:
            plt.text(-l_max_v+10, l_max_v-140, '%d Overall confirmed COVID-19'%(n_total))
            plt.text(-l_max_v+10, l_max_v-240, 'Until '+date + ' in '+self.state_name)
        elif type_data ==3:
            plt.text(-l_max_v+10, l_max_v-20, '%d Overall deaths COVID-19'%(n_total))
            plt.text(-l_max_v+10, l_max_v-40, 'Until '+date + ' in '+self.state_name)
        plt.axis([-l_max_v, l_max_v, -l_max_v, l_max_v])
        fig.tight_layout()      
        ax.axis('off')  # get rid of the ticks and ticklabels
        plt.show()
        if(save_file is not None):
            fig.savefig(save_file)
  

## end of file
