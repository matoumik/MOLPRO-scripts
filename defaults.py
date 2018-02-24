#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 11:33:16 2018

@author: mikulas
"""

import inputgen as ig

range1 = ig.makedistrange(1.0, 0.6, 0.1) + ig.makedistrange(1.1, 2.5, 0.1) +\
         ig.makedistrange(2.6, 4.0, 0.2) + ig.makedistrange(5.0,10.0,1.0)
         
