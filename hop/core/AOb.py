# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 18:18:59 2014

@author: user

AOb.py -- Auxiliary Objects
"""
from operator import attrgetter
from collections import namedtuple
from types import ListType, StringType
from numpy import arange

from MOb import EventContainer
from hop.xmli import X

# пока впишу сюда



# Наследник встроенного типа list дополненный автоматической сортировкой по признаку TimeWhen. 
# дополнить проверкой типа бы...
class EStack(list):
    def push(self, element):
       super(EStack, self).append(element)
       super(EStack, self).sort(None, attrgetter('TimeWhen'), reverse=True) 

class EventServer():
    def __init__(self):
        self.eventsL = EStack()
        self.CurTime = 0
        self.deltaT = 0
    def GetEvent(self):
        try:
            e = self.eventsL.pop()
        except IndexError:   
            self.deltaT = 0
            return None
        self.deltaT = e.TimeWhen - self.CurTime
        self.CurTime = e.TimeWhen
        return e  
        
    # функция создающее событие
    def MakeEvent(self, Who, TimeTo):
        Who.SetEventTime(self.CurTime + TimeTo)
        self.eventsL.push(Who)    

#Event = namedtuple ('Event', 'fun res')
class Event:
    def __init__(self, function, result):
        self.fun = compile(function, '<string>', 'eval')
        self.res = compile(result,   '<string>', 'exec')

# какой-то непонятный рудимент, который я ВРОДЕбы переписал, но пока оставим, вдруг нет
#Compartment = namedtuple ('Compartment', 'int tran')

class FeedBackSever:
    """
    Сервер обратных связей. Основная необходимость в его создании, это преобразование или подмена значений.
    М.б. там распологаются функции выработки, наработки, накопления, дегродации белковых факторов
    
    Идея пересчитывать факторы только при обращении.
    
    Пока словарь словарей слотов по именам. 
    
    Пока обращение к частям модели через self.engine....
    
    """
    def __init__(self, name = 'default', di = {}):    
        self.CureDict = name
        self.ValDic = {name:di}
        
    def changeDict(self,d):
        self.CureDict = d
        
    def addDict(self, name, di = {}):
        """
        Можно сразу словарь запузыривать, со слотами
        """
        self.ValDic.append({name:di})
        
    def addSlot(self, name, d, st):
        self.ValDic[d][name] = st
        
    def val(self,name):
        return(eval(self.ValDic[self.CureDict][name]))

def functionalize(f):f()

class DataCollector:
    data = X()
    slot = X()
    def __init__(self):
        self.addSlot('final', '')
        self.addSlot('taktal', '')
    # функции первого уровня    
    def addDataPoint(self, p, typeOf = 's'):
        #if type(p) == StringType:
        if typeOf == 'v':
            self.data.__dict__[p] = list()
        else: self.data.__dict__[p] = float()
        
        #if type(p) == ListType:
        #    self.data.__dict__.update(dict.fromkeys(p))
    def addSlot(self, name, command):
        # в команде можем использовать self.data.имя ранее определенной точки входа данных 
        compiled_command = compile(command, '<string>', 'exec')
        self.slot.__dict__[name] = compiled_command
    # функции второго уровня
    def makePeriodicCollector(self, name, period, stop):#периодический
        for i in arange(0, stop, period):
            EventContainer(i,self.data.__dict__[name])
            
    def makeFinalCollector(self, s):#конечный
        self.addSlot('final', s)
        
    def makeTaktCollector(self, s):#потактный
        self.addSlot('taktal', s)        
        self.Engine.taktalSlot = self.slot.taktal
        
    #def makeEventCollector(self):#событийный
     #   pass
        # пожалуй пока не буду это вообще реализовывать
    def getVal(self,name):
        return(self.data.__dict__[name])
    def dict(self):
        return(self.data.__dict__)