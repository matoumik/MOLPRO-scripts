# -*- coding: utf-8 -*-
"""
file providing methods for parsing a single molpro out file
"""

import io
import re
import os

import datapoint as p

hartree= 27.21138602

re_occ = re.compile(r"\s*occ\s*=\s*(\S+)", re.I) 
re_method = re.compile(r"\s*1PROGRAM\s*\*\s*(\S+)")
re_basis = re.compile(r"\s*basis\s*=\s*(\S+)", re.I)
re_dist = re.compile(r"\s*SETTING R\(\S*\)\s*=\s*(\S*)")
re_CCSD_energy = re.compile(r"\s*!CCSD total energy\s*(\S*)")

def parse(outfilename,moleculename=""):
    outfile = io.open(outfilename,'r')
    points = list()

    for textline in outfile:
        m = re.match(re_occ,textline)
        if m:
            occ_t = m.group(1)
        
        m = re.match(re_basis,textline)
        if m:
            basis_t = m.group(1)
            
        m = re.match(re_dist,textline)
        if m:
            distance_t= m.group(1)
        
        m = re.match(re_method,textline)
        if m:
            method_t = m.group(1)
        
        
        
        #CCSD
        m = re.match(re_CCSD_energy,textline)
        if m:
            CCSDe = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,CCSDe,moleculename,basis_t,method=method_t)
            points.append(newpoint)
            
            
    outfile.close()
    return p.makelines(points)

def parsefolder(folderpath,moleculename="",
                molprooutfilename="molpro.out",
                mergeidenticallines=False):
    lines=list()
    for dirName, subdirList, fileList in os.walk(folderpath):
        for fname in fileList:
            if fname == molprooutfilename:
                print(dirName + "/" + fname)
                lines = lines + parse(dirName + "/" + fname, moleculename)
    
    if mergeidenticallines:
        lines = p.mergelines(lines)
        
    return lines            
                
