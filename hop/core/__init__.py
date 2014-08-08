# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:29:06 2014

@author: russinow

Ядро расчетов. 
- 1. Сервер событий. Не объект, как ни странно.


"""
import numpy
#from collections import namedtuple

# пока просто тмпорт, а вобще-то надо только определенные функции
import MOb
from AOb import EventServer

# Главный объект

class Engine:
    """
    
    """
    def __init__(self):
        self.ES = EventServer()
        #Куммулятивные показатели
        self.cells = []
        
        self.MCC = []
        self.SCC = []
        self.conditions = {}
        self.defCon = None
        
        
    def addCondition(self, name, fun, dst):
        """
        Формат словаря --
        Имя состояния : что справа пока не понятно. 
        должна быть пара функционал -- функция результат перехода, т.е. события
        """
        self.conditions[name] = 
        
    def setDefCond(self, name):
        if name in self.conditions:
            self.defCon = name
        else:
            return 0

    def addMCC(self, cmprt):
        self.MCC.append(cmprt)
    def addSCC(self, cmprt):
        self.SCC.append(cmprt)
    def start(self):
        StartCell = cell() # создаем первую клетку
        помещаем клетку 
        Запускаем итератор времени.
        запускаем генератор события (получаем в ответ дельту времени)
        MakeEvent(StartCell,)
        
    def tik(self):
        """
        Сначала запускаем такт ивентсервера, откуда получаем длину шага времени
        записываем длину шага времени
        запускаем объекты принимающие шаг времени.   
        """
        #получить длну такта
        e = self.ES.GetEvent()
        if e = None:
            пораждаем конец расчета
        else:
            e.
        #использовать длину такта
        ES.deltaT
    def 
