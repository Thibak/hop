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
          возвращать  """
    def __init__(self, s=None):
        self.action_list = [] #вектор событий с данной клеткой
        self.time_list = [] #вектор последовательности времени до событий
        if s == None:
            pass#self.s = programm.makeDict()
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
    def makeDict(a1=1,a2=1,l1=1,l2=1):
        s = {'a1':a1,'a2':a2,'l1':l1,'l2':l2}
        return s

class experiment:
    def __init__(self, f = None):
        if f == None:
            pass
        
        

            
