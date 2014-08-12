# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 18:18:59 2014

@author: user

AOb.py -- Auxiliary Objects
"""
from operator import attrgetter
from collections import namedtuple


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

Event = namedtuple ('Event', 'fun res')

Compartment = namedtuple ('Compartment', 'int tran')

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
        
