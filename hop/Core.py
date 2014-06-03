# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 10:43:33 2014

@author: user
"""
from hop.clone import Clone
    
class Core:
    def __init__(self):
        self.CurClone = Clone()
        self.track = []
    def newClone(self,s):
        self.CurClone = Clone(s)
    def iterate(self,n,s=None):
        self.product = []       
        self.result = []
        for i in range(n):
            self.newClone(s)
            self.CurClone.do()
            self.product.append(self.CurClone.getProductValue()) #прицепляем объем продукта
            self.result.append(self.CurClone.isAlive()) #прицепляем исход запуска клона
            self.track.append(self.CurClone.track)
    def plotTracks(self):
        for i in self.track: 
            plt.pyplot.plot(i)
        plt.show()
    def GetMeanRes(self):
        return numpy.mean(self.result)
    def GetMedRes(self):
        return numpy.median(self.result)
    def GetMeanProd(self):
        return numpy.mean(self.product)
    def GetMedProd(self):
        return numpy.median(self.product)
