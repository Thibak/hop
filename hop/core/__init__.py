# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:29:06 2014

@author: russinow

Ядро расчетов. 
- 1. Сервер событий. Не объект, как ни странно.


"""

# пока просто тмпорт, а вобще-то надо только определенные функции
import MOb
from MOb import cell
from MOb import SCC
from AOb import EventServer
from AOb import Event

# Главный объект

class Engine:
    """
    
    """
    def __init__(self):
        # создаем ссылку на класс клеток внутри Движка
        self.cell = cell
        # Добавляем пустой словарь для состояний клетки (новая формация для структуры)
        self.cell.conditions = {}
        # Создаем экземпляр Сервера Событий
        self.ES = EventServer()
        #Закладываем ссылку на сервер событий с целью прямой закладки
        self.cell.ES = self.ES        
        # 
        self.SCC = {}
        self.cell.SSC = self.SCC        
        #Куммулятивные показатели
        self.MCC = []
        
        

    def addCondition(self, name, vec):
        """
        Формат словаря --
        Имя состояния : вектор объектов-дуплетов -- Ивентов (namedtuple)
        индекс: функция-исход
        Для внутренних обработок достаточно пары имяСостояния-индекс. Я никак не буду оперировать индексом кроме как для хранения на этапе выполнения
        """
        self.cell.conditions[name] = vec
        
     #   тут надо создавать слоты для оценки количества клеток в состояниях
        self.SCC[name] = SCC()
        
    def setDefCond(self, name):
        if name in self.cell.conditions:
            self.cell.defCon = name
        else:
            return 0



    def start(self):
        # создаем первую клетку, ставим состояние по умолчанию
        StartCell = self.cell() 
        #StartCell.
        #Запускаем итератор времени.
        #запускаем генератор события (получаем в ответ дельту времени)
        #MakeEvent(StartCell,)
        
    def tik(self):
        """
        Сначала запускаем такт ивентсервера, откуда получаем длину шага времени
        записываем длину шага времени
        запускаем объекты принимающие шаг времени.   
        """
        #получить длну такта
        e = self.ES.GetEvent()
        #if e == None:
        #    пораждаем конец расчета
        #else:
        #    e.
        #использовать длину такта
        #ES.deltaT
