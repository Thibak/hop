# -*- coding: utf-8 -*-
"""
DataDriver
@author: russinow
ReMONA V.1.0
http://russinow.me/

"""

from lxml.builder import ElementMaker
from lxml import etree # вспомогательная функция для сериализации
from datetime import datetime
from os.path import exists
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


mod_path = 'hop/models/'
scr_path = 'hop/mkscr/'

class minimal_function(object): pass

class Y(minimal_function):
    def __init__(self,_d={},**kwargs):
        kwargs.update(_d)
        self.__dict__=kwargs
    def __getitem__(self,key):
        return self.__dict__[key]
    def __repr__(self):
        return str(self.__dict__)
    def __getattr__(self,attr):
        return None
    def set(self,name, val):
        self.__dict__[name] = val



class XMLDriver():
    def __init__(self, filename=None):
        self.Factory = ElementMaker()
        if filename == None:
            pass # в будущих версиях вызов new()
        else:
            self.open(filename)
    def __repr__(self):
        out = 'Experiment:'
        # проверка открыт ли файл
        # проверка подгрузки параметров
        out += '\nFile Name: '
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
        out += "\n "       
        try: 
            out += str(self.progress())
            out += '% of calculation complete'
        except AttributeError:
            out += '0% of calculation complete'  
        try:
            out += "\nWhich makes up "       
            out += self.rate() 
            out += " takes"
        except NameError:
            pass
        return out   
        
# ----------- функции работы генератора задачи ---------
    def new(self, filename):
        if filename[-3:] != '.xml':
            filename += '.xml'
        try: 
            self.open(filename)
        except IOError:
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
    def addScriptFile(self, filename):
        if '/' not in filename:
            filename = scr_path + filename
        if filename[-2:] != '.py':
            filename += '.py'
        if exists(filename):
            self.meta.set('ScriptFileName', filename)
            self.save()
            print ('Monte-Carlo model script has been added')
    def loadScript(self):
        exec(compile( open(self.meta.attrib['ScriptFileName']).read(), self.meta.attrib['ScriptFileName'], 'exec') )
    def addVScript(self, script):
        vscript = self.Factory.vscript(script)
        self.meta.remove(self.meta.find('.//vscript'))
        self.meta.append(vscript)
        self.save()
    def addSScript(self, script):
        sscript = self.Factory.sscript(script)        
        self.meta.remove(self.meta.find('.//sscript'))
        self.meta.append(sscript)
        self.save()
    def makeMatrix(self, Xvar, xstart, xstop, xstep, Yvar, ystart, ystop, ystep):
        XX = np.arange(xstart, xstop, xstep)
        YY = np.arange(ystart, ystop, ystep)
        if self.meta.attrib['status'] != 'Null':
            raise Exception('Task already given')
        self.meta.set('TaskType', 'M')
        matrix = self.Factory.matrix()  
        self.meta.append(matrix)
        matrix.append(self.Factory.x(str(XX.tolist()), name = str(Xvar)))
        matrix.append(self.Factory.y(str(YY.tolist()), name = str(Yvar)))

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
        self.filename = filename
        self.tree = etree.parse(filename)
        self.root = self.tree.getroot()
        self.tasks = self.root.find('.//tasks')
        self.meta = self.root.find('.//meta')
        self.data = self.root.find('.//data')
        self.time = self.root.find('.//time')

        try: self.iterations = int(self.meta.attrib['iteration'])
        except KeyError: print('failed to load number of iterations')
        try: self.modelFN    = self.meta.attrib['modelFN']
        except KeyError: print('failed to load name of file of model')
        try: self.type = self.meta.attrib['TaskType']
        except KeyError: print('failed to load type of task')
        try: self.stataus = self.meta.attrib['status']
        except KeyError: print('failed to load status')
        try:
            if self.meta.attrib.get('TaskType') == 'M':
                self.TaskType = 'M'
                self.Xvar = str(self.root.find('.//x').attrib.get('name'))
                self.Yvar = str(self.root.find('.//y').attrib.get('name'))           
            elif self.meta.attrib.get('TaskType') == 'V':
                self.TaskType = 'V'
                self.Xvar = str(self.root.find('.//x').attrib.get('name')) 
                self.Yvar = None
            else:
                raise Exception('Mistake in file (type of task not specified)')
        except KeyError: print('failed to load task type')
        try: self.remain = len(self.root.findall('.//task'))
        except TypeError:  self.remain = 0
        
