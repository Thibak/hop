# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 22:02:45 2014

@author: user
"""

import cell

p = cell.programm()
p.load('simple_ex.rst')
e = cell.experiment(p)
e.plot('a2', 'a1','MeanProd')