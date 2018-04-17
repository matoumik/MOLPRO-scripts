#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 00:32:58 2018

@author: mikulas
"""

import os

import datapoint as dp

class Gnuplot:
    def __init__(self,plotname="plot", plotlines=dp.Linelist(), style = "", output ="",xrange="",yrange =""):
        self.plotname=plotname
        self.lines = plotlines
        self.style = style
        self.output = output
        self.yrange = yrange
        self.xrange = xrange
        
    def writeplot(self, subdir=""):
        i = 0
        comma = False
        axistring = "set xlabel \"nuclear distance [{\\305}]\"\n set ylabel \"Energy [eV]\" \n set encoding iso_8859_1 \n"
        
        if self.yrange != "":
            yrangestring = "set yrange [" +self.yrange+ "]\n"
        else:
            yrangestring = ""
        
        if self.xrange != "":
            xrangestring = "set xrange [" +self.xrange+ "]\n"
        else:
            xrangestring = ""
            
            
        if self.output == "pdf":
            openfilestring = "set term pdf enhanced \n set output \"" + subdir + self.plotname + ".pdf\" \n"        
            closefilestring = "set output\n"
        else:
            openfilestring = ""
            closefilestring = ""
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
            "/"+str(i)+".plt\" "+self.style+" title \"" + str(line) + "\" "
            i=i+1
        
        
        plotfile = open(subdir + self.plotname + ".plt","w")
        plotfile.write("reset\n")
        plotfile.write(axistring)
        plotfile.write(xrangestring)
        plotfile.write(yrangestring)
        plotfile.write(openfilestring)
        plotfile.write(plotstring+"\n")
        plotfile.write(closefilestring)
        plotfile.close()

def makecompareplot(refline, otherlines, name, output="",xrange="",yrange=""):
    for line in (otherlines+refline):
        if line.method == "CI":
            line.setoutputtemplate("$M ($O)")
        else:
            line.setoutputtemplate("$M")
    tempplot = Gnuplot(name, refline + otherlines, "with linespoints", "pdf",xrange=xrange, yrange=yrange)
    tempplot.writeplot()
    
    i = 0
    diffname = name+"-diff"
    for temprefline in refline:
        if i>0:
            tempname = diffname +"_" + str(i)
        else:
            tempname = diffname
        plotlines = dp.Linelist()
        for templine in otherlines:
            plotlines.append(templine-temprefline)
        tempplot = Gnuplot(tempname, plotlines, "with linespoints", "pdf")
        tempplot.writeplot()
