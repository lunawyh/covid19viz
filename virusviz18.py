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
            cv2.imwrite('mi_county20200317.png', self.fca_overlay)
            pass
        elif(key == 27 or key == 1048603):  # esc
            self.now_exit = True
            pass  
        else:   
            print (key)
    ## Show SAV 
    def infoShowCoronaVirus(self, img):
        l_mi_covid19=[
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
	for cov in l_mi_covid19:
	    
	    cv2.putText(img,'%d'%(cov[1]), 
		    (cov[2],cov[3]), 
		    cv2.FONT_HERSHEY_DUPLEX, 
		    1,
		    (0,0,255),
		    1) 
        cv2.putText(img,'Confirmed Cases', 
            (310,30), 
            cv2.FONT_HERSHEY_DUPLEX, 
            1,
            (255,64,0),
            1) 
        cv2.putText(img,'3/%d/2020'%(19), 
            (10,650), 
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
