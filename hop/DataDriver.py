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

#import lxml #.etree.ElementTree as ET
from lxml.builder import ElementMaker
from lxml import etree #<-- вспомогательная функция для сериализации
from datetime import datetime
from os.path import exists
import numpy as np

#import os

#from hop import mod_path
mod_path = 'hop/models/'

class minimal_function(object): pass

class Y(minimal_function):
    def __init__(self,_d={},**kwargs):
        kwargs.update(_d)
        self.__dict__=kwargs
    def __getitem__(self,key):
        return self.__dict__[key]
    def __repr__(self):
        #return 'Y:%s'%self.__dict__
        return str(self.__dict__)
    def __getattr__(self,attr):
        return None
    def set(self,name, val):
        self.__dict__[name] = val

    
        
#def glue(l, f):
#    """
#    Склеить элементы из l функцией f
#    Причем, вектор элементов может содержать любые элементы
#    """
#    for i in range(len(l)):
#        f.append(l[i])
#    return f


class XMLDriver():
    def __init__(self, filename=None):
        self.Factory = ElementMaker()
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
        out += "\nРасчет завершен на "       
        try: 
            out += str(self.progress())
            out += '%'
        except AttributeError:
            out += '0%'  
        try:
            out += "\nЧто составляет "       
            out += self.rate() 
            out += "задач"
        except:
            pass
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
        self.save()
    def addVScript(self, script):
        vscript = self.Factory.vscript(script)
        self.meta.append(vscript)
        self.save()
    def addSScript(self, script):
        sscript = self.Factory.sscript(script)
        self.meta.append(sscript)
        self.save()
    def makeMatrix(self, Xvar, xstart, xstop, xstep, Yvar, ystart, ystop, ystep):
        # матрица. Может передавать не матрицы, а диапазоны и шаги?
        # что еще надо в матрице?
        XX = np.arange(xstart, xstop, xstep)
        YY = np.arange(ystart, ystop, ystep)
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
    def makeVec(self, Xvar, start, stop, step):
        XX = np.arange(start, stop, step)
        if self.meta.attrib['status'] != 'Null':
            print('Task already given')
            return
            #raise Exception('Task already given')
        self.meta.set('TaskType', 'V')
        vec = self.Factory.vec()
        self.meta.append(vec)
        vec.append(self.Factory.x(str(XX.tolist()), name = str(Xvar)))
        for i in range(len(XX)):
            self.makeVTask(i,XX[i])
        self.meta.set('status', 'task')
        self.save()
    def makeMTask(self, i, j, x, y):
        task = self.Factory.task(i = str(i), j = str(j), x = str(x), y = str(y))
        self.tasks.append(task)
        #При свертывании выполняем двойной цикл в котором забиваем item.i = i, item.j = j, item.x = x[i][j], item.y = y[i][j], где x и y -- имена итерируемых переменных
    def makeVTask(self,i,x):
        task = self.Factory.task(i = str(i), x = str(x))
        self.tasks.append(task)
    def setModel(self, filename):
        if '/' not in filename:
            filename = mod_path + filename
        if filename[-2:] != '.py':
            filename += '.py' 
        if exists(filename):
            self.meta.set('modelFN', str(filename))
        else:
            print "No such file. Model not added"
        self.save()
        
# ------------функции работы парсера существующего файла  -------------------
    def open(self, filename):
        if filename[-3:] != '.xml':
            filename += '.xml'
#        print (os.getcwd())
#        print(filename)
        self.filename = filename
        self.tree = etree.parse(filename)
        self.root = self.tree.getroot()
        self.tasks = self.root.find('.//tasks')
        self.meta = self.root.find('.//meta')
        self.data = self.root.find('.//data')
        self.time = self.root.find('.//time')
        # тут нужно извлекать все, дабы каждый раз не обращаться к хмлью
        # ХОТЯ внимание, я этого не делаю для существующего без презакрытия. Что с этим елать? Переоткрывать? Не самый плохой вариант. А можно вынести в модуль renewStatus
        # не самый лучший вариант, т.к. мы снова читаем хмль, Может быть стоит дважды прописать
        try: self.iterations = int(self.meta.attrib['iteration'])
        except: print('failed to load number of iterations')
        try: self.modelFN    = self.meta.attrib['modelFN']
        except: print('failed to load name of file of model')
        try: self.type = self.meta.attrib['TaskType']
        except: print('failed to load type of task')
        try: self.stataus = self.meta.attrib['status']
        except: print('failed to load status')
        #
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
        
        self.CT = self.root.find('.//task')
        if type(self.CT) == type(None):
            self.meta.set('status', 'complete')
            raise IndexError # попробовать выработку специфического ексепшена.
        self.Task = Y()
