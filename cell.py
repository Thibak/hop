# coding: utf8
import scipy.stats
import numpy
import copy
import matplotlib as plt

def move(a,b,i): #перемещение из одного списка в другой
    a.append(i)
    b.remove(i)


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
       и тут немного о Вейбулеи рисовании http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy          
          
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
    def tst():
        print ("test")

        
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
    def GetMeanRes(self):
        return numpy.mean(self.result)
    def GetMedRes(self):
        return numpy.median(self.result)
    def GetMeanProd(self):
        return numpy.mean(self.product)
    def GetMedProd(self):
        return numpy.median(self.product)

class programm:
    """
    Программа вычислений.
      видимо мы должны иметь хитрую структуру из многомерных словарей, 
      где описываются имена клонов и их количество, и словари для них. 
      Количество итерации не должно отличаться для отдальных элементов. (если оно не адаптивное!!!)
        храним тут:
            iter -- количество итераций для каждой точки
            s -- вектор словарей для деления
    кроме того имеем конструкторы всяких подсущностей плана эксперимента
    [{'sth':[1,1,1], 'sthe':[1,1]}]
    addAttr(self, '____', vk = [], n = 1) -- добавить атрибут, с вектором (можно загнать пустой), если надо то много раз

            
    """
    def __init__(self,f="default"):
        attrList = {'dict':1}
        if f == "default":
            self.itr = 1000
            
    def makeDict(self, a1=1,a2=1,l1=1,l2=1):
        s = {'a1':a1,'a2':a2,'l1':l1,'l2':l2}
        return s
    def addAttr(self, strg, vk = [], n = 1):
        pass
        

class experiment:
    """ 
    Это собственно программа читающая файл-программу-вычислений, представляющую собой
    вектор пар команда-аргументы. Я последовательно читаю команды, и выполняю их с этими аргументами
    ПРИЧЕМ! Это могут быть команды загрузки 
    """
    def __init__(self, f = None):
        if f == None:
            pass
        
        

            
