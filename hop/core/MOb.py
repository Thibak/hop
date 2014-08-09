# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 16:54:50 2014

@author: user

MOb.py от Modell Objects

"""

import numpy

class AbstractCompartment:
    """
    Содержит ли компартмент собственную историю??
    Добавить можно всегда, потому пока нет.
    Абстрактный компартмент, это количество клеток
    """
    
    def __init__(self):
        self.n = 0
    def getQty(self):
        return self.n
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
    pass
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
    В этой функции будет куча всего
    """
    pass
    
    
#--------------------------------------------------
# клетки    
    
    
class cell:
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
    def __init__(self):
        self.CureCond = self.defCon
        self.SSC[self.CureCond].addCell()
        self.GenEv()
        
    def GenEv(self):
        """
        по справочнику определяем множество формул для данного состояния
        self.conditions[self.CureCond] -- возвращает какой-то объект, из которого мы получаем множество формул
        """
        #разыгрывем время до ближайших событий
#        act.append(self.s['l1']*numpy.random.weibull(self.s['a1'])) 
#        act.append(self.s['l2']*numpy.random.weibull(self.s['a2']))
#        i = numpy.argmin(act) #определяем какое из событий таки ближайшее

        # Достаём формулы
        # выкидываем время до события по формулам        
        times = []
        for i in range(len(self.conditions[self.CureCond])):
            times.append(eval(self.conditions[self.CureCond][i].fun))
        # определяем наименьшую
        # определяем соответствие событию
        # Ставим идентификатор события
        self.ev = numpy.argmin(times)
        # записываем таймер
        self.ES.MakeEvent(self, eval(self.conditions[self.CureCond][self.ev].fun))        
        
    def SetEventTime(self, Time):
        self.TimeWhen = Time

    def ChComp(self, fromC, toC):
        """
        Смена компартмента
        """
        fromC.removeCell(self)
        toC.addCell(self)
# фактически события
# проблема в том, что мне надо передавать тогда как атрибут кто делится и пр.
# т.е. это не собственный метод. Хотя можно их запихнуть в клетку, но это отрицательно скажется на памяти. Т.к. храним ссылки, то не значительно.
    def division(self):
        """
        Деление от материнской клетки наследует компартмент, это важно
        """
        pass
    
    def differentiation(self, cmprt):
        """
        Получается, что дифференцировка совпадает с переходом в новый компартмент
        """
        pass
    def apoptosys(self):
        """
        Клетка самоудаляется из всех списков, и вычитает значение из компартмента. 
        По хорошему объект должен удалится сам
        """        
        pass        
        
#----------------------------------------------------------   
   

    def go(self):
        """
        Выполнить действие.
        Просто достаем строку из справочника по текущему состоянию и записанному событию
        
        """
        eval(self.conditions[self.CureCond][self.ev].res)