#        <--------------- переделать таск в Y, тогда присвоение идет через гетатр
        #self.Task = {}
        if self.meta.attrib.get('TaskType') == 'M':
            self.Task.TaskType = 'M'
            self.Task.Xvar = str(self.root.find('.//x').attrib.get('name'))
            self.Task.Yvar = str(self.root.find('.//y').attrib.get('name'))           
            self.Task.i = int(self.CT.attrib.get('i'))
            self.Task.j = int(self.CT.attrib.get('j'))
            self.Task.x = float(self.CT.attrib.get('x'))
            self.Task.y = float(self.CT.attrib.get('y'))
        elif self.meta.attrib.get('TaskType') == 'V':
            self.Task.TaskType = 'V'
            self.Task.Xvar = str(self.root.find('.//x').attrib.get('name'))           
            self.Task.i = int(self.CT.attrib.get('i'))
            self.Task.x = float(self.CT.attrib.get('x'))
        else:
            raise Exception('ошибка в файле (нет типа задания)')
        # мне не нравится такой способ, надо как-то экранировать эти атрибуты, но пусть будет так.
        # хотя можно словарь сделать, как элементарный контейнер
        #делаем подгрузку через try. Через сортировку того, что может
        # перенес выше
        
    def loadConst(self):
        """
        Возвращает dict, которым делаем апдейт словаря констант
        """
        const_dict = {}
        const_dict[self.Task.Xvar] = self.Task.x
        const_dict[self.Task.Yvar] = self.Task.y
        return const_dict 
    def delTask(self):
        if self.meta.attrib['status'] != 'Null':
            print('задача не задана')
        elif self.meta.attrib['status'] == 'task':
            self.tasks.clear()
            self.meta.set('status', 'Null')
        else:
            print ('Расчет начат, нельзя удалить начатую задачу')
        #raise Exception('Task already given')
        
    def writeData(self, data):
        """
        вопросыЖ
        1. Как затирать таски? -- очень просто, вызовом метода .clear()
        2. что писать? пока стоит рабочая заглушка
        3. определитель типа 
        """
        #<----------------- тут доделать записываемые параметры. и и жи достаются неправильно и надо еще что-то записывать. А если не матрица!?
        if self.Task.TaskType == 'M':
            DI = self.Factory.item(str(data), i = str(self.Task.i), j = str(self.Task.j), x = str(self.Task.x), y = str(self.Task.y))
        elif self.Task.TaskType == 'V':
            DI = self.Factory.item(str(data), i = str(self.Task.i), x = str(self.Task.x))
        else:
            print "ошибка записи данных, нет типа задачи, битый Task.TaskType. Результаты не записаны"
        self.data.append(DI)
        prnt = self.CT.getparent()
        prnt.remove(self.CT)
        #self.CT.clear()
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
            return len(self.tasks.findall('.//'))/(len(self.tasks.findall('.//'))+len(self.data.findall('.//')))*100
        else: raise Exception('No status')
    def rate(self):
        return str(len(self.tasks.findall('.//'))) + ' from ' + str(len(self.tasks.findall('.//'))+len(self.data.findall('.//')))
    def status(self):
            return self.meta.attrib['status'] 
    def getVScript(self):
        return str(self.meta.find('vscript').text)
    def getSScript(self):
        return str(self.meta.find('sscript').text)
# -------- функции работы графического обработчика -------
    def getZ(self, nameZ):
        pass
        # возвращает матрицу, которая формируется из прочесываемых итемов. 
        # проверка на законченность вычислений
        
class DataMachine:
    def __init__(self):
        self.names = Y()
        self.erase()
        
    def erase(self): 
        self.names.float = []
        self.names.list = []    
        self.val = {} 
        self.data = {}
        
    # ------------ подготовка ------------
    def LoadScripts(self, XMLi):
        self.vscr = compile(XMLi.getVScript(),'<string>', 'exec')
        self.sscr = compile(XMLi.getSScript(),'<string>', 'exec')
        
    def AnalizeModel(self, dictn):
        for dataname in dictn:
            if type(dictn.get(dataname)) == float:
                self.names.float.append(dataname)
            if type(dictn.get(dataname)) == list:
                self.names.list.append(dataname)

        # подготавливаем слоты для данных      
        self.val.update({k:[] for k in self.names.list + self.names.float})    
    #-------------- постобработка -------------        

    def addData(self, dc):
        for dataname in self.names.list + self.names.float:
            self.val[dataname].append(dc.getVal(dataname))
        
    def CollapseData(self):
        """
        Для скриптов интерфейс следующий:
        для получения данных используем matrix и vector, которые list и nested list
        для результатов используем data. дальше нужное имя
        
        В связи с форматом написать функцию извлечения данных getZ 40-ка строками выше
        """
        for mtrname in self.names.list:
            #<----------------------
            # непонятно почему я не присваиваю matrix ни куда..
            matrix = self.val[mtrname] # <-------- это и следующее нужно как интерфейс для монтекарловского скрипта
            data = Y()
            exec(self.vscr)
            self.data[mtrname] = eval(str(data)) # что бы внутри хранились словари
            # страшно корявая реализация, но пусть будет 
            #  проблема в том, что внутри мы храни
            
        for vecname in self.names.float:
            vector = self.val[vecname]
            data = Y()
            exec(self.vscr)  
            self.data[vecname] = eval(str(data)) # что бы внутри хранились словари
            
    def PushData(self,XMLi):
        XMLi.writeData(str(self.data))