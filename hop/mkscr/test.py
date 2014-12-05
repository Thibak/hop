# -*- coding: utf-8 -*-
"""
@author: russinow m a
ReMONA V.1.0
http://russinow.me/
"""

vscript =\
"""
#data.source = matrix
_len = []
for i in matrix:
    _len.append(len(i))
data.len = _len

_min = []
for i in matrix:
    _min.append(min(i))
data.min = _min

_max = []
for i in matrix:
    _max.append(max(i))
data.max = _max

_mean = []
for i in matrix:
    _mean.append(np.mean(i))
data.mean = _mean

_median = []
for i in matrix:
    _median.append(np.median(i))
data.median = _median
"""
sscript =\
"""
data.source = vector
data.mean = np.mean(vector)
"""
self.addVScript(vscript)
self.addSScript(sscript)