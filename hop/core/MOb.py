# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 16:54:50 2014

@author: user

MOb.py от Modell Objects

"""


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
        
#----------------------------------------------------------   
   

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
