#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 20:46:19 2018

@author: mikulas
"""
import io,re,os

deftemplate = """***, !!!NAME!!
memory,64,m
gprint,basis,orbitals=10,civector
gexpec,dm
symmetry,x,y
angstrom
geometry={
!!GEOM!!
}
PSPACE.1.0

!!BASIS!!
!!OCC!!
!!FROZEN!!

rs      = [ !!DISTS!! ]

do k = 1, #rs

  r(k) = rs(k)

 !!METHOD!!

enddo
"""
shparttemplate = """#!/bin/bash

# set required memory
#PBS -l mem=2g
#PBS -l walltime=24:00:00

# submit this script with 
# ~$ qsub main_job.sh

echo This calculation was done on
less $PBS_NODEFILE

#Remember the submit directory for later
SbmtDir=$PBS_O_WORKDIR

#THIS SCRIPT IS BEING EXECUTED ON THE NODE, ALL THE I/O SHOULD USE LOCAL DISC
#DRIVE /SCRATCH
# Here, we create the scratch directory for the job, copy all the data from
# submit directory there, and move there to execute the calculation
export SCRATCH=/scratch/$USER/$PBS_JOBID
mkdir -p $SCRATCH
cp -r $SbmtDir/* $SCRATCH/.
cd $SCRATCH
CurrDir=$PWD

# set no limits for STACK size
ulimit -s unlimited

# set the intel compiler and MKL environment variables
module load intel

# set the number of threads available for multi-threaded MKL routines
#export MKL_NUM_THREADS=4

# HERE COMES THE ACTUAL CALCULATION - CALL OF THE MAIN BINARY ETC.

/opt/MOLPRO/molpro/molpros_2012_1_Linux_x86_64_i8/bin/molpro --no-xml-output molpro.in
# DON'T FORGET TO REMOVE AUX. FILES BEFORE COPYING DATA BACK TO $HOME 

# COPY THE RESULTS BACK TO THE SUBMIT DIR IN $HOME
cd $CurrDir
cp -r * $SbmtDir/. && rm -rf *
cd $SbmtDir

# CLEAN THE SCRATCH
rmdir $SCRATCH && echo "scratch cleaned"
"""

reMN = re.compile("!!NAME!!")
reGE = re.compile("!!GEOM!!")
reBA = re.compile("!!BASIS!!")
reDI = re.compile("!!DISTS!!")
reME = re.compile("!!METHOD!!")
reOC = re.compile("!!OCC!!")
reFR = re.compile("!!FROZEN!!")
class Molprojob:
    def __init__(self,name=".",templatefile="",molname="", geom ="", basis="", occ="", frozen=""):
        self.name = name
        if templatefile != "":
            f= io.open(templatefile,'r')
            self.template = ""
            for line in f:
                self.template = self.template + line
            f.close()
        else:
            self.template = deftemplate
            
        self.molname = molname
        self.geom = geom
        
        if basis == "":
            self.basis = ""
        else:
            self.basis = "basis = " + basis
        
        if occ == "":
            self.occ = ""
        else:
            self.occ = "occ," + occ
            
        if frozen == "":
            self.frozen = ""
        else:
            self.frozen = "frozen," + frozen
        
        
        
        self.ranges = list()
        self.methods = ""
        
        
        
    def addranges(self, ranges):
        self.ranges = self.ranges + ranges
        
    def setranges(self, ranges):
        self.ranges = ranges
    
    def addrange(self, rangelist):
        self.ranges.append(rangelist)
        
    def writeinfile(self,dists,filename):
        strdists=" "
        comma=False
        for dist in dists:
            if comma:
                strdists = strdists + ", "
            else:
                comma = True
            strdists = strdists + str(dist)
        infile = self.template
        infile = re.sub(reMN, self.molname, infile)
        infile = re.sub(reGE, self.geom, infile)
        infile = re.sub(reBA, self.basis, infile)
        infile = re.sub(reOC, self.occ, infile)
        infile = re.sub(reFR, self.frozen, infile)
        infile = re.sub(reDI, strdists, infile)
        infile = re.sub(reME, self.methods, infile)

        #print(infile)
        f = io.open(filename,'w')
        f.write(infile)
        f.close()
    def writerunfile(self,filename):
        f = io.open(filename,'w')
        f.write(shparttemplate)
        f.close()
        
    def makejob(self):
        try:
            os.mkdir(self.name)
        except:
            pass;
        
        if len(self.ranges)==1:
            for therange in self.ranges:
                self.writeinfile(therange, self.name+"/molpro.in")
                self.writerunfile(self.name+"/run.sh")                
        elif len(self.ranges)>1:
            i = 1
            runfile="#!/bin/bash\n\n"
            for arange in self.ranges:
                if len(arange)>0:
                    dirn = self.name+"/range"+str(i)
                    try:
                        os.mkdir(dirn)
                    except:
                        pass;
                    
                    self.writeinfile(arange, dirn+"/molpro.in")
                    self.writerunfile(dirn+"/runpart.sh")
                    runfile=runfile + "cd range"+str(i)+"\n qsub runpart.sh\n cd ..\n"
                    i=i+1
            f = io.open(self.name+"/runall.sh", "w")
            f.write(runfile)
            f.close()
            #os.chmod(self.name+"/runall.sh",0777)
    
    def removemethods(self):
        self.methods = ""
        
    def addRHF(self, nelec, sym, spin):
        self.methods = self.methods +\
        "{rhf;\n" + wf(nelec,sym,spin) + "\n}\n\n"
            
    def addUHF(self, nelec, sym, spin):
        self.methods = self.methods +\
        "{uhf;\n" + wf(nelec,sym,spin) + "\n}\n\n"
        
    def addFCI(self, nelec, sym, spin, states=-1):
        self.methods = self.methods +\
        "{fci;\n" + wf(nelec,sym,spin,states) + "\n ORBITAL,IGNORE_ERROR;\n}\n\n"
       
    def addCCSDT1(self, nelec, sym, spin):
        self.methods = self.methods +\
        "{CCSD(T);\n" + wf(nelec,sym,spin) + "\n ORBITAL,IGNORE_ERROR;\n}\n\n"
       
    def addRCCSDT1(self, nelec, sym, spin):
        self.methods = self.methods +\
        "{RCCSD(T);\n" + wf(nelec,sym,spin) + "\n ORBITAL,IGNORE_ERROR;\n}\n\n"

    def addMULTI1(self, nelec, sym, spin):
        self.methods = self.methods +\
        "{multi;\n" + wf(nelec,sym,spin) + "ORBITAL,IGNORE_ERROR;\n \n }\n\n" #
        
    def addMULTI(self, states, weights):
        self.methods = self.methods + "{multi;\n"
        i = 0
        for state in states:
            nelec = state[0]
            sym = state[1]
            spin = state[2]
            nstat = state[3]
            self.methods += wf(nelec,sym,spin, nstat) + "weight"
            for weight in weights[i]:
                self.methods+=","+str(weight)
            self.methods+=";\n"
            i+=1
        self.methods += "ORBITAL,IGNORE_ERROR;\n \n }\n\n" #


    def addCI(self, nelec, sym, spin, states):
        self.methods = self.methods +\
        "{ci;\n" + wf(nelec,sym,spin,states) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" #
        
    def MULTI_BeH_ne(self, weights = ""):
        self.methods = self.methods +\
        "{rhf;\n" + wf(6,1,0) + "\n}\n\n"+\
        "{multi;" + "\n" + wf(5,1,1,7) + "\n" +\
        wf(5,2,1,6) + "\n" +\
        wf(5,3,1,6) + "\n" +\
        wf(5,4,1,1) + "\n" +\
        wf(5,2,3,1) + "\n" +\
        wf(5,3,3,1) + "\n" +\
        "ORBITAL,IGNORE_ERROR;\n \n }\n\n" #
    
    def CI_BeH_ne(self):
        self.MULTI_BeH_ne()
        self.methods = self.methods +\
        "{ci;\n"  + wf(5,1,1,7) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{ci;\n"  + wf(5,2,1,6) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{ci;\n" + wf(5,3,1,6) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{ci;\n" + wf(5,4,1,1) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{ci;\n" + wf(5,2,3,1) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n"  +\
        "{ci;\n" + wf(5,3,3,1) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n"
    
    def FCI_BeH_ne(self):
        self.methods = self.methods +\
        "{rhf;\n" + wf(6,1,0) + "\n}\n\n"+\
        "{fci;\n"  + wf(5,1,1,7) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{fci;\n"  + wf(5,2,1,6) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{fci;\n" + wf(5,3,1,6) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{fci;\n" + wf(5,4,1,1) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{fci;\n" + wf(5,2,3,1) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n" +\
        "{fci;\n" + wf(5,3,3,1) + "ORBITAL,IGNORE_ERROR;\n\n }\n\n"
        
    def MULTI_OH_ne(self, weights = ""):
        self.methods = self.methods +\
        "{rhf;\n" + wf(10,1,0) + "\n}\n\n"+\
        "{multi;states,10;" +"\n" +\
        "ORBITAL,IGNORE_ERROR;\n \n }\n\n" #
        
    def CI_OH_ne(self):
        self.MULTI_OH_ne()
        self.methods = self.methods +\
        "{ci;states,10;\n" + "ORBITAL,IGNORE_ERROR;\n\n }\n\n"
        
    def FCI_OH_ne(self):
        self.methods = self.methods +\
        "{rhf;\n" + wf(10,1,0) + "\n}\n\n"+\
        "{fci;state,10;\n" +"ORBITAL,IGNORE_ERROR;\n\n }\n\n"


def makedistrange(mind, maxd, step):
    dists = list()
    if mind < maxd:
        i = mind
        while i < maxd:
            dists.append(i)
            i = i + step
        dists.append(i)
    else:
        i = mind
        while i > maxd:
            dists.append(i)
            i = i - step
        dists.append(i)
    
    return dists

def splitdistrange(distrange,size):
    ranges = list()
    temprange= list()
    i=1
    for dist in distrange:
        temprange.append(dist)
        if i % size == 0:
            ranges.append(temprange)
            temprange = list()
        i=i+1
    try:
        ranges.append(temprange)
    except:
        pass
    return ranges
        
def gediat(el1, el2):
    return el1 + " ,,   0.0, 0.0, -r(k)/2\n" + el2 + " ,,   0.0, 0.0, r(k)/2"
           
def wf(nelec,sym,spin,states=-1):
    wfstr = "wf,nelec="+str(nelec)+",sym="+str(sym)+",spin="+str(spin)
    if states > 1:
        wfstr = wfstr + ";state," + str(states) 
    wfstr = wfstr +";"
    return wfstr
            
def BeH_gen(name,method="CI",occ="",frozen="", basis="", ranges = (1.342396,)):
    job = Molprojob(name, geom=gediat("Be","H"), basis =basis, occ = occ, frozen = frozen)
    job.setranges(ranges)
    if method == "CI":
        job.CI_BeH_ne()
    elif method == "MULTI":
        job.MULTI_BeH_ne()
    elif method == "FCI":
        job.FCI_BeH_ne()
    job.makejob()
    
def OH_gen(name,method="CI",occ="",frozen="", basis="", ranges = (0.96966,)):
    job = Molprojob(name, geom=gediat("Be","H"), basis =basis, occ = occ, frozen = frozen)
    job.setranges(ranges)
    if method == "CI":
        job.CI_OH_ne()
    elif method == "MULTI":
        job.MULTI_OH_ne()
    elif method == "FCI":
        job.FCI_OH_ne()
    job.makejob()
    