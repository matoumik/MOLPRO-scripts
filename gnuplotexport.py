#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 00:32:58 2018

@author: mikulas
"""

import os

class Gnuplot:
    def __init__(self,plotname="plot", plotlines=list()):
        self.plotname=plotname
        self.lines = plotlines
        
    def writeplot(self, subdir=""):
        i = 0
        comma = False
        plotstring = "plot"
        try:
            os.mkdir(subdir + self.plotname)
        except:
            pass
        
        for line in self.lines:
            line.writeplotdatafile(subdir + self.plotname +"/"+str(i)+".plt")
            if comma:
                plotstring = plotstring + ","
            else:
                comma = True    
            
            plotstring = plotstring + " \"" + subdir + self.plotname + \
            "/"+str(i)+".plt\" title \"" + str(line) + "\" "
            i=i+1
        
        
        plotfile = open(subdir + self.plotname + ".plt","w")
        plotfile.write(plotstring)
        plotfile.close
