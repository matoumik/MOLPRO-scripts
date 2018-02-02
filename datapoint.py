#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:04:54 2018

@author: mikulas
"""
__Name__ = "datapoint"

import re

B = re.compile("\$B")
D = re.compile("\$D")
E = re.compile("\$E")
G = re.compile("\$G")
M = re.compile("\$M")
N = re.compile("\$N")
O = re.compile("\$O")
S = re.compile("\$S")
L = re.compile("\$L")
U = re.compile("\$U")


class Point:
    """ dfa """
    def __init__(self,distance,energy,
                   moleculename="",basis="", method ="",occ="",numberofelectrons="",
                   symmetry="",spin="",number=""):
        
        self.moleculename=moleculename
        self.basis=basis
        self.method=method
        self.occ=occ
        self.numberofelectrons=numberofelectrons
        self.symmetry=symmetry       
        self.number=number
        self.distance=distance
        self.energy=energy
        self.spin=spin
        self.strtemplate="$D -- $E"
        
    def __str__(self):
        ret = self.strtemplate
        ret = re.sub(B, self.basis, ret)
        ret = re.sub(D,str(self.distance),ret)
        ret = re.sub(E,self.numberofelectrons,ret)
        ret = re.sub(G,str(self.energy),ret)
        ret = re.sub(M,self.method,ret)
        ret = re.sub(N, self.number, ret)
        ret = re.sub(O,self.occ, ret)
        ret = re.sub(S,self.spin, ret)
        ret = re.sub(L,self.symmetry, ret)
        ret = re.sub(U,self.moleculename,ret)
        
        return ret
    
    def __repr__(self):
        
        ret = "$B,$D,$E,$G,$M,$N,$O,$S,$L"
        ret = self.strtemplate
        ret = re.sub(B, self.basis, ret)
        ret = re.sub(D,str(self.distance),ret)
        ret = re.sub(E,self.numberofelectrons,ret)
        ret = re.sub(G,str(self.energy),ret)
        ret = re.sub(M,self.method,ret)
        ret = re.sub(N, self.number, ret)
        ret = re.sub(O,self.occ, ret)
        ret = re.sub(S,self.spin, ret)
        ret = re.sub(L,self.symmetry, ret)
        ret = re.sub(U,self.moleculename,ret)
        
        return ret
    
    def setoutputtemplate(self,OutputTemplate):
        self.strtemplate = OutputTemplate
        
class Line:
    def __init__(self,points,
                   moleculename="",basis="",method="",occ="",numberofelectrons="",
                   symmetry="",spin="",number="",strtemplate="$U-$M-$B"):
        self.moleculename=moleculename
        self.basis=basis
        self.method=method
        self.occ=occ
        self.numberofelectrons=numberofelectrons
        self.symmetry=symmetry       
        self.number=number
        self.spin=spin
        self.points=points
        self.strtemplate = strtemplate
        
    def __str__(self):
        ret = self.strtemplate
        ret = re.sub(B, self.basis, ret)
        ret = re.sub(E,self.numberofelectrons,ret)
        ret = re.sub(M,self.method,ret)
        ret = re.sub(N, self.number, ret)
        ret = re.sub(O,self.occ, ret)
        ret = re.sub(S,self.spin, ret)
        ret = re.sub(L,self.symmetry, ret)
        ret = re.sub(U,self.moleculename,ret)
        
        return ret
    
    def __repr__(self):
        ret = "$B,$E,$M,$N,$O,$S,$L"
        ret = re.sub(B, self.basis, ret)
        ret = re.sub(E,self.numberofelectrons,ret)
        ret = re.sub(M,self.method,ret)
        ret = re.sub(N, self.number, ret)
        ret = re.sub(O,self.occ, ret)
        ret = re.sub(S,self.spin, ret)
        ret = re.sub(L,self.symmetry, ret)
        ret = re.sub(U,self.moleculename,ret)
        
        return ret
    
    def addline(self,line):
        self.points = self.points + line.points
        
    def __eq__(self,other):
        return self.__repr__() == other.__repr__() 
    
    def writeplotdatafile(self,filename):
        datafile = open(filename,"w")
        for point in self.points:
            datafile.write(str(point.distance)+" "+str(point.energy)+"\n")
        datafile.close()
        
    def setoutputtemplate(self,OutputTemplate):
        self.strtemplate = OutputTemplate
        
    
    
def makelines(points):
    lines = list()
    for point in points:
        lines.append(Line([point],moleculename=point.moleculename,basis=point.basis,
                          method = point.method,
                            occ=point.occ, numberofelectrons=point.numberofelectrons,
                            symmetry=point.symmetry, number=point.number,
                            spin=point.spin
                            ))
    
    return mergelines(lines)

def mergelines(lines):
    newlines = list()
    for line in lines:
        notmatched = True
        for newline in newlines:
            if newline==line:
                newline.addline(line)
                notmatched = False
        if notmatched:
            newlines.append(line)
    
    return newlines

def chooselines(lines, moleculename="",basis="",method="",
                occ="",numberofelectrons="",
                symmetry="",spin="",number=""):
    newlines = list()
    for line in lines:
        if isin(moleculename, line.moleculename) and \
        isin(basis,line.basis) and isin(method, line.method) and\
        isin(occ,line.occ) and isin(numberofelectrons, line.numberofelectrons) and\
        isin(symmetry,line.symmetry) and isin(spin, line.spin) and\
        isin(number,line.number):
            newlines.append(line)
    
    return newlines

        
def isin(thelist, themember):
    if thelist == "":
        return True
    elif themember == "":
        return True
    elif type(thelist) is list:
        if themember in thelist:
            return True
    elif thelist == themember:
        return True
    else:
        return False
