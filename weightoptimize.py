
import subprocess as sp
import inputgen as ig
import fileparse as fp
import datapoint as dp
from scipy import optimize
import numpy as np

molprocall = "/opt/MOLPRO/molpro/molpros_2012_1_Linux_x86_64_i8/bin/molpro --no-xml-output molpro.in"
outfilename = "weights.out"
occ = "8,2,2,0"
basis = "aug-cc-pVDZ"
frozen = "0,0,0,0"
nelecHF = "6"
spinHF = "0"
symHF = "1"

BeHstates=((5,1,1,7),(5,2,1,5),(5,3,1,5),(5,4,1,1),(5,2,3,1),(5,2,3,1))
BeHreference=((0.0,5.532,5.539,6.107,6.706,6.747,7.019),
           (2.5,6.313,6.712,7.266,7.352),
           (2.5,6.313,6.712,7.266,7.352),
           (6.747,),
           (5.77,),
           (5.77,))

BeHjob = ig.Molprojob(geom=ig.gediat("Be","H"), basis=basis, occ = occ, frozen = frozen)

class molopt:
    def __init__(self,states, reference, distance, job = BeHjob):
        self.states = states
        self.reference = reference
        self.distance = distance
        self.job = job
        self.i = 0

    def energies(self, weights):
        self.job.removemethods()
        self.job.addRHF(nelecHF,symHF,spinHF)
        self.job.addMULTI(self.states, weights)
        dists=list()
        dists.append(self.distance)
        self.job.writeinfile(dists, "molpro.in")
        sp.check_call(molprocall, shell = True)
        lines = fp.parse("molpro.out")
        energies = list()
        for state in self.states:
            templ = dp.chooselines(lines, symmetry=state[1], spin=dp.spinstr(state[2]))
            tempe = list()
            for line in templ:
                tempe.append(line.points[0].energy)
            tempe.sort()
            #TODO write to file
            energies.append(tempe)
        ground = min(min(energies,key=lambda x:min(x)))
        print(self.i)
        self.i+=1
        energies = list(map(lambda y:list(map(lambda x: x-ground, y)), energies))
        return energies
    
    def optfunc(self,optweights):
        weights = list()
        
        i=0
        for st in self.states:
            tempweights=list()
            for a in range(0,st[3],1):
                tempweights.append(optweights[i])
                i+=1
            weights.append(tempweights)
        #print(weights)
        levels = self.energies(weights)
        return leastsq(levels, self.reference)
        #return leastsq(weights, self.reference)
    
    
    def optimizeweights(self):
        initweights = list()
        bnds = tuple()
        for st in self.states:
            initweights += [1]*st[3]
            bnds += ((0.0,1.0),)*st[3]
        
        optres = optimize.minimize(self.optfunc, np.array(initweights), method="L-BFGS-B", bounds=bnds,
                                   options={'disp':True,'ftol':0.01,})
        optweights = optres.x
        outweights = list()
        
        i=0
        for st in self.states:
            tempweights = list()
            for a in range(0,st[3],1):
                tempweights.append(optweights[i])
                i+=1
            outweights.append(tempweights)
        return outweights
        

def leastsq(computed, exact):
    result = 0
    for en1 in zip(computed, exact):
        for en2 in zip(en1[0],en1[1]):
            result+= (en2[0]-en2[1])*(en2[0]-en2[1])
    return result
    


