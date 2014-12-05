# -*- coding: utf-8 -*-
"""
@author: russinow m a
ReMONA V.1.0
http://russinow.me/

MOb.py -- Modell Objects

"""

import numpy as np
import random # интерфейс для скриптинга
from types import CodeType

class AbstractCompartment():
    """
    Абстрактный компартмент, это количество объектов в данном состоянии
    методы доступа к изменению количества
    """
    n = 0  
    def __repr__(self):
        return str(self.n)
    def addObject(self):
        self.n = self.n + 1
    def remObject(self):
        self.n = self.n - 1        
    
class SOC(AbstractCompartment):
    """
    Singular Objects Compartment
    """
    vec = []
#    def getQty(self):
#        return len(self)
#    def addObject(self, Object):
#        super(StemCompartment, self).append(Object)
#    def removeObject(self, Object):
       # try:
#            super(StemCompartment, self).remove(Object)
       # except:
       #    pass
        
class MOC(AbstractCompartment):
    """
    Mass Object Compartment
    1. Общая характеристика компартмента
    2. Команды для построения модели (модификаторы конфигурации)
    """
    def __init__(self, internal, transition, to):
        self.internal = compile(internal, '<string>', 'eval')
        self.transition = compile(transition, '<string>', 'eval') 
        self.to = to
    
    def step(self, dt):
        """
        """
        N = self.n # локальное значение
        self.n = eval(self.internal) # расчитываем внутреннее количество
        return eval(self.transition) # возвращаем dt
    def add(self, intg):
        self.n += intg
    
    
#--------------------------------------------------
   
    
class EventContainer:
    """
    Абстрактный контейнер события. 
    При создании задаем время и строку для выполнения через время.
    """
    def __init__(self, Time, st = None):
        if type(st) == type(None):
            st = ''
        elif type(st) == str:
            self.st = compile(st, '<string>', 'eval')
        elif type(st) == CodeType:
            self.st = st
        else: 
            raise TypeError
        
        self.SetEventTime(Time)
        self.Engine.ES.MakeEvent(self, Time)  

    def SetEventTime(self, Time):
        """
        Инфраструктурная функция, задает время.
        """
        self.TimeWhen = Time
        
    def go(self):
        """
        Запуск выполнения запланированной строки события
        """
        exec(self.st)
        return 0
    
    
class Object(EventContainer):
    """ Класс Объект.
        Каждый объект существует внутри некоторого компартмента. 
        Компартмент-хендлер -- пустой класс-идентификатор поведения для Объектов
        По большому счету, нам не важно какие Объекты содержатся в компартменте, 
        Т.к. от компартмента нам нужно только знание содержимого (количества). 
        Данные о состоянии Объекта в текущий момент.        
        - SetEventTime() -- кладем время до события
        - EventTime() -- время до события
          
          """
    def __init__(self, cond = None):
        if cond == None:
            self.CureCond = self.defCon
        else:
            self.CureCond = cond
        self.SOC[self.CureCond].addObject()
        self.GenEv()
        
    def GenEv(self):
        """
        по справочнику определяется множество формул для данного состояния
        self.SOC[self.CureCond] -- возвращает какой-то объект, из которого мы получаем множество формул
        """
        # Достаём формулы
        # выкидываем время до события по формулам  
             
        times = []
        for i in range(len(self.SOC[self.CureCond].vec)):
            times.append(eval(self.SOC[self.CureCond].vec[i].fun))
        # определяем наименьшую
        # определяем соответствие событию
        # Ставим идентификатор события
        self.ev = np.argmin(times)
        # записываем таймер, записываем время ЧЕРЕЗ КОТОРОЕ ПРОИЗОЙДЕТ СОБЫТИЕ
        self.Engine.ES.MakeEvent(self, eval(self.SOC[self.CureCond].vec[self.ev].fun))        

    # Инфраструктура событий
    # События м.б. продуцирующими и дегенеративными
    # продуцирующие события запускают в конце метод-генератор нового события
    # дегенративные этого не делают, в любом случае удаляются из текущего компартмента и, возможно что-то еще

    def sleep(self):
        """
        Минимальное событие, просто перезапускает генератор события (т.е. оттягивает время)
        """
        self.GenEv()
        
    def divide(self):
        """
        Деление Объекта наследует компартмент (происходит в том же компартменте).
        """
        Object(self.CureCond)
        self.GenEv()
    
    def assymDivide(self, cond = None):
        """
        Ассиметричное деление
        """
        Object(cond)
        self.GenEv()
    
    def reconfigurate(self, cmprt):
        """
        Смена конфигурации, в парадигме РМС, или изменение состояния объекта.
        Происходит через удаление текущего Объекта и создание нового в новом компартменте.
        """ 
        self.SOC[self.CureCond].remObject()
        self.CureCond = cmprt
        self.SOC[self.CureCond].addObject()
        self.GenEv()


    def destroy(self):
        """
        Объект самоудаляется из всех списков, и вычитает значение из компартмента. 
        """        
        self.SOC[self.CureCond].remObject()
    
    def toMOC(self, name):
        """
        Добавление в МОС
        """
        self.MOC[name].addObject()     
        
    def test(self,s):
        """
        Тестовая функция, выводит сообщение s
        """
        print('get -- > '+s)
        
#----------------------------------------------------------      

    def go(self):
        """
        Выполнить действие.
        Достаем строку из справочника по текущему состоянию и записанному событию
        Возвращаем дельту времени для запуска итератора интегральных компартментов
        """
        exec(self.SOC[self.CureCond].vec[self.ev].res)
        return self.Engine.ES.deltaT

class StopEvent(EventContainer):
    """
    Метод, переопределяющий функцию go таким образом, что она возвращает ошибку, останавливающую Ивент-сервер и расчет данного раунда
    """
    def go(self):
        raise AttributeError
    # Запасной метод, реализуется через простой вызов смены словаря
    #def TurnOnFeedback(self,name):
    #    self.Engine.FB.changeDict(name)