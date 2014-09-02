# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:29:06 2014

@author: russinow

Ядро расчетов. 
- 1. Сервер событий. Не объект, как ни странно.


"""
import datetime

from MOb import EventContainer
from MOb import cell
from MOb import SCC
from MOb import MCC
from AOb import EventServer
from AOb import FeedBackSever, DataCollector
from hop.DataDriver import Y, minimal_function
from hop.usrexcept import setScript, UException1, UException2, UException3, UException4, UException5, UException6     


#импорт для работы скрипта описания модели:
from AOb import Event
from MOb import EventContainer
from MOb import StopEvent
# Главный объект


class Engine:
    """
    
    """
    const = Y()
    def __init__(self):
        # создаем ссылку на класс клеток внутри Движка
        self.cell = cell
        EventServer.Engine = self
        FeedBackSever.Engine = self
        EventContainer.Engine = self
        DataCollector.Engine = self
        # self.cell.Engine = self <-- в этой строке нет необходимости, т.к. есть предыдущая
        #self.EventContainer = EventContainer
        # Добавляем пустой словарь для состояний клетки (новая формация для структуры)
        # Создаем экземпляр Сервера Событий
        self.ES = EventServer()
        self.FB = FeedBackSever()
        self.DC = DataCollector()
        self.DC.addDataPoint('calctime', 's'),
        #self.FB.Engine = self
        #Закладываем ссылку на сервер событий с целью прямой закладки
        #self.cell.ES = self.ES  
        #изменено, т.к. cell наследуется от EventContainer
        # 
        self.SCC = {}
        self.cell.SCC = self.SCC        
        self.MCC = {}
        self.cell.MCC = self.MCC 
        #Куммулятивные показатели
        self.TimeLine = []
    
        #Хитрый пустой слот, который мы запиливаем как заглушку тактовому сборщику данных.
        self.taktalSlot = compile('','<string>','exec')
        #compile('','<string>','exec')        

    def addCondition(self, name, vec):
        """
        Формат словаря --
        Имя состояния : вектор объектов-дуплетов -- Ивентов (namedtuple)
        индекс: функция-исход
        Для внутренних обработок достаточно пары имяСостояния-индекс. Я никак не буду оперировать индексом кроме как для хранения на этапе выполнения
        """
# <-- Дописать проверку
        self.SCC[name] = SCC()
        self.SCC[name].vec = vec
        # слоты для оценки количества клеток в состояниях
        
        
    def setDefCond(self, name):
        if name in self.SCC:
            self.cell.defCon = name
        else:
            raise Exception('setDefCond: Нет такого состояния')

    def addCompartment(self, name, internal, transition, to):
        """
        name -- имя компартмента
        internal -- функция от N и dt изменения внутреннего сосотояния
        transition -- функция от N и dt перехода
        to -- куда??
        """
        self.MCC[name] = MCC(internal, transition, to)

    def start(self):
        """
        Сначала запускаем такт ивентсервера, откуда получаем длину шага времени
        записываем длину шага времени
        запускаем объекты принимающие шаг времени.   
        """
        # создаем первую клетку, ставим состояние по умолчанию
        # как ни странно, ни чему не надо ее присваивать, Т.к. клетка делает все сама.
        st = datetime.datetime.now()
        self.cell() 
              
        #Запускаем итератор времени.
        #запускаем генератор события (получаем в ответ дельту времени)
        while True:
            cell = self.ES.GetEvent()
            #print(type(cell))
            #хитрость в том, что когда заканчивается очередь, возвращается None, который не имеет атрибута .go, при попытки его запроса генерируется ошибка AttributeError
            try:
                dt = cell.go() # генератор события                
            except AttributeError:                 
                break
            #user exception block                
            except UException1 as UE1:
                try: 
                    exec(UE1.script)
                except AttributeError:
                    raise AttributeError("set exception script 1")
            except UException2 as UE2:
                try: 
                    exec(UE2.script)
                except AttributeError:
                    raise AttributeError("set exception script 2")
            except UException3 as UE3:
                try: 
                    exec(UE3.script)
                except AttributeError:
                    raise AttributeError("set exception script 3")
            except UException4 as UE4:
                try: 
                    exec(UE4.script)
                except AttributeError:
                    raise AttributeError("set exception script 4")
            except UException5 as UE5:
                try: 
                    exec(UE5.script)
                except AttributeError:
                    raise AttributeError("set exception script 5")
            except UException6 as UE6:
                try: 
                    exec(UE6.script)
                except AttributeError:
                    raise AttributeError("set exception script 6")
            # end
            self.TimeLine.append(dt)
            #запускаем переббор всех интегральных компартментов
            for cmprt in self.MCC:
                self.MCC[self.MCC[cmprt].to].add(self.MCC[cmprt].step(dt))
            exec(self.taktalSlot)       
        exec(self.DC.slot.final)
        et = datetime.datetime.now()
        self.DC.data.calctime = (et-st).total_seconds() 
        #print "finale!"