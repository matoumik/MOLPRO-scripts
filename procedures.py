#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 10:07:31 2018

@author: mikulas
"""

import quantumsol as qs
import inputgen as ig
import datapoint as dp

def annepars(anion, neutral, mu):
    an_pot, an_spacing = qs.potencialgridprep(anion, 400)
    ne_pot, ne_spacing = qs.potencialgridprep(neutral, 400)  
    
    ne_eqen, ne_eqdist = ne_pot.minimum()
    an_eqen, an_eqdist = an_pot.minimum()
    
    ne_viben, ne_vibwf = qs.quantumgrid(ne_pot, mu, ne_spacing)
    an_viben, an_vibwf = qs.quantumgrid(an_pot, mu, an_spacing)
    
    ne_asen = ne_pot.asymptotice()
    an_asen = an_pot.asymptotice()
    
    elaff_vib = ne_viben[0] - an_viben[0]
    elaff_min = ne_eqen - an_eqen
    
    elaff_as = ne_asen - an_asen
    
    return elaff_vib, elaff_min, elaff_as

def linepars(line, mu):

    pot, spacing= qs.potencialgridprep(line, 400)

    eqen, eqdist = pot.minimum()

    viben, vibwf = qs.quantumgrid(pot, mu, spacing)
    
    asen = pot.asymptotice()
    
    disen_vib = asen - viben[0]
    disen_min = asen - eqen
    
    return disen_vib, disen_min, viben
    

def comptablehead(file, var=1, caption = "TODO", label = "TODO"):
    tablehead1 = \
"""
\\begin{tabular}{rrrrr}
\\toprule
Method & $E_a(BeH)[\mathrm{eV}]$ & $E_a(H)[\mathrm{eV}]$ & $D_a(BeH)[\mathrm{eV}]$ & $D_a(BeH^-)[\mathrm{eV}]$ \\\\ \\midrule
    """
    tablehead2 = \
"""
\\begin{tabular}{rrrrr}
\\toprule
Method & $E_a(OH)[\mathrm{eV}]$ & $E_a(O)[\mathrm{eV}]$ & $D_a(OH)[\mathrm{eV}]$ & $D_a(OH^-)[\mathrm{eV}]$ \\\\ \\midrule
"""
    if var == "BeH1":
        file.write(tablehead1)
    elif var == "OH1":
        file.write(tablehead2)
    
def tablefoot(file):
    tablefoot = \
    """\\bottomrule
\\end{tabular}
"""
    file.write(tablefoot)

def comptable2line(file,anion, neutral,var="BeH1"):
    print(var)
    if var == "BeH1":
        mu = qs.mu(1,9)
    elif var == "OH1":
        mu = qs.mu(1,16)
    
    deli = " & "
    afv, afm, afa = annepars(anion, neutral, mu)
    an_dv, an_dm, an_vib = linepars(anion, mu)
    ne_dv, ne_dm, ne_vib = linepars(neutral, mu)
    if var == "BeH1":
        neutral.setoutputtemplate("$M $O /$B")
        line = str(neutral)
        for thing in ( afv, afa, ne_dv, an_dv):
            line = line +deli + "{:.3f}".format(thing) 
        line = line + "\\\\\n"
        file.write(line)
    if var == "OH1":
        neutral.setoutputtemplate("$M $O /$B")
        line = str(neutral)
        for thing in ( afv, afa, ne_dv, an_dv):
            line = line +deli + "{:.3f}".format(thing) 
        line = line + "\\\\\n"
        file.write(line)
        
def comptable2lineexp(file,var):
    if var == "BeH1":
        expline='Experimental:  & $0.70\\pm0.1$ & $0.754195$\
        & $2.18\\pm0.02$ & $2.07$ \\\\ \\midrule\n'
    elif var == "OH1":
        expline='Experimental:  & $1.82767$ & $1.461$ &\
        $4.3914$ & $5.120435$ \\\\ \\midrule\n'
    file.write(expline)
        
        
def annetable(filename, anionlines, neutrallines, var, caption = "TODO", label = "TODO", experimental = True):
    file = open(filename, "w")
    print(len(anionlines))
    print(len(neutrallines))
    comptablehead(file, var, caption, label)
    if experimental:
        comptable2lineexp(file, var)
    for i in range(0,len(neutrallines), 1):
        comptable2line(file, anionlines[i], neutrallines[i], var)
    tablefoot(file)
    file.close()
    
def vibrtablehead(file, var=1, caption = "TODO", label = "TODO", experimental = True):
    tablehead1 = \
"""
\\begin{tabular}{lllll}
\\toprule
Method & $v_0 [\mathrm{eV}]$ & $v_1 [\mathrm{eV}]$ & $v_2 [\mathrm{eV}]$ & $v_3[\mathrm{eV}]$ \\\\ \\midrule
    """
    tablehead2 = \
    """
