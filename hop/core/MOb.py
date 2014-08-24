# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 16:54:50 2014

@author: user

MOb.py от Modell Objects

"""

import numpy
import random
from types import CodeType

class AbstractCompartment():
    """
    Содержит ли компартмент собственную историю??
    Добавить можно всегда, потому пока нет.
    Абстрактный компартмент, это количество клеток
    методы доступа к изменению количества
    """
    n = 0  
    def __repr__(self):
        return str(self.n)
    def addCell(self):
        self.n = self.n + 1
    def remCell(self):
        self.n = self.n - 1        
    
class SCC(AbstractCompartment): #, list):
    """
    stem cells compartment

    Отличие от абстракта     
    Пока никакого. А если и не будет? 
    Может наследовать от нее MCC, а сюда перенести весь функционал из абстракта
    """
    vec = []
#    def getQty(self):
#        return len(self)
#    def addCell(self, cell):
#        super(StemCompartment, self).append(cell)
#    def removeCell(self, cell):
       # try:
#            super(StemCompartment, self).remove(cell)
       # except:
       #    pass
        
class MCC(AbstractCompartment):
    """
    mature celss compartment
    1. Прямо тут будем хранить не только информацию о количестве но и
    2. функции изменения и переходов
    """
    # по большому счету совершенно не обязательно тут это определять, но пусть будет для наглядности
    def __init__(self, internal, transition, to):
        self.internal = compile(internal, '<string>', 'eval')
        self.transition = compile(transition, '<string>', 'eval') 
        self.to = to
    
    def step(self, dt):
        """
        internal -- должно быть выражением с использованием N как предыдущего значения и dt как дельты времени
        """
        N = self.n #<--- сильно не факт, что будет работать! Эксперименты показывают, что будет, т.к. используется тот неймспейс, в котором запущено.
        self.n = eval(self.internal) # умно запускаю внутренний пересчет при вызове. Но! Умно ли он происходит до расчета перехода? Думаю, что нет. Надо создавать буферное значение. А оказывается я все уже сделал!
        return eval(self.transition)
    def add(self, intg):
        self.n += intg
    
    
#--------------------------------------------------
# клетки    
    
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
        Инфраструктурная функция. Запилить ее.
        """
        self.TimeWhen = Time
    def go(self):
        exec(self.st)
        return 0
    
    
class cell(EventContainer):
    """ Класс клетка.
        Каждая клетка существует внутри некоторого компартмента. 
        Важно следить за тем, что бы небыло утечки клеток.
        Компартмент-хендлер -- пустой класс-идентификатор поведения для клеток
        По большому счету, нам не важно какие клетки содержатся в компартменте. 
        Т.к. от компартмента нам нужно только знание содержимого. 
        Хотя мы будем делать самостоятельных наследников
        Храним данные о состоянии клетки в текущий момент.        
        - SetEventTime() -- кладем время до события
        - EventTime() -- время до события
        Умеет
          выдавать решение на следующую итерацию:
              делится,
              умирать (и вот вопрос, что с ней происходит, когда она умирает)
тут немного о Вейбуле и рисовании http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy          
          
          """
    def __init__(self, cond = None):
        if cond == None:
            self.CureCond = self.defCon
        else:
            self.CureCond = cond
        self.SCC[self.CureCond].addCell()
        self.GenEv()
        
    def GenEv(self):
        """
        по справочнику определяем множество формул для данного состояния
        self.SCC[self.CureCond] -- возвращает какой-то объект, из которого мы получаем множество формул
        """
        #разыгрывем время до ближайших событий
#        act.append(self.s['l1']*numpy.random.weibull(self.s['a1'])) 
#        act.append(self.s['l2']*numpy.random.weibull(self.s['a2']))
#        i = numpy.argmin(act) #определяем какое из событий таки ближайшее

        # Достаём формулы
        # выкидываем время до события по формулам        
        times = []
        for i in range(len(self.SCC[self.CureCond].vec)):
            times.append(eval(self.SCC[self.CureCond].vec[i].fun))
        # определяем наименьшую
        # определяем соответствие событию
        # Ставим идентификатор события
        self.ev = numpy.argmin(times)
        # записываем таймер, записываем время ЧЕРЕЗ КОТОРОЕ ПРОИЗОЙДЕТ СОБЫТИЕ
        self.Engine.ES.MakeEvent(self, eval(self.SCC[self.CureCond].vec[self.ev].fun))        
        


#    def ChComp(self, fromC, toC):
#        """
#        Смена компартмента
#        """
#        fromC.removeCell(self)
#        toC.addCell(self)

# Инфраструктура событий
# События м.б. продуцирующими и дегенративными
# продуцирующие события запускают в конце метод-генератор нового события
# дегенративные этого не делают, в любом случае удаляются из текущего компартмента и, возможно что-то еще

    def sleep(self):
        """
        Минимальное событие, просто перезапускает генератор события (т.е. оттягивает время)
        """
        self.GenEv()
        
    def division(self):
        """
        Деление от материнской клетки наследует компартмент, это важно.
        Тут два момента
        1. Вопрос об ассиметричном делении. Вообще-то нет...
        2. Перегенерируем ли self?
        """
        cell(self.CureCond)
        self.GenEv()
    
    
    def assymDivision(self, name = None):
        """
        """
        cell(name)
        self.GenEv()
    
    def differentiation(self, cmprt):
        """
        Получается, что дифференцировка совпадает с переходом в другой компартмент
        """ 
        self.SCC[self.CureCond].remCell()
        self.CureCond = cmprt
        self.SCC[self.CureCond].addCell()


    def apoptosys(self):
        """
        Клетка самоудаляется из всех списков, и вычитает значение из компартмента. 
        По хорошему объект должен удалится сам
        """        
        self.SCC[self.CureCond].remCell()
    
    def toMature(self, name):
        self.MCC[name].addCell()
    def test(self,s):
        print('get -- > '+s)
#----------------------------------------------------------   
   

    def go(self):
        """
        Выполнить действие.
        Просто достаем строку из справочника по текущему состоянию и записанному событию
        Возвращаем дельту времени для запуска итератора интегральных компартментов
        """
        exec(self.SCC[self.CureCond].vec[self.ev].res)
        return self.Engine.ES.deltaT

class StopEvent(EventContainer):
    """
    Метод, переопределяющий функцию go таким образом, что она возвращает ошибку, останавливающую Ивент-сервер и расчет данного раунда
    """
    def go(self):
        raise AttributeError
    # какой-то бессмысленный метод, каменчу
    #def TurnOnFeedback(self,name):
    #    self.Engine.FB.changeDict(name)