# -------- функции работы обработчика -----------
    def LoadTask(self): 
        """
        оболочка над итератором
        """

        self.CT = self.root.find('.//task')
        if type(self.CT) == type(None):
            self.meta.set('status', 'complete')
            self.save()
            raise IndexError # попробовать выработку специфического ексепшена.
        self.Task = Y()
        if self.TaskType == 'M':          
            self.Task.i = int(self.CT.attrib.get('i'))
            self.Task.j = int(self.CT.attrib.get('j'))
            self.Task.x = float(self.CT.attrib.get('x'))
            self.Task.y = float(self.CT.attrib.get('y'))
        elif self.TaskType == 'V':          
            self.Task.i = int(self.CT.attrib.get('i'))
            self.Task.x = float(self.CT.attrib.get('x'))
        else:
            raise Exception('Mistake in file (type of task not specified)')        
        
    def loadConst(self):
        """
        Возвращает dict, которым делаем апдейт словаря констант
        """
        const_dict = {}
        const_dict[self.Xvar] = self.Task.x
        const_dict[self.Yvar] = self.Task.y
        return const_dict 
        
    def delTask(self):
        if self.meta.attrib['status'] != 'Null':
            print('No task')
        elif self.meta.attrib['status'] == 'task':
            self.tasks.clear()
            self.meta.set('status', 'Null')
        else:
            print ("Calculations started (or complit), you cannot delete the task you've started")
        #raise Exception('Task already given')
        
    def writeData(self, data):
        """ 
        """
        if self.TaskType == 'M':
            DI = self.Factory.item(str(data), i = str(self.Task.i), j = str(self.Task.j), x = str(self.Task.x), y = str(self.Task.y))
        elif self.TaskType == 'V':
            DI = self.Factory.item(str(data), i = str(self.Task.i), x = str(self.Task.x))
        else:
            raise Exception ("Data recording mistake, no task type, broken TaskType. Results not recorded")
        self.data.append(DI)
        prnt = self.CT.getparent()
        prnt.remove(self.CT)
        self.meta.set('status', 'progress')
        self.save()
        
    def progress(self):
        """
        Возвращает процент выполненной работы
        """
        if self.meta.attrib['status'] in 'Nulltask':
            return 0
        elif self.meta.attrib['status'] == 'complete':
            return 100
        elif self.meta.attrib['status'] == 'progress':
            return float(len(self.data.findall('.//')))/(len(self.tasks.findall('.//'))+len(self.data.findall('.//')))*100
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
# Графический обработчик должен эмулировать все  функции, для работы с матплотлибом.

    def plot(self, name, aprType = 'mean', plotSymb = ''):
        """
        Запускает отрисовку указанной характеристики.
        первый аргумент -- имя зависимой переменной
        второй аргумент (по умолчанию 'mean')
        """
        if self.TaskType == 'V':
            alldata = self.root.findall('.//item')
            X = [None]*len(alldata)
            Z = [None]*len(alldata)
            for item in alldata:
                X[int(item.attrib['i'])] = item.attrib['x'] 
                data = eval(item.text)
                Z[int(item.attrib['i'])] = data[name][aprType]
            plt.plot(X,Z,plotSymb)
            plt.xlabel(self.Xvar)
            plt.ylabel(name)
            plt.show()
        elif self.meta.attrib.get('TaskType') == 'M':
            alldata = self.root.findall('.//item')
            X = [None]*len(alldata)
            Y = [None]*len(alldata)
            Z = [[None]*len(alldata)]*len(alldata)
            for item in alldata:
                X[int(item.attrib['i'])] = item.attrib['x'] # ставим полученное значнеие на нужное место
                Y[int(item.attrib['j'])] = item.attrib['y']
                data = eval(item.text)
                Z[int(item.attrib['i'])][int(item.attrib['j'])] = data[name][aprType]
            XX, YY = np.meshgrid(X, Y)
            ZZ = np.array(Z)
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.plot_surface(XX, YY, ZZ)
            plt.show()
        else:
            print('Mistake in file (type of task not specified)')        
        pass

        
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
        """
        # далее интерфейсы для монтекарловского скрипта
        for mtrname in self.names.list:
            matrix = self.val[mtrname] 
            data = Y()
            exec(self.vscr)
            self.data[mtrname] =  eval(str(data)) 
        for vecname in self.names.float:
            vector = self.val[vecname]
            data = Y()
            exec(self.sscr)  
            self.data[vecname] = eval(str(data))
            
    def PushData(self,XMLi):
        XMLi.writeData(str(self.data))
        