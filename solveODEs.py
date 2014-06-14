# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 01:02:51 2014

@author: user
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
plt.ion()

P = 0       # birth rate
d = 0.0001  # natural death percent (per day)
B = 0.0095  # transmission percent  (per day)
G = 0.0001  # resurect percent (per day)
A = 0.0001  # destroy percent  (per day)

# solve the system dy/dt = f(y, t)
def f(y, t, l1,l0,ls,k):
        G1 = y[0]
        G0 = y[1]
        S = y[2]
        # the model equations (see Munz et al. 2009)
        f0 = (1-math.e**(-t/l0))*G0 - (2-math.e**(-t/l1) -math.e**(-(t/ls)**k))*G1
        f1 = (1-math.e**(-t/l1))*G1 - (1-math.e**(-t/l0))*G0
        f2 = (1-math.e**(-(t/ls)**k))*G1
        return [f0, f1, f2]

# initial conditions
S0 = 1               # initial population
Z0 = 0                  # initial zombie population
R0 = 0                  # initial death population
y0 = [S0, Z0, R0]       # initial condition vector
l0 = (1,1,1,7) #l1,l0,ls,k
t  = np.linspace(0, 10., 10000)   # time grid

# solve the DEs
soln = odeint(f, y0, t, l0)
G1 = soln[:, 0]
G0 = soln[:, 1]
S = soln[:, 2]

# plot results
plt.figure()
plt.plot(t, S, label='S')
plt.plot(t, G1, label='G1')
plt.plot(t, G0, label='G0')
plt.plot(t,np.gradient(S)*1000, label="S'")
plt.xlabel('time')
plt.ylabel('Distr')
plt.title('State')
plt.legend(loc=0)