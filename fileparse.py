# -*- coding: utf-8 -*-
"""
file providing methods for parsing a single molpro out file
"""

import io
import re
import os

import datapoint as p

hartree= 27.21138602


re_occ = re.compile(r"\s*occ\s*,\s*(\S+)", re.I) 
re_method = re.compile(r"\s*1PROGRAM\s*\*\s*(\S+)")
re_basis = re.compile(r"\s*basis\s*=\s*(\S+)", re.I)
re_dist = re.compile(r"\s*SETTING R\(\S*\)\s*=\s*(\S*)")
re_CCSD_energy = re.compile(r"\s*!CCSD total energy\s*(\S*)")
re_UCCSD_energy = re.compile(r"\s*!RHF-UCCSD energy\s*(\S*)")
re_RCCSD_energy = re.compile(r"\s*!RHF-RCCSD energy\s*(\S*)")
#re_CCSD_energy = re.compile(r"\s*!CCSD energy\s*(\S*)")
re_FCI_energy = re.compile(r"\s*!FCI STATE \S+\.\S+ Energy\s*(\S*)")
re_CI_energy = re.compile(r"\s*!MRCI STATE \S+\.\S+ Energy\s*(\S*)")
re_CI_sym = re.compile(r"\s*Reference symmetry:\s*(\S*)\s*(\S*)", re.I)
re_RCCSDT1_energy = re.compile(r"\s*!RHF-RCCSD\(T\) energy\s*(\S*)")
re_CCSDT1_energy = re.compile(r"\s*!CCSD\(T\) total energy\s*(\S*)")

def parse(outfilename,moleculename=""):
    outfile = io.open(outfilename,'r')
    points = list()
    occ_t=""

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
            
        #UCCSD
        m = re.match(re_UCCSD_energy,textline)
        if m:
            UCCSDe = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,UCCSDe,moleculename,basis_t,method="UCCSD")
            points.append(newpoint)
            
        #RCCSD
        m = re.match(re_RCCSD_energy,textline)
        if m:
            RCCSDe = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,RCCSDe,moleculename,basis_t,method="RCCSD")
            points.append(newpoint)
             
        #RCCSD(T)    
        m = re.match(re_RCCSDT1_energy,textline)
        if m:
            RCCSDT1e = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,RCCSDT1e,moleculename,basis_t,method="RCCSD(T)")
            points.append(newpoint)

	#CCSD(T)
        m = re.match(re_CCSDT1_energy,textline)
        if m:
            CCSDT1e = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,CCSDT1e,moleculename,basis_t,method="CCSD(T)")
            points.append(newpoint)
            
        #FCI TODO: more states
        m = re.match(re_FCI_energy,textline)
        if m:
            FCIe = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,FCIe,moleculename,basis_t,method=method_t)
            points.append(newpoint)
            
        #CI TODO: more states
        m = re.match(re_CI_sym,textline)
        if m:
            CIsym = m.group(1)
            CIspin = m.group(2)
            
        
        m = re.match(re_CI_energy,textline)
        if m:
            CIe = float(m.group(1))*hartree
            newpoint= p.Point(distance_t,CIe,moleculename,basis_t,method=method_t,occ=occ_t,symmetry=CIsym,spin=CIspin)
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
                
