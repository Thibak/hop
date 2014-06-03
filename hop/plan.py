# -*- coding: utf-8 -*-
"""
@author: Mikhail Rusinov
"""

import copy
import pickle #загружаем и сохраняем данные
import numpy as np 


class Plan:
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
      
      Задачи: Переделать загрузку дефаулта.
              Освоить итераторы
              все-таки заменить pickle на csv.
      
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
                Решение: Оказывается Pickleзация объекта происходит через сохранение
                (внимание!) СЛОВАРЯ __dict__ в котором хранятся переменные объекта.
                Что мне собственно и нужно. Пишем метод для сохранения и извлечения __dict__
                Работать будет так.  Если нужно загрузить словарь, то создаем пустой объект
                и запускаем метод Load. ВАЖНО сделать предупреждение, что существующий 
                метод обнуляется
                
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
            a = np.arange(start1, stop1, step1)
            b = np.arange(start2, stop2, step2)
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
            a = np.arange(start, stop, step)
            for i in a:
                self.chAttr(name,i)
                self.push()
        else:
            print ('No such name')
    # Подсистема сохранения и извлечения программы эксперимента
    def save(self,name):
        if self.isCalc:
            with open(name + '.rst', 'wb') as f:
                pickle.dump(self.__dict__, f,2)
        else:
            with open(name + '.dic', 'wb') as f:
                pickle.dump(self.__dict__, f,2)
    def load(self,name):
        with open(name, 'rb') as f:
            loaded_dict = pickle.load(f)
            f.close()          
            self.__dict__.update(loaded_dict) 
         