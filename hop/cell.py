# coding: utf8
#import scipy.stats

import numpy


 
from hop.plan import Plan

def move(a,b,i): #перемещение из одного списка в другой
    a.append(i)
    b.remove(i)


class Cell:
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
            p = Plan()
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

        

    


                       
        



            
