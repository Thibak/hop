# coding: utf8
import scipy.stats
import numpy
import copy

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
    def __init__(self, lbd, a):
        self.action_list = [] #вектор событий с данной клеткой
        self.time_list = [] #вектор последовательности времени до событий
        self.lbd = lbd 
        self.a = a
    def action(self):
        act = self.lbd*numpy.random.weibull(self.a,2) #разыгрывем время до ближайших событий
        i = numpy.argmin(act) #определяем какое из событий таки ближайшее
        self.time_list.append(act[i]) #прицепляем минимальный элемент
        self.action_list.append(i) #прицепляем минимальный элемент -- номер события
        return i #возвращаем идентификатор события
    def getCumTime(self):
        return sum(self.time_list)

        
class clone:
    def __init__(self, lbd, a):
        self.live_cells = []
        self.cell_arch = []
        self.live_cells.append(cell(lbd,a))
    def tik(self):
        actions=[]
        for i in self.live_cells:
            act = i.action()
            actions.append(act)
            if act == 0:
                self.live_cells.append(copy.deepcopy(i))
            if act == 1:
                move(self.cell_arch, self.live_cells, i)
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
    def newClone(self):
        self.CurClone = clone()
    def iterate(self,n):
        for i in range(n):
            self.newClone()
            

            
