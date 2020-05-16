#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			mapviz.py
#
#	visualize data in map
#
#

from __future__ import print_function


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================
import math
import numpy as np
import csv
from os.path import isfile, join
import pandas as pd
#
# In Windows
#   download http://download.osgeo.org/osgeo4w/osgeo4w-setup-x86_64.exe and install
#     https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi
#   pip install pyproj==1.9.6
#   set the system environment variable: GEOS_DIR=C:\OSGeo4W64
#                                                         PROJ_DIR=C:\OSGeo4W64
#   add    C:\OSGeo4W64\bin to PATH
#   pip install --user git+https://github.com/matplotlib/basemap.git
# In Linux
#   sudo pip install https://github.com/matplotlib/basemap/archive/master.zip
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for mapping
class mapViz(object):
    ## the start entry of this class
    def __init__(self, l_config, n_state):

        # create a node
        print("welcome to mapViz")
        self.state_name = n_state
        self.state_dir = './'+n_state.lower()+'/'
        self.l_state_config = l_config
        self.pl_timer = None
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
    ## save to csv 
    def saveToFileCoordinate(self, l_data, csv_name):
        csv_data_f = open(csv_name, 'w')
        # create the csv writer 
        csvwriter = csv.writer(csv_data_f)
        # make sure the 1st row is colum names
        csvwriter.writerow(['USPS','GEOID','ANSICODE','NAME','ALAND','AWATER',\
            'ALAND_SQMI','AWATER_SQMI','INTPTLAT','INTPTLONG','ROTATE','NOTES'])
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
    ## look up table to get pre-set information
    def lookupMapData(self, c_name, lst_data):
        c_name_clean = c_name.replace('*', '').replace('.', '')
        for cov in lst_data:
            if c_name_clean in cov[0]:
                return True, cov
        #print ('Not found', c_name)
        return False, [' ', 0, 10, 30, (0,0,255)]
    ## look up table to get pre-set information
    def getColorByCompare(self, case_today, lst_data=[]):
        #if(self.data_daily): return ( (0,255,0) )
        bfound, case_last = self.lookupMapData(case_today[0], lst_data)
        if( int(case_today[1]) - int(case_last[1]) > 0): return True
        else: False

    ## GMAPS
    def isExitedCounty(self, l_counties, a_county):
        #print('isExitedCounty...')
        for a_city in l_counties:
            if(a_city[3] in a_county): return True
        return False
    ## GMAPS
    def getCountiesInState(self, state):
        #print('getCountiesInState...')
        lst_us_cities = self.open4File('./ne_maps/2019_Gaz_counties_national.csv')
        lst_counties = []
        for a_city in lst_us_cities:
            #if(a_city[5] == 0): continue
            a_city[3] = a_city[3].replace(' County', '')
            if( (a_city[0] in state) and (not self.isExitedCounty(lst_counties, a_city[3])) ):
                lst_counties.append(a_city)
        return lst_counties
    ## get County Info
    def getCountyInfo(self, l_counties, a_county):
        c_color = '#eedd99'
        for a_item in l_counties:
            if(a_county in a_item[3]):   # .lower()
                c_color = a_item[11]
                break
        #print(a_county, c_color)
        return c_color
    ## get County Info
    def getCountyCenterSize(self, a_state):
        l_centers = self.open4File('./ne_maps/us_states_info.csv')
        for a_item in l_centers:
            if(a_state in a_item[0]):
                if(float(self.l_state_config[8][1]) != 0): lat_2 = float(self.l_state_config[8][1])
                else: lat_2 = float(a_item[1])
                if(float(self.l_state_config[8][2]) != 0): lon_2 = float(self.l_state_config[8][2])
                else: lon_2 = float(a_item[2])
                if(float(self.l_state_config[9][1]) != 0): s_2 = float(self.l_state_config[9][1])
                else: 
                    ratio = math.sqrt( float(a_item[5])/56803.82 )
                    s_2 = 370000.0*ratio
                return (lat_2, lon_2, s_2)
        return (41.850033, -87.6500523, 370000.0)
    ## get position Info in the list
    def isNextList(self, index, lat_1, lon_1):
        isNext = False
        lat_2, lon_2 = 0, 0
        for jj in range(int(self.l_state_config[10][1])):
            if (index == int(self.l_state_config[13+jj][3]) ):
                lat_2, lon_2 = lat_1+float(self.l_state_config[13+jj][1]), lon_1+float(self.l_state_config[13+jj][2])
                isNext = True
                break
        return (isNext, lat_2, lon_2)
    ## set County Info
    def setCountyInfo(self, l_counties, l_cases):
        case_max, case_col, case_total = 0, 0.0, 0
        for a_item in l_cases:
            if('Total' in a_item[0]): continue
            if('County' in a_item[0]): continue
            if(a_item[1] > case_max): case_max = a_item[1]
            case_total += a_item[1]
        c_color = 'w'
        cmap=plt.get_cmap("Blues")
        #l_info = []
        for a_item in l_counties:
            bFound, map_data = self.lookupMapData(a_item[3], l_cases)
            if(bFound): 
                a_item[1] = map_data[1]
                a_item[2] = map_data[2]
                case_r = float(a_item[1]) / float(case_max)
                if(case_r >= 0.6): case_col = 1.0
                elif(case_r >= 0.5): case_col = 0.9
                elif(case_r >= 0.3): case_col = 0.8
                elif(case_r >= 0.15): case_col = 0.7
                elif(case_r >= 0.1): case_col = 0.6
                elif(case_r >= 0.01): case_col = 0.5
                elif(case_r >= 0.001): case_col = 0.4
                elif(case_r >= 0.0001): case_col = 0.3
                elif(case_r >= 0.00001): case_col = 0.2
                else: case_col = 0.1
                a_item[11] = cmap(case_col)
            else:
                a_item[11] = c_color
                a_item[1] = 0
                a_item[2] = 0
            #l_info.append(a_item)
        return case_total
    # generic function for reading polygons from file and plotting them on the map. This works with Natural Earth shapes.
    def drawShapesFromFile(self, filename,facecolor,edgecolor,m,ax,l_counties):
            m.readshapefile(filename, 'temp', drawbounds = False)
            patches = []
            for info, shape in zip(m.temp_info, m.temp): 
                patches = []
                if(self.l_state_config[6][1] in info['STATE_NAME']):
                    facecolor2 = self.getCountyInfo(l_counties, info['NAME'])
                    pass
                else:
                    continue
                patches.append( Polygon(np.array(shape), True) )
                ax.add_collection(PatchCollection(patches, facecolor=facecolor2, edgecolor=edgecolor, linewidths=1))
    def close_event(self):
        self.pl_timer.stop()
        plt.close() #timer calls this function after 3 seconds and closes the window 
    ## GMAPS
    def showCountyInMap(self, l_cases_today, l_type=2, l_last=[], save_file=None, date='', timeout=0):
        print('showCountyInMap...')
        # 10. read name of counties
        coord_f = self.state_dir + 'state_county_coord.csv'
        if(isfile(coord_f) ):
            l_counties = self.open4File(coord_f)
        else:
            l_counties = self.getCountiesInState(self.state_name)
            l_d_sort = sorted(l_counties, key=lambda k: k[3])
            self.saveToFileCoordinate( l_d_sort, coord_f)
        # 15. set latest cases infomation
        n_total = self.setCountyInfo(l_counties, l_cases_today)
        
        # 20. create plot
        fig = plt.figure()
        fig.set_figheight(11)
        fig.set_figwidth(11)
        ax = fig.add_subplot(111)
        if(timeout > 10):
            self.pl_timer = fig.canvas.new_timer(interval = timeout) #creating a timer object and setting an interval of xxx milliseconds
            self.pl_timer.add_callback(self.close_event)
        # 30. create base map
        landColor, coastColor, oceanColor, popColor, countyColor = '#eedd99','#93ccfa','w','#ffee99','#ff0000'
        lat_1, lon_1, s_1 = self.getCountyCenterSize(self.state_name)
        print('  County Center', lat_1, lon_1, s_1)
        m = Basemap(projection='ortho',lon_0=lon_1,lat_0=lat_1,resolution='l',llcrnrx=-s_1,llcrnry=-s_1,urcrnrx=s_1,urcrnry=s_1)
        m.drawmapboundary(fill_color=oceanColor) # fill in the ocean

        # 40. plot counties
        #gdf = gpd.read_file('./ne_maps/UScounties/UScounties.shp')
        #print(gdf.columns) # [u'NAME', u'STATE_NAME', u'STATE_FIPS', u'CNTY_FIPS', u'FIPS', u'geometry']
        #print(gdf[gdf['STATE_NAME'] == 'Michigan'])
        # read the higher resolution Natural Earth coastline (land polygons) shapefile and display it as a series of polygons
        # refer to https://gis.stackexchange.com/questions/136028/finding-gps-coordinates-of-geographic-center-of-us-counties
        self.drawShapesFromFile('./ne_maps/UScounties/UScounties',landColor,coastColor,m,ax,l_counties)
        m.drawcounties(color=countyColor)

        # 50. draw name of counties
        for a_county in l_counties:	
            lat2, lon2 = float(a_county[8]), float(a_county[9])
            x, y = m(lon2, lat2) 
            plt.text(x, y, a_county[3],fontsize=8, ha='center',va='center',color='k',rotation=a_county[10])
        # 55. draw list of counties
        ii = 0
        for a_case in l_cases_today:	
            if('Total' in a_case[0]): continue
            if('County' in a_case[0]): continue
            isNext, lat_2, lon_2 = self.isNextList(ii, lat_1, lon_1)
            if(isNext): lat2, lon2 = lat_2, lon_2
            if( self.getColorByCompare(a_case, l_last) ): nColor = 'g'
            else: nColor = 'y'
            # show name
            lat2 -= 0.1
            x, y = m(lon2, lat2) 
            plt.text(x, y, a_case[0],fontsize=8, ha='left',va='center',color=nColor)
            # show number
            x, y = m(lon2 + 1.0, lat2) 
            plt.text(x, y, str(a_case[1]),fontsize=8, ha='left',va='center',color=nColor)
            ii += 1
           
        # 58. draw title 
        if(l_type==1):
            lat2, lon2 = lat_1+float(self.l_state_config[11][1]), lon_1+float(self.l_state_config[11][2])
            x, y = m(lon2, lat2) 
            plt.text(x, y, '%d Daily confirmed COVID-19'%(n_total),fontsize=20, ha='left',va='center',color='g')
            lat2 -= 0.2
            x, y = m(lon2, lat2) 
            plt.text(x, y, 'On '+date + ' in '+self.state_name,fontsize=16, ha='left',va='center',color='g')
        elif l_type ==2:
            lat2, lon2 = lat_1+float(self.l_state_config[11][1]), lon_1+float(self.l_state_config[11][2])
            x, y = m(lon2, lat2) 
            plt.text(x, y, '%d Overall confirmed'%(n_total),fontsize=20, ha='left',va='center',color='g')
            lat2 -= 0.2
            x, y = m(lon2, lat2) 
            plt.text(x, y, 'COVID-19 Until '+date + ' in '+self.state_name,fontsize=16, ha='left',va='center',color='g')
        # 59. draw logo 
        lat2, lon2 = lat_1+float(self.l_state_config[12][1]), lon_1+float(self.l_state_config[12][2])
        x, y = m(lon2, lat2) 
        arr_lena = mpimg.imread('./doc/app_qrcode_logo.png')
        imagebox = OffsetImage(arr_lena)  # , zoom=0.15)
        ab = AnnotationBbox(imagebox, (x, y))
        ax.add_artist(ab)
        ax.axis('off')  # get rid of the ticks and ticklabels
        # 60. show all
        fig.tight_layout()      
        if(timeout > 10):
            self.pl_timer.start()
        plt.show()
        if(save_file is not None):
            fig.savefig(save_file)
  

## end of file
