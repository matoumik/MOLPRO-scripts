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

def plotadd(lines):
    if type(lines) is dp.Linelist:
        for line in lines:
            plt.plot(line.distances(),line.energies())
    else:
        plt.plot(lines.distances(),lines.energies())

def writeplot(file=""):
    if file=="":
        plt.show()
    else:
        plt.savefig(file,dpi=300)
        

def plot(lines,file="",xrange = "",yrange = ""):
    setupplot(xrange,yrange)
    plotadd(lines)
    writeplot(file)