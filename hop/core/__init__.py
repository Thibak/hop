# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:29:06 2014

@author: russinow

Ядро расчетов. 
- 1. Сервер событий. Не объект, как ни странно.


"""
import numpy
#from collections import namedtuple
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


# event server
class EStack(list):
    def push(self, element):
       super(EStack, self).appendppend(element)
       super(EStack, self).sort(None, attrgetter('TimeWhen()'), reverse=True) 

# фактически переопределение стринга с возможностью определять новые поля. 
# далее список (словарь?) возможных событий???
# Представляет собой строку с дополнительными параметрами. 
# в строке должно храниться имя типа события, например деление или миграция в след. слой. 
# НЕ БУДЕМ ИСПОЛЬЗОВАТЬ
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
          # who -- кто, т.к. работаем с указателями, то просто event.who = cell
          # timeWhen -- время в абсолютных единицах, по большому счету пофигу в каких. Важна только сортировка
#Event = namedtuple ('Event', 'Type attr Who TimeWhen')
# механизм хороший, но предется отказаться от него в пользу хранения всех данных в самой клетке
# по хорошему Event определяет дальнейшие действия, и вопрос!!!
# определять это по коду или по слову. Или каким-то идентификатором. Для меня пока не понятно.
# можно определять список допустимых событий из типа объекта по словарю, хотя это финт ушами

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

# фактически события
# проблема в том, что мне надо передавать тогда как атрибут кто делится и пр.
# т.е. это не собственный метод. Хотя можно их запихнуть в клетку, но это отрицательно скажется на памяти.
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

#----------------------------- служебные объекты--------------------------------
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
        """
        Пока функция-заглушка (виртуальная функция??) 
        """
        self.n = self.n+1
class SCC(AbstractCompartment, list):
    """
    Отличие от абстракта     
    Пререкрывает ли вызов собственного инита инит родительского класса?
    """
    def getQty(self):
        return len(self)
    def addCell(self, cell):
        super(StemCompartment, self).append(cell)
    def removeCell(self, cell):
       # try:
            super(StemCompartment, self).remove(cell)
       # except:
       #    pass
        
class MCC(AbstractCompartment):
    """
    В этой функции будет куча всего
    """
    pass
    
    
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
    def __init__(self, cmprt):
        cmprt.addCell(self)
        Объявляем внутренние переменные        
        Генерируем нулевое событие. Ктъры ест рождение.
    def ChComp(self, fromC, toC):
        """
        Смена компартмента
        """
        fromC.removeCell(self)
        toC.addCell(self)
        
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