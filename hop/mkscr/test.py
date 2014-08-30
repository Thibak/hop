# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 09:05:02 2014

@author: user
"""

vscript =\
"""
#data.source = matrix
_len = []
for i in matrix:
    _len.append(len(i))
data.len = _len
"""
sscript =\
"""
#data.source = vector
data.len = len(vector)
"""
self.addVScript(vscript)
self.addSScript(sscript)