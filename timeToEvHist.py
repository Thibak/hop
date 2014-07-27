# -*- coding: utf-8 -*-
"""
Created on Fri Jun 06 20:13:36 2014

@author: user
"""
import scipy.stats as s
import numpy as np
import matplotlib.pyplot as plt

act = []

def weib(x,a,n):
    return (a / n) * (x / n)**(a - 1) * np.exp(-(x / n)**a)

#def func(x,a,n):
 #   return weib(x,1,)   
   
#def w(x):
#    a = 1*np.random.weibull(1)
#    if a < 1:
#        l = (a+np.random.normal(5))
#    else:
#        m = (a+.1*np.random.weibull(1)+np.random.normal(5))
#    return (l, m)

#d, f = [w(k) for k in range(10000) ]
#b = [np.random.weibull(1)+np.random.normal(1) for k in range(10000)]

def a(ks = 1, ls = 1, l1 = 1, l0 = 1, gap = 7, t = 0):
    
    w0 = np.random.weibull(1)*l0
    w1 = np.random.weibull(1)*l1
    ws = np.random.weibull(ks)*ls
   # if t == 0:
   #     print ('-----------------------')
   # print ('.'+str(w0)+'>'+str(ws)+'t='+str(t))
    if w0 > ws: # если время до деление меньше, то возвращаем его + задержку
        return gap + t + ws #  
    else: # если время до перехода в фазу сна меньше, 
    # то ставим в качестве задержки время до перехода и время в фазе сна
    # и вызываем рекурсию
        k = a(t = w0 + w1 + t, ks = ks, ls = ls, l1 = l1, l0 = l0, gap = gap)
        
        return k  



m = []
l = []


for k in range(1000):
#    g1 = 10
#    w1 = np.random.weibull(1)#weib(np.random.rand(1)[0], 1.,1.)#
 #   m.append(weib(np.random.rand(1)[0]*10, 1.,1.))
#    w2 = np.random.weibull(1)#weib(np.random.rand(1)[0], 1.,1.)#
#    ws = np.random.weibull(7)#weib(np.random.rand(1)[0], 1.,1)#
#    if w1 > ws:
#        l.append (g1+(ws))#
#    else:
#        l.append(g1+(w1+w2+ws))
    
    l.append([a(ks = 5, l1 = 1, t = 0, ls = 5, l0 = 5),k])


#[l[k]['v'] for k in range(len(l))] так может быть организован сбор 
#дополнительной инфы о данной клетке, например можно красить, и строить scatterplottы

h = np.histogram(l["v"],200) # мне нужна только гистограмма (из 2-х возвращаемых параметров)
#x = np.linspace(0, 2, 1000)
mx = h[1][np.argmax(h['v'])]
print(np.max(l[0]))
print(mx)
plt.hist(l[0],200)
#plt.hist(m,100)

#plt.plot(x, weib(x, 1, 1))
#plt.plot(x, weib(x, 1, 2))
#plt.plot(x, weib(x, 1, 3))


#plt.show()
        
          