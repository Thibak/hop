# coding: utf8
#import scipy.stats
import numpy
import copy
import pickle #загружаем и сохраняем данные
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import arange
from matplotlib.mlab import griddata

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
      
    Внимание вопрос: как сохранять объекты? 
        есть масса вариантов, 
        
  ----> во первых pickle как стандартная библиотека сохранения и извлечения объектов.
        пока реализуем этот самый простой вариант. Тем более, что 
            плюсы
                нативность
            минусы
                читается только питоном же
            Проблемы: 
                все отлично читается и сохраняется, за исключением того, что загрузка самого себя вещь странная.
                 весьма вероятно, что она не будет работать. 
                А сохранять только словарь из всего объекта не правильно, т.к. кроме словаря у меня имеется несколько объектов с важной информацией
                 
                ВОТ И ДУМАЙ...
                
                
        во вторых CSV 
            плюсы
                читаемость SASом 
                читаемость и редактируемость руками
            минусы
                ненативность
        в третьих XML
            плюсы 
            минусы
        в четвертых JSON
            плюсы 
            минусы
      по теме:
          чтение и запись словаря в текстовый файл
          http://stackoverflow.com/questions/11026959/python-writing-dict-to-txt-file-and-reading-dict-from-txt-file
     
      
    """
    
    def __init__(self,itr = 100):
        self.element = []
        self.block = False
        self.itr = itr
        self.dict = {'a1':1,'a2':1,'l1':1,'l2':1}
        self.isCalc = False
        
    def chPrec(self, n):
        self.isCalc = False
        self.itr = n
        
        
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
    def keys(self): return self.dict.keys()
    def makeDict(self, a1=1,a2=1,l1=1,l2=1):
        return self.dict
        
    # высокоуровневые операции по формированию 
    def makeGrid(self, name1, start1, stop1, step1, name2, start2, stop2, step2):
        self.isCalc = False
        if name1 in self.dict.keys() and name2 in self.dict.keys():
            a = arange(start1, stop1, step1)
            b = arange(start2, stop2, step2)
            for j in a:
                for i in b:
                    self.chAttr(name1,j)
                    self.chAttr(name2,i)
                    self.push()
        else:
            print ('No such name. Grid creation aborted')
  
#        [[[self.addDict(i),k] for i in range(4)] for k in range(4)]  
    def makeVec(self, name, start, stop, step):
        self.isCalc = False
        if name in self.dict.keys():
            a = arange(start, stop, step)
            for i in a:
                self.chAttr(name,i)
                self.push()
        else:
            print ('No such name')
    # Подсистема сохранения и извлечения программы эксперимента
    def save(self,name):
        if self.isCalc:
            with open(name + '.rst', 'wb') as f:
                pickle.dump(self, f)
        else:
            with open(name + '.dic', 'wb') as f:
                pickle.dump(self, f)
    def open(self,name):
        with open(name, 'rb') as f:
            p = pickle.load(f)
        if 
                       
        

class experiment:
    """ 
    Объект эксперимент
        задачи: написать инициализацию по словарю
        написать вытакивалку имен параметров и результатов
        
        ВАЖНО!!! 
        По факту система выполнения действий является ассинхронной (т.е. мы выполняем события не в хронологическом порядке),
        в связи с чем мы не можем выполнять взаимодействия и обратные связи.
        Для избежания этой проблемы необходимо создать централизованый стек (с сортировкой после каждого пуша) 
        он должен принадлежать к обработчику, быть единым для всех клонов. 
        Т.е. операцию итерирования мы изымаем из ведения клона. Может быть клон вобще должен быть атрибутом клетки, и не более
        
        НО ЭТО ПОЗЖЕ...

    """
    def __init__(self, p = None):
        self.c = core()
        
        if p == None:
            self.p = programm()
            
    def setDict(self,p):
        self.p = p
    def do(self):
        self.p.isCalc=True
        i = 0
        for s in self.p.element:
            i=i+1
            print("calculating " + str(i) + ' from ' + str(len(self.p.element)))
            print s
            self.c.iterate(self.p.itr,s)
            s['MeanRes'] = self.c.GetMeanRes()
            s['MedRes'] = self.c.GetMedRes()
            s['MeanProd'] = self.c.GetMeanProd()
            s['MedProd'] = self.c.GetMedProd()
        
            
            
    def plot(self, resName, param1, param2 = None, t = 'p'):
        '''
        Если 1 параметр передается, то рисуется 2D график, если два, то 3D       
        
        Для интерполяции неструктурированых данных (кои дефакто мы и имеем, хотя это не совсем так) 
         надо использовать функцию from matplotlib.mlab import griddata. 
         Например как тут: http://matplotlib.org/examples/pylab_examples/griddata_demo.html
         Размерность сетки интерполяции мб такой же как и у данных
        '''
        # сначала надо вытащить из словаря итерируемые значения
        #if resName = 'all'        
        
        if self.p.isCalc:
            print('ATTENTION, object is unCalc')
        
        if param2 == None:
            y = [self.p.element[i][resName] for i in range(len(self.p.element))]
            x = [self.p.element[i][param1] for i in range(len(self.p.element))] 
            plt.pyplot.plot(x, y, 'yo-')
            plt.pyplot.show()
        else:
            z = [self.p.element[i][resName] for i in range(len(self.p.element))]
            x = [self.p.element[i][param1] for i in range(len(self.p.element))] 
            y = [self.p.element[i][param2] for i in range(len(self.p.element))] 
            fig = plt.pyplot.figure()
            axes = Axes3D(fig)
            
            axes.set_xlabel(param1)
            axes.set_ylabel(param2)
            axes.set_zlabel(resName)            
            
          #  axes.scatter3D(x,y,z, c=z)
            
          #  xi = numpy.linspace(0,1,100)
          #  yi = numpy.linspace(0,1,100)
            # grid the data.
          #  zi = griddata(x,y,z,xi,yi,interp='linear')

           # axes.plot_wireframe(X, Y, Z)
          #  axes.plot_surface(xi,yi,zi)
            
        #    plt.pyplot.colorbar()
            #axes.plot(x,y,z)
            #axes.plot_wireframe(x, y, z)
            fig.show()



            
