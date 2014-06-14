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

import time
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import griddata

import hop.model as model
import copy
import pickle #загружаем и сохраняем данные
import numpy as np 


print ('test')

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
        self.c = model.Core()
        
        if p == None:
            self.p = Plan()
        else:
            self.p = p
            
    def setDict(self,p):
        self.p = p
    def do(self):
        '''
        Запускаем расчет по выбраному словарю
    
        Аргументов не требуется
        '''
        print('Start calculating at ' + str(time.ctime()))
        t = time.clock()
        self.p.isCalc=True
        i = 0
        for s in self.p.element:
            i=i+1
            print("calculating " + str(i) + ' from ' + str(len(self.p.element)))
            #print s
            self.c.iterate(self.p.itr,s)
            s['MeanRes'] = self.c.GetMeanRes()
            s['MedRes'] = self.c.GetMedRes()
            s['MeanProd'] = self.c.GetMeanProd()
            s['MedProd'] = self.c.GetMedProd()
        print ('stop at ' + str(time.ctime()))
        print ('take ' + str(time.clock()-t))
            
            
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



class Plan:
    """
    Программа вычислений.
            iter -- количество итераций для каждой точки
            element -- вектор словарей -- задание на эксперимент
      Видимо структура объекта такая, до первого запуска операции push, 
      которая загоняет словарь в стек, мы можем добавлять атрибуты, 
      после этого мы блокируем объект. Кроме того надо написать модули сохранения и извлечения словарей.
      
      После обработки программы каждое задание становилтся экспериментом, 
      т.е. дополняется результатами. После этого мы должны мочь его так же сохранить
      
      self.dict.keys() -- значения ключей
      
      для присвоения нового атрибута используем      
      p.dict['имя']=значение
      НЕ ИСПОЛЬЗУЕМ, ИНАЧЕ БЛОКИРОВКА НЕ БУДЕТ РАБОТАТЬ    
      
      Задачи: Переделать загрузку дефаулта.
              Освоить итераторы
              все-таки заменить pickle на csv.
      
    Внимание вопрос: как сохранять объекты? 
        есть масса вариантов, 
        
  ----> во первых pickle как стандартная библиотека сохранения и извлечения объектов.
        пока реализуем этот самый простой вариант. Тем более, что 
            плюсы
                нативность
            минусы
                читается только питоном же
            Проблемы: 
                все отлично читается и сохраняется, за исключением того, что загрузка самого себя вещь странная.
                 весьма вероятно, что она не будет работать. 
                А сохранять только словарь из всего объекта не правильно, т.к. кроме словаря у меня имеется несколько объектов с важной информацией
                 
                ВОТ И ДУМАЙ...
                Решение: Оказывается Pickleзация объекта происходит через сохранение
                (внимание!) СЛОВАРЯ __dict__ в котором хранятся переменные объекта.
                Что мне собственно и нужно. Пишем метод для сохранения и извлечения __dict__
                Работать будет так.  Если нужно загрузить словарь, то создаем пустой объект
                и запускаем метод Load. ВАЖНО сделать предупреждение, что существующий 
                метод обнуляется
                
        во вторых CSV 
            плюсы
                читаемость SASом 
                читаемость и редактируемость руками
            минусы
                ненативность
        в третьих XML
            плюсы 
            минусы
        в четвертых JSON
            плюсы 
            минусы
      по теме:
          чтение и запись словаря в текстовый файл
          http://stackoverflow.com/questions/11026959/python-writing-dict-to-txt-file-and-reading-dict-from-txt-file
     
      
    """
    
    def __init__(self,itr = 100):
        self.element = []
        self.block = False
        self.itr = itr
        self.dict = {'a1':1,'a2':1,'l1':1,'l2':1}
        self.isCalc = False
        
    def chPrec(self, n):
        self.isCalc = False
        self.itr = n
        
        
    def push(self):
        self.block = True
        self.element.append(copy.deepcopy(self.dict))
        
    def addAttr(self, name, value):
        """ Добавление атрибута к словарю """
        if self.block:
            print ('attempt rejected')
        else:
            self.dict[name]=value
    def chAttr(self,name, value):
        if name in self.dict.keys():
            self.dict[name]=value
        else:
            print ('No such name')
    def keys(self): return self.dict.keys()
    def makeDict(self, a1=1,a2=1,l1=1,l2=1):
        return self.dict
        
    # высокоуровневые операции по формированию 
    def makeGrid(self, name1, start1, stop1, step1, name2, start2, stop2, step2):
        self.isCalc = False
        if name1 in self.dict.keys() and name2 in self.dict.keys():
            a = np.arange(start1, stop1, step1)
            b = np.arange(start2, stop2, step2)
            for j in a:
                for i in b:
                    self.chAttr(name1,j)
                    self.chAttr(name2,i)
                    self.push()
        else:
            print ('No such name. Grid creation aborted')
  
#        [[[self.addDict(i),k] for i in range(4)] for k in range(4)]  
    def makeVec(self, name, start, stop, step):
        self.isCalc = False
        if name in self.dict.keys():
            a = np.arange(start, stop, step)
            for i in a:
                self.chAttr(name,i)
                self.push()
        else:
            print ('No such name')
    # Подсистема сохранения и извлечения программы эксперимента
    def save(self,name):
        if self.isCalc:
            with open(name + '.rst', 'wb') as f:
                pickle.dump(self.__dict__, f,2)
        else:
            with open(name + '.dic', 'wb') as f:
                pickle.dump(self.__dict__, f,2)
    def load(self,name):
        with open(name, 'rb') as f:
            loaded_dict = pickle.load(f)
            f.close()          
            self.__dict__.update(loaded_dict) 
         