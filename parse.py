# -*- coding: utf-8 -*-
"""
file providing methods for parsing a single molpro out file
"""

import io
import re

def parse(outfilename):
    outfile = io.open(outfilename,'r')
    
    occ = re.compile(r"TODO")
    
    for textline in outfile:
        """
        !TODO
        """
    
    outfile.close()
    