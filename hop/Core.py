# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:29:06 2014

@author: russinow

Ядро расчетов. 
- 1. Сервер событий. Не объект, как ни странно.


"""
import numpy
from collections import namedtuple
from operator import attrgetter

#def StartServer():
# сервер запускается сам собой при импорте. 
# Судя по всему как таковой необходимости его останавливать нет.
# по большому счету самого сервера как такового нет. 
# Импорт ядра выполняет ряд подготовительных операций
# 
# основные операции ядра, добавлять операцию в стек, и выполнять операции из стека.
# Автоматически сортировать стек по времени.
# вариант: Стек с переписанным пушем, поп остается старым, выдающим последнее значение
# а не создать ли отдельную библиотеку EventServer

# с каждым тиком времени значение в очереди как-то изменяется, и надо понять как делать сортировку
# Ответ: просто храним абсолютное время, т.е. время когда событие произойдет

# Start Event Server

class EStack(list):
    def push(self, element):
       super(EStack, self).append(element)
       super(EStack, self).sort(None, attrgetter('TimeWhen'), reverse=True) 

# фактически переопределение стринга с возможностью определять новые поля. 
# далее список (словарь?) возможных событий???
class EvType():
    #t = str
    def __init__(self, *args, **kwargs):
         self.s = str(*args, **kwargs)
    #def a(self):
    #    return self.t
    def __getattr__(self, name): 
        return getattr(self.s, name)  

# формат Ивента. 
      # namedtuple. Неизменяемый тип данных, а после события нам оно и не надо
      # Ивент содержит три типа данных, Type, Who, TimeWhen
          # Type -- тип события, пара значений, тип и вектор доп. данных
          # who -- кто, т.к. работаем с указателями, то просто event.cell = cell
          # timeWhen -- время в абсолютных единицах, по большому счету пофигу в каких. Важна только сортировка
Event = namedtuple ('Event', 'Type Who TimeWhen')

eventsL = EStack()
CurTime = 0

def MakeEvent():
    e = eventsL.pop()
    #e.Who
    pass # операциии с (e) 



#----------------------------- служебные объекты--------------------------------
class cell:
    """ Класс клетка.
        Умеет
          выдавать решение на следующую итерацию:
              делится,
              умирать (и вот вопрос, что с ней происходит, когда она умирает)
          возвращать  
        Есть реальный вариант наследовать этому: https://pypi.python.org/pypi/bintrees/2.0.1          
        Бинарное дерево можно использовать как структуру данных в клоне, и хранить в клетке только информацию о количестве делений
        а историю и время хранить в Клоне, в нодах дерева. Ожнако это не нужно пока нет проблемы с памятью
       и тут немного о Вейбуле и рисовании http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy          
          
          """
    def __init__(self, s=None):
        self.action_list = [] #вектор событий с данной клеткой
        self.time_list = [] #вектор последовательности времени до событий
        if s == None:
            p = programm()
            self.s = p.makeDict()
        else:
            self.s = s
    def action(self):
        act = []
        act.append(self.s['l1']*numpy.random.weibull(self.s['a1'])) #разыгрывем время до ближайших событий
        act.append(self.s['l2']*numpy.random.weibull(self.s['a2'])) #разыгрывем время до ближайших событий
        i = numpy.argmin(act) #определяем какое из событий таки ближайшее
        self.time_list.append(act[i]) #прицепляем минимальный элемент
        self.action_list.append(i) #прицепляем минимальный элемент -- номер события
        return i #возвращаем идентификатор события
    def getCumTime(self):
        return sum(self.time_list)

        
class clone:
    """ для дуплицирования объектов используется http://pymotw.com/2/copy/ """
    def __init__(self, s=None):
        self.live_cells = []
        self.cell_arch = []
        self.live_cells.append(cell(s))
        self.actions=[]
        self.track = []
    def tik(self):
        for i in self.live_cells:
            act = i.action()
            self.actions.append(act)
            if act == 0:
                self.live_cells.append(copy.deepcopy(i))
            if act == 1:
                move(self.cell_arch, self.live_cells, i)
        self.track.append(len(self))
    def NTiks(self, n):
        for i in range(n):
            self.tik()
    def do(self):
        while self.isAlive():
            self.tik()
            if self.getProductValue()>1000: 
                break
    def __len__(self): #getCloneValue:
        return len(self.live_cells)
    def getProductValue(self):
        return len(self.cell_arch)
    def isAlive(self):
        if len(self) == 0: 
            return False 
        else: return True
    
    
class core:
    def __init__(self):
        self.CurClone = clone()
        self.track = []
    def newClone(self,s):
        self.CurClone = clone(s)
    def iterate(self,n,s=None):
        self.product = []       
        self.result = []
        for i in range(n):
            self.newClone(s)
            self.CurClone.do()
            self.product.append(self.CurClone.getProductValue()) #прицепляем объем продукта
            self.result.append(self.CurClone.isAlive()) #прицепляем исход запуска клона
            self.track.append(self.CurClone.track)
    def plotTracks(self):
        for i in self.track: 
            plt.pyplot.plot(i)
        plt.show()
    def GetMeanRes(self):
        return numpy.mean(self.result)
    def GetMedRes(self):
        return numpy.median(self.result)
    def GetMeanProd(self):
        return numpy.mean(self.product)
    def GetMedProd(self):
        return numpy.median(self.product)