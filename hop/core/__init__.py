# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:29:06 2014

@author: russinow

Ядро расчетов. 
- 1. Сервер событий. Не объект, как ни странно.


"""
from MOb import EventContainer
from MOb import cell
from MOb import SCC
from MOb import MCC
from AOb import EventServer
from AOb import Event
from MOb import RoutineEvents
from AOb import FeedBackSever

# Главный объект

class Engine:
    """
    
    """
    def __init__(self):
        # создаем ссылку на класс клеток внутри Движка
        self.cell = cell
        self.cell.Engine = self
        EventServer.Engine = self
        FeedBackSever.Engine = self
        EventContainer.Engine = self
        #self.EventContainer = EventContainer
        # Добавляем пустой словарь для состояний клетки (новая формация для структуры)
        # Создаем экземпляр Сервера Событий
        self.ES = EventServer()
        self.FB = FeedBackSever()
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
        self.MCC[name] = MCC()
        self.MCC[name].internal = internal
        self.MCC[name].transition = transition
        self.MCC[name].to = to

    def start(self):
        """
        Сначала запускаем такт ивентсервера, откуда получаем длину шага времени
        записываем длину шага времени
        запускаем объекты принимающие шаг времени.   
        """
        # создаем первую клетку, ставим состояние по умолчанию
        # как ни странно, ни чему не надо ее присваивать, Т.к. клетка делает все сама.
        self.cell() 
                
        #Запускаем итератор времени.
        #запускаем генератор события (получаем в ответ дельту времени)
        while True:
            cell = self.ES.GetEvent()
            try:
                dt = cell.go() # генератор события
            except AttributeError:
                break
            else:
                self.TimeLine.append(dt)
                #запускаем переббор всех интегральных компартментов
                for cmprt in self.MCC:
                    self.MCC[self.MCC[cmprt].to].add(self.MCC[cmprt].step(dt))
