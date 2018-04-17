#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 08:25:57 2018

@author: mikulas
"""

import scipy.optimize as op
import numpy as np
import numpy.linalg as la
import matplotlib as plt
hartree= 27.21138602
amuel= 1822.157434
bohr= 0.529177

def mu(amu1, amu2):
    return 1.0*amu1*amu2*amuel/(amu1+amu2)

def quantumgrid(potencial,mu,spacing):
    
    #potencial = potencial.cut(mindist, maxdist)
    #spacing = (potencial.points[1].distance - potencial.points[0].distance)/bohr
    #potencial.extendtozero()


    #print(spacing)
    #TODO check equidistance
    pointnum = len(potencial.points)
    hamiltonian = np.zeros((pointnum+1,pointnum+1))
    for i in range(1,pointnum+1,1):
        hamiltonian[i][i] = potencial.points[i-1].energy/hartree + 1.0/mu/spacing/spacing
        hamiltonian[i-1][i] = -0.5/mu/spacing/spacing
        hamiltonian[i][i-1] = -0.5/(mu*spacing*spacing)
    
    E,psi = la.eigh(hamiltonian)
    
    
    return E*hartree, psi

def potencialgridprep(potencial, mindist="", maxdist=""):
    potencial.distsort()
    potencial = potencial.cut(mindist, maxdist)
    spacing = (potencial.points[1].distance - potencial.points[0].distance)/bohr
    potencial.extendtozero()
    return potencial, spacing


def quantumLHO(potencial, neigh, states=1):
    minen, mindist = potencial.minimum()
    potencial = potencial.cut(mindist-neigh,mindist+neigh)
    pars = op.curve_fit(LHO(), potencial.distances(),
                        potencial.energies())
    return pars

def LHO():
    def f(x, k, e, d):
        return 0.5*k*(x-d)*(x-d) + e
    return f
    
    
class Quantumstate:
    def __init__(self, Energy, Psi):
        self.energy =  Energy
        self.wf = Psi
    
    