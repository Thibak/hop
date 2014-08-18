# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:32:42 2014

@author: russinow

Синтаксис фабрики:
from lxml.builder import ElementMaker
E = ElementMaker()
d = E.e
ff = E('ddd')

* Для XML-фабрики есть волшебная функция, выполняющая роль сериализатора списка. Т.к. фабрика понимает на входе как строку так и эелемент типа _element, то функция может спокойно использовать в построении фабрики.
Фишка в том, что тут передается элементы XMLя, у которого есть атрибут .append
def a(l, f):
  for i in range(len(l)):
   f.append(l[i])
  return f
ggg = d(a([d('1'),d('2')], d()))

Для пуша объектов в память используем str(), для извлечения используем eval()


Извлечение элементов

from lxml import etree
etree.tostring(ff)

"""

import lxml #.etree.ElementTree as ET
from lxml.builder import ElementMaker
from lxml import etree #<-- вспомогательная функция для сериализации
from types import NoneType
from datetime import datetime


def glue(l, f):
    """
    Склеить элементы из l функцией f
    Причем, вектор элементов может содержать любые элементы
    """
    for i in range(len(l)):
        f.append(l[i])
    return f


class Experiment():
    def __init__(self, filename=None):
        if filename == None:
            pass # м.б. вызов new()
        else:
            self.open(filename)
    def __repr__(self):
        out = 'Эксперимент:'
        # проверка открыт ли файл
        # проверка подгрузки параметров
        out += '\nИмя файла: '
        try: 
            out += self.filename
        except AttributeError:
            pass
        out += '\nCreated at: '
        try: 
            out += self.time.attrib['CreationTime']
        except AttributeError:
            pass
        out += '\nStatus: '
        try: 
            out += self.meta.attrib['status']
        except AttributeError:
            pass          
        out += "Расчет завершен на "       
        try: 
            out += str(self.progress())
            out += '%'
        except AttributeError:
            out += '0%'        

        return out   
        
# ----------- функции работы генератора задачи ---------
    def new(self, filename):
        if filename[-3:] != '.xml':
            filename += '.xml'
        try: 
            self.open(filename)
        except:
            self.filename = filename
            self.root = etree.XML('<root></root>')
            self.Factory = ElementMaker()
            self.tree = etree.ElementTree(self.root)
            # meta
            self.meta = self.Factory.meta()
            self.root.append(self.meta)
            # tasks
            self.tasks = self.Factory.tasks()
            self.root.append(self.tasks)
            #data
            self.data = self.Factory.data()
            self.root.append(self.data)   
            #status
            self.meta.set('status', 'Null')
            # time
            self.time = self.Factory.time()
            self.meta.append(self.time)        
            self.time.set('CreationTime', str(datetime.now()))
            #save
            self.save()
        else:
            print('File with such name alrady exist. File is open for reading.')
    def save(self, filename = None):
        if filename != None:
            self.filename = filename
        self.tree.write(self.filename, pretty_print=True)
            
    def setIter(self,iteration):
        self.meta.set('iteration', str(iteration))
        
    def MakeMatrix(self, Xvar, XX, Yvar, YY):
        # матрица. Может передавать не матрицы, а диапазоны и шаги?
        # что еще надо в матрице?
        if self.meta.attrib['status'] != 'Null':
            raise Exception('Task already given')
        self.meta.set('TaskType', 'M')
        matrix = self.Factory.matrix()  
        self.meta.append(matrix)
        matrix.append(self.Factory.x(str(XX.tolist()), name = str(Xvar)))
        matrix.append(self.Factory.y(str(YY.tolist()), name = str(Yvar)))
        # тут будет цикл, с makeTask 
        #z = [[x[i][j]+y[i][j] for i in range(len(x))] for j in range(len(y))]
        for i in range(len(XX)):
            for j in range(len(YY)):
                self.makeTask(i,j,XX[i][j],YY[i][j])
        self.meta.set('status', 'task')
        self.save()
    def makeVec(self, Xvar, XX):
        if self.meta.attrib['status'] != 'Null':
            raise Exception('Task already given')
        self.meta.set('TaskType', 'V')
        vec = self.Factory.vec()
        self.meta.append(vec)
        vec.append(self.Factory.x(str(XX.tolist()), name = str(Xvar)))
        for i in range(len(XX)):
            self.makeVTask(i,XX[i])
        self.meta.set('status', 'task')
        self.save()
    def makeMTask(self, i, j, x, y):
        mtask = self.Factory.mtask(i = str(i), j = str(j), x = str(x), y = str(y))
        self.tasks.append(mtask)
        #При свертывании выполняем двойной цикл в котором забиваем item.i = i, item.j = j, item.x = x[i][j], item.y = y[i][j], где x и y -- имена итерируемых переменных
    def makeVTask(self,i,x):
        vtask = self.Factory.vtask(i = str(i), x = str(x))
        self.tasks.append(vtask)
    def setModel(self, name):
        self.meta.set('modelFN', str(name))
# ------------функции работы парсера существующего файла  -------------------
    def open(self, filename):
        if filename[-3:] != '.xml':
            filename += '.xml'
        self.filename = filename
        self.tree = etree.parse(filename)
        self.root = self.tree.getroot()
        self.tasks = self.root.find('.//tasks')
        self.meta = self.root.find('.//meta')
        self.time = self.root.find('.//time')        
        # может быть и не надо предыдущее, т.к. можно использовать абсолютные фаинды            
            # тут нужно извлекать все, дабы каждый раз не обращаться к хмлью
        # ХОТЯ внимание, я этого не делаю для существующего без презакрытия. Что с этим елать? Переоткрывать? Не самый плохой вариант. А можно вынести в модуль renewStatus
        # ЭТО НЕобязательные параметры, т.ч. тут должны быть траи
        # проводить проверку статуса и в зависимости от подгружать параметры.
        #self.iterations = int(self.meta.attrib['iteration'])
        #self.modelFN    = self.meta.attrib['modelFN']
        #self.type = self.meta.attrib['TaskType']
        #self.stataus = self.meta.attrib['status']
# -------- функции работы обработчика -----------
    def LoadTask(self): #<-- фактически оболочка над итератором
        """
        ВАЖНО! Не забыть, что тут нужен трай, иначе в конце обработки будет вылет.
        Хотя можно и делать проверку по прогрессу.
        А можно реализовать ретурн 1/0 как индикатор загружено/нет
        
        ДОПОЛНИТЬ определителем типа задачи
        """
        # мы находим какой-то (любой) таск, и возвращаем словарь атрибутов? 
        # нет, т.к. ООП, то метод меняет текущие параметры. Т.е. LoadTask
        self.Task = {}
        self.CT = self.root.find('.//task')
        if type(self.CT) == NoneType:
            self.meta.set('status', 'complete')
            raise IndexError # попробовать выработку специфического ексепшена.
            
        # мне не нравится такой способ, надо как-то экранировать эти атрибуты, но пусть будет так.
        # хотя можно словарь сделать, как элементарный контейнер
        self.Task['i'] = int(self.CT.attrib['i'])
        self.Task['j'] = int(self.CT.attrib['j'])
        self.Task['x'] = int(self.CT.attrib['x'])
        self.Task['y'] = int(self.CT.attrib['y'])
    def writeData(self, data):
        """
        вопросыЖ
        1. Как затирать таски? -- очень просто, вызовом метода .clear()
        2. что писать? пока стоит рабочая заглушка
        3. определитель типа 
        """
        DI = self.Factory.item(str(data), i = str(self.i), j = str(self.j), x = str(self.x), y = str(self.y))
        self.data.append(DI)
        self.CT.clear()
        self.meta.set('status', 'progress')
        self.save()
    def progress(self):
        """
        Возвращает процент выполненной работы
        """
        if self.meta.attrib['status'] == 'Null' or 'task':
            return 0
        elif self.meta.attrib['status'] == 'complete':
            return 100
        elif self.meta.attrib['status'] == 'progress':
            return len(self.tasks.findall())/(len(self.tasks.findall())+len(self.data.findall()))*100
        else: raise Exception('No status')
    def status(self):
            return self.meta.attrib['status'] 
# -------- функции работы графического обработчика -------
    def getZ(self, nameZ):
        pass
        # возвращает матрицу, которая формируется из прочесываемых итемов. 
        # проверка на законченность вычислений