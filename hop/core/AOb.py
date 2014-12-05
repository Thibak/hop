# -*- coding: utf-8 -*-
"""
@author: russinow m a
ReMONA V.1.0
http://russinow.me/

AOb.py -- Auxiliary Objects
"""
from operator import attrgetter

from numpy import arange

from MOb import EventContainer
from hop.DataDriver import Y

# Наследник встроенного типа list дополненный автоматической сортировкой по признаку TimeWhen. 

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

class Event:
    def __init__(self, function, result):
        self.fun = compile(function, '<string>', 'eval')
        self.res = compile(result,   '<string>', 'exec')


class FeedBackSever:
    """
    Сервер обратных связей. Основная необходимость в его создании, это преобразование или подмена значений.
    Перерасчет факторов только при обращении.
    Словарь словарей слотов по именам. 
    Обращение к частям модели через self.engine.
    
    """
    def __init__(self, name = 'default', di = {}):    
        self.CureDict = name
        self.ValDic = {name:di}
        
    def changeDict(self,d):
        self.CureDict = d
        
    def addDict(self, name, di = {}):
        """
        """
        cultivate_dict = {}
        for item in di:
            if isinstance(di[item], (int, float)): 
                cultivate_dict[item] = di[item]
            elif isinstance(di[item], str):
                cultivate_dict[item] = compile(di[item],'<string>','eval')
            else:
                raise Exception('Словарь сервера событий допускает действительные числа или строковые скрипты')
        self.ValDic.append({name:cultivate_dict})
        
    def addSlot(self, name, d, st):
        if isinstance(st, (int, float)): 
            self.ValDic[d][name] = st
        elif isinstance(st, str):
            self.ValDic[d][name] = compile(st,'<string>','eval')
        else:
            raise Exception('Словарь сервера событий допускает действительные числа или строковые скрипты')
        
    def val(self,name):
        item = self.ValDic[self.CureDict][name]
        if isinstance(item, (int, float)): 
            return item
        elif isinstance(item, str):
            return(eval(item))

def functionalize(f):f()

class DataCollector:
    data = Y()
    slot = Y()
    def __init__(self):
        self.addSlot('final', '')
        self.addSlot('taktal', '')
    # функции первого уровня    
    def addDataPoint(self, p, typeOf = 's'):

        if typeOf == 'v':
            self.data.__dict__[p] = list()
        else: self.data.__dict__[p] = float()

    def addSlot(self, name, command):
        # в команде можем использовать self.data.имя ранее определенной точки входа данных 
        compiled_command = compile(command, '<string>', 'exec')
        self.slot.__dict__[name] = compiled_command
    # функции второго уровня
    def makePeriodicCollector(self, name, period, stop):#периодический
        for i in arange(0, stop, period):
            EventContainer(i,self.slot.__dict__[name])
            
    def makeFinalCollector(self, s):#конечный
        self.addSlot('final', s)
        
    def makeTaktCollector(self, s):#потактный
        self.addSlot('taktal', s)        
        self.Engine.taktalSlot = self.slot.taktal
        
    def getVal(self,name):
        return(self.data.__dict__[name])
    def dict(self):
        return(self.data.__dict__)