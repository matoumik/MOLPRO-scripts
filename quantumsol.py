#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 08:25:57 2018

@author: mikulas
"""
import datapoint as dp

from scipy.interpolate import UnivariateSpline
import scipy.optimize as op
import numpy as np
import numpy.linalg as la
import matplotlib as plt
hartree= 27.21138602
amuel= 1822.157434
bohr= 0.529177

eps = 0.0001

def mu(amu1, amu2):
    return 1.0*amu1*amu2*amuel/(amu1+amu2)

def quantumgrid(potencial,mu,spacing):
       
    spacing = spacing/bohr
    pointnum = len(potencial.points)
    potencial = potencial.distsort()
    
    hamiltonian = np.zeros((pointnum,pointnum))  
    for i in range(1,pointnum,1):   
        hamiltonian[i][i] = potencial.points[i].energy/hartree + 1.0/mu/spacing/spacing
        hamiltonian[i][i-1] = -0.5/mu/spacing/spacing
        hamiltonian[i-1][i] = -0.5/(mu*spacing*spacing)
    
    E,psi = la.eigh(hamiltonian)
    
    return E*hartree, psi

def potencialgridprep(potencial, pointnum, mindist="", maxdist=""):
    potencial.distsort()
    potencial = potencial.cut(mindist, maxdist)    
    #potencial.extendtozero()
    potencial.distsort()
    spacing = (potencial.points[-1].distance-potencial.points[0].distance)/(pointnum-1)


    x = np.linspace(potencial.points[0].distance,potencial.points[-1].distance, num = pointnum, endpoint = True)
    interpol = UnivariateSpline(np.array(potencial.distances()),np.array(potencial.energies()),k=3, s=0, ext = 'const')

    newpotencial = potencial.removepoints()
    for dist in x:
        newpotencial.addpoint(dist,interpol(dist))


    #print(newpotencial.distances())
    return newpotencial, spacing


def quantumLHO(potencial, neigh, states=1):
    minen, mindist = potencial.minimum()
    potencial = potencial.cut(mindist-neigh,mindist+neigh)
    pars = op.curve_fit(LHO(), potencial.distances(),
                        potencial.energies())
    return pars

def LHO():
    def f(x, k, e, d):
        return (0.5*k*(x-d)*(x-d)/bohr/bohr + e)*hartree
    return f

def CBEexpF(E_Dz, E_Tz, E_Qz):
    E = (E_Dz*E_Qz-E_Tz*E_Tz)/(E_Dz-2*E_Tz+E_Qz)
    return E

def CBEexp(Line_Dz, Line_Tz, Line_Qz):
    extrapol = dp.Line(  list(),  
            moleculename=Line_Qz.moleculename,
                            basis="CBE (exponential)", 
                            method =Line_Qz.method,
                            occ=Line_Qz.occ,
                            numberofelectrons=Line_Qz.numberofelectrons,
                            symmetry=Line_Qz.symmetry,spin=Line_Qz.spin,number=Line_Qz.number)
    for pointD in Line_Dz.points:
        for pointT in Line_Tz.points:
            for pointQ in Line_Qz.points:
                if (abs(pointD.distance - pointT.distance) < eps) and (abs(pointD.distance - pointQ.distance) < eps):
                    extrapol.points.append(dp.Point(pointD.distance, 
                            CBEexpF(pointD.energy, pointT.energy, pointQ.energy),
                            moleculename=extrapol.moleculename,
                            basis="CBE (exponential)", 
                            method =extrapol.method,
                            occ=extrapol.occ,
                            numberofelectrons=extrapol.numberofelectrons,
                            symmetry=extrapol.symmetry,spin=extrapol.spin,number=extrapol.number))
    return extrapol
    
class Quantumstate:
    def __init__(self, Energy, Psi):
        self.energy =  Energy
        self.wf = Psi
    
    