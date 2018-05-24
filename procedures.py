#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 10:07:31 2018

@author: mikulas
"""

import quantumsol as qs

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
    """\\begin{table}[]
\\centering
\\caption{""" +\
        caption \
      +   """}
\\label{""" +\
        label \
      +   """}
\\begin{tabular}{rrrrr}
\\toprule
Method & $E_a(BeH)[" eV"]$ & $E_a(H)[" eV"]$ & $D_a(BeH)[" eV"]$ & $D_a(BeH^-)[" eV"]$ \\\\ \\midrule
    """
    tablehead2 = \
    """\\begin{table}[]
\\centering
\\caption{""" +\
        caption \
      +   """}
\\label{""" +\
        label \
      +   """}
\\begin{tabular}{rrrrr}
\\toprule
Method & $E_a(OH)[" eV"]$ & $E_a(O)[" eV"]$ & $D_a(OH)[" eV"]$ & $D_a(OH^-)[" eV"]$ \\\\ \\midrule
"""
    if var == "BeH1":
        file.write(tablehead1)
    elif var == "OH1":
        file.write(tablehead2)
    
def tablefoot(file):
    tablefoot = \
    """\\bottomrule
\\end{tabular}
\end{table}
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
    """\\begin{table}[]
\\centering
\\caption{""" +\
        caption \
      +   """}
\\label{""" +\
        label \
      +   """}
\\begin{tabular}{rrrrr}
\\toprule
Method & $v_0 [" eV"]$ & $v_1 [" eV"]$ & $v_2 [" eV"]$ & $v_3[" eV"]$ \\\\ \\midrule
    """
    tablehead2 = \
    """\\begin{table}[]
\\centering
\\caption{""" +\
        caption \
      +   """}
\\label{""" +\
        label \
      +   """}
\\begin{tabular}{rrrrr}
\\toprule
Method & $v_0 [" eV"]$ & $v_1 [" eV"]$ & $v_2 [" eV"]$ & $v_3[" eV"]$ \\\\ \\midrule
"""
    if var == "BeH1":
        file.write(tablehead1)
    elif var == "OH1":
        file.write(tablehead2)
        

def vibrtableline(file,line,var="BeH1"):
    print(var)
    if var == "BeH1":
        mu = qs.mu(1,9)
    elif var == "OH1":
        mu = qs.mu(1,16)
    
    potencial, spacing = qs.potencialgridprep(line, 400)
    E, psi = qs.quantumgrid(potencial, mu, spacing)
    Emin, whatever = potencial.minimum()

    deli = " & "
    
    if var == "BeH1":
        line.setoutputtemplate("$M $O /$B")
        linestr = str(line)
        for i in range(0,4,1):
            Etemp =E[i]-Emin
            linestr = linestr +deli + "{:.4f}".format(Etemp) 
        linestr = linestr + "\\\\\n"
        file.write(linestr)
    if var == "OH1":
        line.setoutputtemplate("$M $O /$B")
        linestr = str(line)
        for i in range(0,4,1):
            linestr = linestr +deli + "{:.3f}".format(E[i]-Emin) 
        linestr = linestr + "\\\\\n"
        file.write(linestr)        
    
    
def vibrtable(filename, lines, var, caption = "TODO", label = "TODO", experimental = True):
    file = open(filename, 'w')
    vibrtablehead(file, var, caption, label)
    for line in lines:
        vibrtableline(file, line, var)
    tablefoot(file)
    file.close()
    