# -*- coding: utf-8 -*-
"""
@author: russinow m a
ReMONA V.1.0
http://russinow.me/

Ядро расчетов. 

"""
import datetime

from MOb import EventContainer
from MOb import Object
from MOb import SOC
from MOb import MOC
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
    Движок расчетов
    """
    const = Y()
    def __init__(self):
        # создаем ссылку на класс Объектов внутри Движка
        self.Object = Object
        EventServer.Engine = self
        FeedBackSever.Engine = self
        EventContainer.Engine = self
        DataCollector.Engine = self
        
        # Добавляем пустой словарь для состояний Объектов (новая формация для структуры)
        # Создаем экземпляр Сервера Событий
        self.ES = EventServer()
        self.FB = FeedBackSever()
        self.DC = DataCollector()
        self.DC.addDataPoint('calctime', 's'),

        self.SOC = {}
        self.Object.SOC = self.SOC        
        self.MOC = {}
        self.Object.MOC = self.MOC 
        
        #Куммулятивные показатели
        self.TimeLine = []
    
        #пустой слот -- заглушку тактовому сборщику данных.
        self.taktalSlot = compile('','<string>','exec')     

    def addCondition(self, name, vec):
        """
        Формат словаря --
        Имя состояния : вектор объектов-дуплетов -- Ивентов (namedtuple)
        индекс: функция-исход
        Для внутренних обработок достаточно пары имяСостояния-индекс. 
        """

        self.SOC[name] = SOC()
        self.SOC[name].vec = vec
        # слоты для оценки количества клеток в состояниях
        
        
    def setDefCond(self, name):
        if name in self.SOC:
            self.Object.defCon = name
        else:
            raise Exception('setDefCond: no such Condition')

    def addCompartment(self, name, internal, transition, to):
        """
        name -- имя компартмента
        internal -- функция от N и dt изменения внутреннего сосотояния
        transition -- функция от N и dt перехода
        to -- куда??
        """
        self.MOC[name] = MOC(internal, transition, to)

    def start(self):
        """
        Сначала запускаем такт ивентсервера, откуда получаем длину шага времени
        записываем длину шага времени
        запускаем объекты принимающие шаг времени.   
        """
        # создаем первый объект, ставим состояние по умолчанию
        st = datetime.datetime.now()
        self.Object() 
              
        #Запускаем итератор времени.
        #запускаем генератор события (получаем в ответ дельту времени)
        while True:
            Object = self.ES.GetEvent()
            #хитрость в том, что когда заканчивается очередь, возвращается None, который не имеет атрибута .go, при попытки его запроса генерируется ошибка AttributeError
            try:
                dt = Object.go() # генератор события                
            except AttributeError:     
                self.TimeLine.append(self.ES.deltaT)
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
            for cmprt in self.MOC:
                self.MOC[self.MOC[cmprt].to].add(self.MOC[cmprt].step(dt))
            exec(self.taktalSlot)       
        exec(self.DC.slot.final)
        et = datetime.datetime.now()
        self.DC.data.calctime = (et-st).total_seconds() 
        #print "finale!"