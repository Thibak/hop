# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:32:42 2014

@author: russinow

Синтаксис фабрики:
from lxml.builder import ElementMaker
E = ElementMaker()
d = E.e
ff = E('ddd')

* Для XML-фабрики есть волшебная функция, выполняющая роль сериализатора списка. Т.к. фабрика понимает на входе как строку так и эелемент типа _element, то функция может спокойно использовать в построении фабрики.
Фишка в том, что тут передается элементы XMLя, у которого есть атрибут .append
def a(l, f):
  for i in range(len(l)):
   f.append(l[i])
  return f
ggg = d(a([d('1'),d('2')], d()))

Для пуша объектов в память используем str(), для извлечения используем eval()


Извлечение элементов

from lxml import etree
etree.tostring(ff)

"""

import lxml #.etree.ElementTree as ET
from lxml.builder import ElementMaker
from lxml import etree #<-- вспомогательная функция для сериализации


def glue(l, f):
    """
    Склеить элементы из l функцией f
    Причем, вектор элементов может содержать любые элементы
    """
    for i in range(len(l)):
        f.append(l[i])
    return f

def load(name):
    tree = ET.parse(load) #(file_in)
    root = tree.getroot()
    return root

def save():
    pass

class Experiment():
    def __init__(self, filename=None):
        if filename == None:
            self.root = etree.XML('<root></root>')
            self.Factory = ElementMaker()
            self.tree = etree.ElementTree(self.root)
            self.tasks = self.Factory.tasks()
            self.root.append(self.tasks)
            self.meta = self.Factory.meta()
            self.root.append(self.meta)
        else:
            pass # пока пасс, а на самом деле загрузка парсера файла
    def setIter(self,iteration):
        self.meta.set(iteration = str(iteration))
        
    def MakeMatrix(self, Xvar, XX, Yvar, YY):
        # матрица. Может передавать не матрицы, а диапазоны и шаги?
        # что еще надо в матрице?
        matrix = self.Factory.matrix()  
        self.meta.append(matrix)
        matrix.append(self.Factory.x(XX.tolist(), name = str(Xvar)))
        matrix.append(self.Factory.y(YY.tolist(), name = str(Yvar)))
        # тут будет цикл, с makeTask        
        
    def makeTask(self, i, j, x, y):
        task = self.Factory.task(i = str(i), j = str(j), x = str(x), y = str(y))
        self.tasks.append(task)
        #При свертывании выполняем двойной цикл в котором забиваем item.i = i, item.j = j, item.x = x[i][j], item.y = y[i][j], где x и y -- имена итерируемых переменных
        
        
  
    