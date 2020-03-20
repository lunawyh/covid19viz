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

VIZ_W  = 599
VIZ_H  = 681
# ==============================================================================
# -- codes -------------------------------------------------------------------
# ==============================================================================

# class for mapping
class runVirusViz(object):
    ## the start entry of this class
    def __init__(self):

        # create a node
        print("welcome to node virusviz")
        #initialize
        size = VIZ_H, VIZ_W, 3
        self.fca_overlay = np.zeros(size, dtype=np.uint8)	# overlay image
        self.map_data_updated = 1	# being updated
        self.now_exit = False
        self.num_date = 20

	self.fca_overlay = cv2.imread('mi_county2020.png')
        while (not self.now_exit):
            self.cmdProcess( cv2.waitKeyEx(300), 19082601 )
            if(self.map_data_updated > 0):
                self.infoShowCoronaVirus(self.fca_overlay)
                cv2.imshow("COVID-19 %.0f in Michigan"%2020, self.fca_overlay)
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
        elif(key == 115 or key == 1048691):  # s key
            cv2.imwrite('./results/mi_county202003%d.png'%(self.num_date), self.fca_overlay)
            pass
        elif(key == 27 or key == 1048603):  # esc
            self.now_exit = True
            pass  
        else:   
            print (key)
    ## Show SAV 
    def infoShowCoronaVirus(self, img):
        l_mi_covid19_20200318=[
                ['Bay',		1, 465, 480],
                ['Charlevoix',	1, 380, 322],
                ['Detroit',	13, 540, 645],
                ['Ingham',	2, 440, 600],
                ['Jackson',	1, 442, 633],
                ['Kent',	5, 360, 559],
                ['Leelanau',	1, 320, 355],
                ['Macomb',	10, 550, 600],
                ['Monroe',	1, 510, 670],
                ['Montcalm',	1, 380, 537],
                ['Oakland',	23, 500, 600],
                ['Otsego',	1, 425, 355],
                ['Ottawa',	1, 320, 570],
                ['St. Clair',	2, 580, 570],
                ['Washtenaw',	7, 470, 635],
                ['Wayne',	10, 510, 630]
        ]
        l_mi_covid19=[
                ['Bay',		1, 465, 480, (0,0,255)],
                ['Charlevoix',	1, 380, 322, (0,0,255)],
		['Clinton',     1, 436, 559,(64, 240,64)],
                ['Detroit',	75, 550, 645, (64,240,64)],
		['Eaton',	2, 413, 601, (64,240,64)],
                ['Ingham',	6, 440, 600, (64,240,64)],
                ['Jackson',	1, 442, 633, (0,0,255)],
                ['Kent',	7, 360, 559, (64,240,64)],
                ['Leelanau',	1, 320, 355, (0,0,255)],
                ['Livingston',	1, 476, 600, (64,240,64)],
                ['Macomb',	55, 550, 600, (64,240,64)],
                ['Midland',     1, 445,490, (64,240,64)],
                ['Monroe',	2, 510, 670, (0,0,255)],
                ['Montcalm',	1, 380, 537, (0,0,255)],
                ['Oakland',	105, 500, 600, (64,240,64)],
                ['Otsego',	1, 425, 355, (0,0,255)],
                ['Ottawa',	1, 320, 570, (0,0,255)],
                ['St. Clair',	4, 570, 570, (0,0,255)],
                ['Washtenaw',	14, 470, 635, (0,0,255)],
                ['Wayne',	44, 510, 630, (64,240,64)],
                ['nonreported', 10, 25, 85, (64,240,64)]
        ]

        l_mi_covid20=[
                ['Bay',		1, 465, 480, (0,0,255)],
                ['Charlevoix',	1, 380, 322, (0,0,255)],
		['Clinton',     1, 436, 559,(0,0,255)],
                ['Detroit',	149, 550, 645, (64,240,64)],
		['Eaton',	2, 413, 601, (0,0,255)],
                ['Genesee',	1, 492, 554, (64,240,64)],
                ['Ingham',	7, 440, 600, (64,240,64)],
                ['Jackson',	1, 442, 633, (0,0,255)],
                ['Kent',	12, 352, 559, (64,240,64)],
                ['Leelanau',	1, 320, 355, (0,0,255)],
                ['Livingston',	3, 476, 600, (64,240,64)],
                ['Macomb',	86, 550, 600, (64,240,64)],
                ['Midland',     3, 445,490, (64,240,64)],
                ['Monroe',	3, 510, 670, (64,240,64)],
                ['Montcalm',	1, 380, 537, (0,0,255)],
                ['Oakland',	184, 500, 600, (64,240,64)],
                ['Otsego',	1, 425, 355, (0,0,255)],
                ['Ottawa',	1, 320, 570, (0,0,255)],
                ['St. Clair',	7, 570, 570, (64,240,64)],
                ['Washtenaw',	16, 470, 635, (64,240,64)],
                ['Wayne',	67, 510, 630, (64,240,64)],
                ['Out-of-state', 1, 25, 85, (64,240,64)]
        ]

	n_total, ii = 0, 0		
        for cov in l_mi_covid20:
            n_total += cov[1]
            cv2.putText(img,cov[0] + '    %d'%(cov[1]), 
                (10, ii*15+360), 
                cv2.FONT_HERSHEY_DUPLEX, 
                0.5,
                cov[4],
                1) 
            ii += 1
            if('Out-of-state' in cov[0]): continue
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
        cv2.putText(img,'3/%d/2020'%(self.num_date), 
            (405,65), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1,
            (255,0,0),
            1) 
	    	
    ## exit node
    def exit_hook(self):
        print("bye bye, node virusviz")

## the entry of this application
if __name__ == '__main__':
        runVirusViz()
        cv2.destroyAllWindows()
        pass

## end of file
