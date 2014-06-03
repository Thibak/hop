# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 20:44:20 2014

@author: Mikhail Rusinov

декоратор замеряющий время. 
Взято из: http://habrahabr.ru/post/141501/
def benchmark(func):
    тут должны стоять 3 двойные кавычки
    Декоратор, выводящий время, которое заняло
    выполнение декорируемой функции.
    тут должны стоять 3 двойные кавычки
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock() - t
        return res
    return wrapper
"""

import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.mlab import griddata



class TaskManager:
    """ 
    Hematopoiesis On Python
    
    Прредставляет собой основной объект 
        
        ВАЖНО!!! 
        По факту система выполнения действий является ассинхронной (т.е. мы выполняем события не в хронологическом порядке),
        в связи с чем мы не можем выполнять взаимодействия и обратные связи.
        Для избежания этой проблемы необходимо создать централизованый стек (с сортировкой после каждого пуша) 
        он должен принадлежать к обработчику, быть единым для всех клонов. 
        Т.е. операцию итерирования мы изымаем из ведения клона. Может быть клон вобще должен быть атрибутом клетки, и не более
        
        НО ЭТО ПОЗЖЕ...

    """
    def __init__(self, p = None):
        self.c = core()
        
        if p == None:
            self.p = programm()
        else:
            self.p = p
            
    def setDict(self,p):
        self.p = p
    def do(self):
        '''
        Запускаем расчет по выбраному словарю
    
        Аргументов не требуется
        '''
        print('Start calculating: /n')
        self.p.isCalc=True
        i = 0
        for s in self.p.element:
            i=i+1
            print("calculating " + str(i) + ' from ' + str(len(self.p.element)))
            print s
            self.c.iterate(self.p.itr,s)
            s['MeanRes'] = self.c.GetMeanRes()
            s['MedRes'] = self.c.GetMedRes()
            s['MeanProd'] = self.c.GetMeanProd()
            s['MedProd'] = self.c.GetMedProd()
        
            
            
    def plot(self, resName, param1, param2 = None, t = 'p'):
        '''
        Если 1 параметр передается, то рисуется 2D график, если два, то 3D       
        
        Для интерполяции неструктурированых данных (кои дефакто мы и имеем, хотя это не совсем так) 
         надо использовать функцию from matplotlib.mlab import griddata. 
         Например как тут: http://matplotlib.org/examples/pylab_examples/griddata_demo.html
         Размерность сетки интерполяции мб такой же как и у данных
        '''
        # сначала надо вытащить из словаря итерируемые значения
        #if resName = 'all'        
        
        if not self.p.isCalc:
            print('ATTENTION, object is unCalc')
        
        if param2 == None:
            y = [self.p.element[i][resName] for i in range(len(self.p.element))]
            x = [self.p.element[i][param1] for i in range(len(self.p.element))] 
            plt.pyplot.plot(x, y, 'yo-')
            plt.pyplot.show()
        else:
            z = [self.p.element[i][resName] for i in range(len(self.p.element))]
            x = [self.p.element[i][param1] for i in range(len(self.p.element))] 
            y = [self.p.element[i][param2] for i in range(len(self.p.element))] 
            fig = plt.pyplot.figure()
            axes = Axes3D(fig)
            
            axes.set_xlabel(param1)
            axes.set_ylabel(param2)
            axes.set_zlabel(resName)            
            
            axes.scatter3D(x,y,z, c=z)
            
          #  xi = numpy.linspace(0,1,100)
          #  yi = numpy.linspace(0,1,100)
            # grid the data.
          #  zi = griddata(x,y,z,xi,yi,interp='linear')

           # axes.plot_wireframe(X, Y, Z)
          #  axes.plot_surface(xi,yi,zi)
            
        #    plt.pyplot.colorbar()
            #axes.plot(x,y,z)
            #axes.plot_wireframe(x, y, z)
            fig.show()
