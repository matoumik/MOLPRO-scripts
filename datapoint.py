#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:04:54 2018

@author: mikulas
"""
__Name__ = "datapoint"

import re
import numpy as np

distepsilon=0.01

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
        ret = re.sub(N, str(self.number), ret)
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
        ret = re.sub(N, str(self.number), ret)
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
        ret = re.sub(N, str(self.number), ret)
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
        ret = re.sub(N, str(self.number), ret)
        ret = re.sub(O,self.occ, ret)
        ret = re.sub(S,self.spin, ret)
        ret = re.sub(L,self.symmetry, ret)
        ret = re.sub(U,self.moleculename,ret)
        
        return ret
    
    def __iter__(self):
        return iter(self.points)
    
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
        
    def __sub__(self,y):
        if False: #TODO compare type
            print("Warning - substracting lines of different types")
        
        newline=Line(list(),
                   moleculename=self.moleculename,basis=self.basis,method=self.method,occ=self.occ,numberofelectrons=self.numberofelectrons,
                   symmetry=self.symmetry,spin=self.spin,number=self.number,strtemplate=self.strtemplate) 
        for firstpoint in self.points:
            for secondpoint in y.points:
                if abs(float(secondpoint.distance) - float(firstpoint.distance)) < distepsilon:
                    newpoint = firstpoint
                    newpoint.energy = firstpoint.energy - secondpoint.energy
                    newline.points.append(newpoint)
        return newline
    
    def cut(self, mindist="", maxdist=""):
        newline = Line(list(),
                   moleculename=self.moleculename,basis=self.basis,method=self.method,occ=self.occ,numberofelectrons=self.numberofelectrons,
                   symmetry=self.symmetry,spin=self.spin,number=self.number,strtemplate=self.strtemplate) 
        for point in self.points:
            if ((mindist == "" or point.distance>mindist) and (maxdist == "" or point.distance<maxdist)):
                newline.points.append(point)
        return newline
    
    def distsort(self):
        self.points.sort(key=lambda x: x.distance)
        return self
        #self.points.sort(key=lambda x: x.distance)
    
    def minimum(self):
        minimum = self.points[0]
        for point in self.points:
            if point.energy<minimum.energy:
                minimum = point
        
        return minimum.energy, minimum.distance
    
    def distances(self):
        self.distsort()
        dists = list()
        for point in self.points:
            dists.append(point.distance)
        return dists
        
    def energies(self):
        self.distsort()
        energs = list()
        for point in self.points:
            energs.append(point.energy)
        return energs
        
    def asymptotice(self):
        self.distsort()
        return self.points[-1].energy
        
    def extendtozero(self):
        self.distsort()
        self.addpoint(0,self.points[0].energy+20)
        
    def removepoints(self):
        self.points = list()
        return self
            
    def addpoint(self,distance,energy):
        newpoint = Point(distance,energy,
                   moleculename=self.moleculename,basis=self.basis, 
                   method =self.method,occ=self.occ,numberofelectrons=self.numberofelectrons,
                   symmetry=self.symmetry,spin=self.spin,number=self.number)
        self.points.append(newpoint)
        self.distsort()


        
        
    
def makelines(points):
    lines = Linelist()
    for point in points:
        lines.append(Line([point],moleculename=point.moleculename,basis=point.basis,
                          method = point.method,
                            occ=point.occ, numberofelectrons=point.numberofelectrons,
                            symmetry=point.symmetry, number=point.number,
                            spin=point.spin
                            ))
    
    return mergelines(lines)

def mergelines(lines):
    newlines = Linelist()
    for line in lines:
        notmatched = True
        for newline in newlines:
            if newline==line:
                newline.addline(line)
                notmatched = False
        if notmatched:
            newlines.append(line)
    for line in newlines:
        line.points.sort(key=lambda x: float(x.distance))
    
    return newlines

def chooselines(lines, moleculename="",basis="",method="",
                occ="",numberofelectrons="",
                symmetry="",spin="",number=""):
    newlines = Linelist()
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
    elif type(thelist) is Linelist:
        if themember in thelist:
            return True
    elif type(thelist) is list:
        if themember in thelist:
            return True
    elif type(thelist) is tuple:
        if themember in thelist:
            return True
    elif thelist == themember:
        return True
    else:
        return False

class Linelist(list):
    def __init__(self, *args):
        super(Linelist, self).__init__(args)
    
    def __sub__(self, alist):
        newlines = Linelist()
        for line1 in self:
            for line2 in alist:
                newlines.append(line1-line2)
        return newlines
    def __add__(self,alist):
        newlines = Linelist()
        for line in self:
            newlines.append(line)
        for line in alist:
            newlines.append(line)
        return newlines

    def setoutputtemplate(self,template):
        for line in self:
            line.setoutputtemplate(template)
