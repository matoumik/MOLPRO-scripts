#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 08:25:57 2018

@author: mikulas
"""
from scipy.interpolate import interp1d
import scipy.optimize as op
import numpy as np
import numpy.linalg as la
import matplotlib as plt
hartree= 27.21138602
amuel= 1822.157434
bohr= 0.529177

def mu(amu1, amu2):
    return 1.0*amu1*amu2*amuel/(amu1+amu2)

def quantumgrid(potencial,mu,pointnum):
    
    #potencial = potencial.cut(mindist, maxdist)
    #spacing = (potencial.points[1].distance - potencial.points[0].distance)/bohr
    #potencial.extendtozero()


    #print(spacing)
    #TODO check equidistance
    
    spacing = (potencial.points[-1].distance - potencial.points[0].distance)/(pointnum-1)
    spacing = spacing/bohr
    
    x = np.linspace(potencial.points[0].distance,potencial.points[-1].distance, num = pointnum, endpoint = True)
    potencial = potencial.distsort()
    print( potencial.distances())
    
    interpol = interp1d(np.array(potencial.distances()),np.array(potencial.energies()),kind="cubic")

    hamiltonian = np.zeros((pointnum,pointnum))
    for i in range(0,pointnum,1):
        pot = interpol(x[i])
        hamiltonian[i][i] = pot/hartree + 1.0/mu/spacing/spacing
        hamiltonian[i-1][i] = -0.5/mu/spacing/spacing
        hamiltonian[i][i-1] = -0.5/(mu*spacing*spacing)
    
    E,psi = la.eigh(hamiltonian)
    
    return E*hartree, psi, x, interpol

def potencialgridprep(potencial, mindist="", maxdist=""):
    potencial.distsort()
    potencial = potencial.cut(mindist, maxdist)
    spacing = (potencial.points[1].distance - potencial.points[0].distance)
    #potencial.extendtozero()
    newpoint = potencial.points[0]
    newpoint.distance = 0
    #potencial.points.append(newpoint)
    potencial.distsort()
    return potencial, spacing


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
    
    
class Quantumstate:
    def __init__(self, Energy, Psi):
        self.energy =  Energy
        self.wf = Psi
    
    