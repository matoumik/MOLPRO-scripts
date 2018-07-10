#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 23:33:19 2018

@author: mikulas
"""

import matplotlib.pyplot as plt
import datapoint as dp

def setupplot(xrange="", yrange=""):
    plt.clf()
    plt.xlabel(r'$R\,[\mathrm{\AA}]$')
    plt.ylabel(r'$E\,[\mathrm{eV}]$')
    if xrange != "":
        mi, ma = xrange
        plt.xlim(mi, ma)
    if yrange != "":
        mi, ma = yrange
        plt.ylim(mi, ma)

def plotadd(lines, color = "", title = ""):
    if color != "":
        if title != "":
            if type(lines) is dp.Linelist:
                first = True
                for line in lines:
                    if first:
                        plt.plot(line.distances(),line.energies(), color=color, label = title)
                        first = False
                    else:
                        plt.plot(line.distances(),line.energies(), color=color)
            else:
                plt.plot(lines.distances(),lines.energies(), color=color, label = title)
        else:
            if type(lines) is dp.Linelist:
                
                for line in lines:
                        plt.plot(line.distances(),line.energies(), color=color)
                    
            else:
                plt.plot(lines.distances(),lines.energies(), color=color,)
    
    else:
         if title != "":
            if type(lines) is dp.Linelist:
                first = True
                for line in lines:
                    if first:
                        plt.plot(line.distances(),line.energies(), color=color, title = title)
                        first = False
                    else:
                        plt.plot(line.distances(),line.energies(), color=color)
            else:
                plt.plot(lines.distances(),lines.energies(), color=color, title = title)
         else:
            if type(lines) is dp.Linelist:
                for line in lines:
                    plt.plot(line.distances(),line.energies())
            else:
                plt.plot(lines.distances(),lines.energies())

def writeplot(file="",title=False):
    if title:
        plt.legend()
    if file=="":
        plt.show()
    else:
        plt.savefig(file,dpi=300)
        

def plot(lines,file="",xrange = "",yrange = ""):
    setupplot(xrange,yrange)
    plotadd(lines)
    writeplot(file)
    
def refplot(reference, experimental,file="",xrange="",yrange = "",shift=True):
    setupplot(xrange,yrange)
    if shift:
        refmin=float('inf')
        expmin=float('inf')
        for line in reference:
            e, d = line.minimum()
            if e <refmin:
                refmin = e
        for line in experimental:
            e, d = line.minimum()
            if e <expmin:
                expmin = e
        for line in reference:
            line.setzero(refmin)
        for line in experimental:
            line.setzero(expmin)
    
    plotadd(reference, color='#D0D0B0')
    plotadd(experimental, color='#FF5050')
    writeplot(file)
    
    
        
    
    
    
    