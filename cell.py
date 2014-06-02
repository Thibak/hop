# coding: utf8
#import scipy.stats
import numpy
import copy
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D

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
   # def newClone(self,s)
#        self.CurClone = clone(s)"""
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

class programm:
    """
    Программа вычислений.
            iter -- количество итераций для каждой точки
            element -- вектор словарей -- задание на эксперимент
      Видимо структура объекта такая, до первого запуска операции push, 
      которая загоняет словарь в стек, мы можем добавлять атрибуты, 
      после этого мы блокируем объект. Кроме того надо написать модули сохранения и извлечения словарей.
      
      После обработки программы каждое задание становилтся экспериментом, 
      т.е. дополняется результатами. После этого мы должны мочь его так же сохранить
      
      self.dict.keys() -- значения ключей
      
      для присвоения нового атрибута используем      
      p.dict['имя']=значение
      НЕ ИСПОЛЬЗУЕМ, ИНАЧЕ БЛОКИРОВКА НЕ БУДЕТ РАБОТАТЬ      
      
      addAttr
         [[[a(i),k] for i in range(4)] for k in range(4)]   
    """
    
    def __init__(self,f="default"):
        self.element = []
        self.block = False
        if f == "default":
            self.itr = 1000
            self.dict = {'a1':1,'a2':1,'l1':1,'l2':1}
        
    def push(self):
        self.block = True
        self.element.append(copy.deepcopy(self.dict))
        
    def addAttr(self, name, value):
        """ Добавление атрибута к словарю """
        if self.block:
            print ('attempt rejected')
        else:
            self.dict[name]=value
    def chAttr(self,name, value):
        if name in self.dict.keys():
            self.dict[name]=value
        else:
            print ('No such name')
    def keys(self): self.dict.keys()
    def makeDict(self, a1=1,a2=1,l1=1,l2=1):
        return self.dict
        
    # высокоуровневые операции по формированию 
    def makeGrid(self, name1, start1, stop1, step1, name2, start2, stop2, step2):
        a = frange(start1, stop1, step1)
        b = frange(start2, stop2, step2)
        for j in a:
            for i in b:
                self.chAttr(name1,j)
                self.chAttr(name2,i)
                self.push()
  
#        [[[self.addDict(i),k] for i in range(4)] for k in range(4)]  
    def makeVec(self, name, start, stop, step):
        a = frange(start, stop, step)
        for i in a:
            self.chAttr(name,i)
            self.push()
  
        

class experiment:
    """ 
    Объект эксперимент
    """
    def __init__(self, p = None):
        self.c = core()
        if p == None:
            p = programm('default')
            p.addDict(p.makeDict())
    def do(self,p):
        for e in p:
            self.c.iterate(e)
            
            
    def plot(self, param = 'result'):
        # сначала надо вытащить из словаря итерируемые значения
        x = [self.p.element[i][param] for i in range(len(self.p.element))] 
        # а -- идентификатор итерируемого значения
        
        # надо все результаты тоже загонять в словарь!!! И вытаскивать по той же конструкции
        
        # затем 
        fig = plt.figure()
        axes = Axes3D(fig)
        #axes.scatter3D(a,a,a)
        axes.plot(x,y,z)
        #axes.plot_wireframe(x, y, z)
        fig.show()



            
