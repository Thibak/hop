# -*- coding: utf-8 -*-
"""
Created on Sun Jun 01 18:39:59 2014

@author: user
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

a=linspace(0,1,10)
fig = plt.figure()
axes = Axes3D(fig)
#axes.scatter3D(a,a,a)
axes.plot(a,a,a)
#axes.plot_wireframe(x, y, z)
plt.show()