\\begin{tabular}{lllll}
\\toprule
Method & $v_0 [\mathrm{eV}]$ & $v_1 [\mathrm{eV}]$ & $v_2 [\mathrm{eV}]$ & $v_3[\mathrm{eV}]$ \\\\ \\midrule
"""
    if var == "BeH1":
        file.write(tablehead1)
    elif var == "BeH2":
        file.write(tablehead1)
    elif var == "OH1":
        file.write(tablehead2)
    elif var == "OH2":
        file.write(tablehead2)
    elif var == "OHan1":
        file.write(tablehead2)
    elif var == "OHan2":
        file.write(tablehead2)
        

def vibrtableline(file,line,var="BeH1",mindist = "", maxdist = ""):
    print(var)
    if var == "BeH1":
        mu = qs.mu(1,9.012)
    elif var == "BeH2":
        mu = qs.mu(1,9.012)
    elif var == "OH1":
        mu = qs.mu(1,16)
    elif var == "OH2":
        mu = qs.mu(1,16)
    elif var == "OHan1":
        mu = qs.mu(1,16)
    elif var == "OHan2":
        mu = qs.mu(1,16)
    
    potencial, spacing = qs.potencialgridprep(line, 1000, mindist, maxdist)
    Emin, whatever = potencial.minimum()
    #potencial.setzero(Emin)
    E, psi = qs.quantumgrid(potencial, mu, spacing)
    print(E[0])
    print(E[1])
    deli = " & "
    
    if var == "BeH1":
        line.setoutputtemplate("$M $O/$B")
        linestr = str(line)
        for i in range(0,4,1):
            Etemp =E[i]-Emin
            linestr = linestr +deli + "{:.4f}".format(Etemp) 
        linestr = linestr + "\\\\\n"
        file.write(linestr)
        
    if var == "BeH2":
        line.setoutputtemplate("$M $O/$B")
        linestr = str(line)
        for i in range(0,4,1):
            Etemp =E[i]-E[0]
            linestr = linestr +deli + "{:.4f}".format(Etemp) 
        linestr = linestr + "\\\\\n"
        file.write(linestr)
    
    
    if var == "OH1":
        line.setoutputtemplate("$M $O/$B")
        linestr = str(line)
        for i in range(0,4,1):
            linestr = linestr +deli + "{:.3f}".format(E[i]-Emin) 
        linestr = linestr + "\\\\\n"
        file.write(linestr)        
    if var == "OH2":
        line.setoutputtemplate("$M $O/$B")
        linestr = str(line)
        for i in range(0,4,1):
            linestr = linestr +deli + "{:.3f}".format(E[i]-E[0]) 
        linestr = linestr + "\\\\\n"
        file.write(linestr)    
    
    
def vibrtable(filename, lines, var, caption = "TODO", label = "TODO", experimental = True, mindist = "", maxdist = ""):
    file = open(filename, 'w')
    vibrtablehead(file, var, caption, label)
    if var=="BeH2" and experimental:
        file.write("Exper. & 0.000 & 0.246 & 0.483 & 0.710 \\\\\n\\midrule\n" )
    if var=="OH2" and experimental:
        file.write("Exper. & 0.000 & 0.462 &  &  \\\\\n\\midrule\n" )
    for line in lines:
        vibrtableline(file, line, var, mindist, maxdist)
    tablefoot(file)
    file.close()

def eqtable(filename, levels, var):
    file = open(filename, 'w')
    file.write("\\begin{tabular}{r"+ 'r'*len(levels)+"}\n\\toprule\n")
    if var =="BeH1":
        terms = (1,2,3,4,5,6,7,8);
    elif var =="OH1":
        terms = (1,2,3,4,5,6,7,8,9);
    i = 0
    
    newlevels = list()
    for level in levels:
        cilev = dp.chooselines(level, method = "CI")
        if len(cilev) > 0:
            level = cilev
        #newlevels.append(dp.chooselines(sorted(level, key = lambda x: x.points[0].energy))) 
        newlevels.append(level)
    levels = newlevels
    for linel in levels:
        linel.setoutputtemplate("$M $O")
        file.write(" & "+str(linel[0]))
    file.write("\\\\\n ")
    for linel in levels:    
        linel.setoutputtemplate("$B")
        file.write(" & "+str(linel[0]))
        
        
    file.write("\\\\\n\\midrule\n")            
    
    
    for term in terms:
        tableline = str(term)
        
        
        
        for linel in levels:
            tableline += "&" + "{:.3f}".format(linel[i].points[0].energy)
        tableline+="\\\\\n"
        file.write(tableline)
        i+=1
        
    tablefoot(file)
    file.close()
    
        
    
    
    
