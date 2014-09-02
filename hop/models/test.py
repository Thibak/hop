# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 16:51:28 2014

@author: user
"""

#########################################################
############# Модель системы кроветсоврения #############
#########################################################
# Гайдлайн по написанию модели
# Описание:
# все функции вызываются как методы класса e. (* точнее e является сущностью класса XMLDriver)

# выполняется внутри calculate выполняемого модуля. Потому в неймспейсе три основных объекта:
#exp -- XMLDriver
#e -- Engine
#DM -- машина данных
 

# Константы должны определяться в виде e.const.имя_константы = значение
# Модель состоит из двух частей: модуль клеточной динамики и блочной модели
# Для описания первого служит система состояний (Condition). Состояние состоит из названия сосоятония клетки и вектора событий (Event).
# для добавления события служит вызов функции
# e.addCondition(name, vec)
# Ивенты выполняются внутри объекта Cell. Значит 

e.addCondition('g1',[Event('np.random.weibull(1)','self.chCond("M")'), Event('np.random.weibull(1)','self.chCond("g0")')])
#e.addCondition('g1',[Event('np.random.weibull(1)','self.division()')])
e.addCondition('g0',[Event('np.random.weibull(1)','self.chCond("g1")')])
e.addCondition('M',[Event('np.random.weibull(1)','self.division()')])
e.setDefCond('g1')
# Каждое событие описывается парой функций: функционал и результат события.
# Формат: [Event('функция','результат'), ...]
# Функционал является случайной функцией возвращающей время до события. Для использования доступны любые алгеброические функции и пр. доступное в библиотеке numpy, в частности рекомендуется использование библиотеки random и np.random, и в частности np.random.weibull
# Управляющие обратные связи работают через сервер обратных связей. О добавлении значений написано ниже, здесь же оговорим возможность использования значения из слотов сервера обратных связей. Слоты возвращают значение в зависимости от подключенного словаря. Обращение к слотам происходит через функцию self.Engine.FB.val(имя слота)
# функционал вычисляется для всех возможных событий, определяется ближайший и закладывается в Сервер Событий, когда приходит время для события, выполняется вторая строка
# Для второй строки доступны следующие функции (не забывать префикс self.):
# - sleep() 
# - division()
# - assymDivision(name) -- имя состояния для второй клетки
# - differentiation(cmprt) -- имя состояния куда переходит клетка
# - apoptosys()
# - toMature()
# Хитрость состоит в том, что действие выполняется по прошествии времени. Например действие sleep, не делает ничего кроме выбрасывания нового времени. Это значит, что клетка "проспола" это время.
# Т.к. управление происходит "изнутри" клетки, вызов происходит с префиксом self.
#
# Кроме того, для использования доступны управляющие события. Т.к. управление происходит "изнутри" клетки, то использовать необходимо абсолютный адресс:
# self.Engine.
#  
# После того, как все состояния созданы, необходимо задать начальное состояние для клеток. e.setDefCond(name)
#  
# Управление сервером обратных связей:
# e.FB.
#  -  addDict(name, dict = {}) -- где dict - словарь, т.е. пары имя_слота:строка_для_выполнения. Имя слота -- имя по которому происходит обращение из событий, строка -- функционал, возвращающий управляющее значение. В общем случае может содержать все, что угодно. В частном предпологается использование сумматоров из компартментов по формату:
# self.MCC[name].n и self.SCC[name].n -- количество клеток в компартменте с таким-то именем. Естественно, возможно суммирование по всем компартментам для списков, какие-то генераторы и пр.
#  -  addSlot(name, dict, string) -- вообще не понятно зачем, т.к. есть общая функция, но для полноты она имеется. Добавляет слот к созданному ранее словарю. Причем если такого нет, то программа вылетает.
# При создании сервера обратных связей автоматически словарем по умолчанию становится пустой словарь default, потому необходимо его переопределить функцией:
# self.Engine.FB.changeDict(имя словаря)
# Добавление псевдособытия
# в основном псевдособытия предназначены для переключения словарей обратных связей, т.е. замена словаря-болванки (начальные значения), рабочей версией обратных связей. Отдельное переключение слотов не пердпологается. 
# Контейнеры у меня крайне умные, и сами добавляется в сервер событий, потому вполне достаточно их создать
# 1. Абстрактный контейнер события (например генерирующий клетку-мутанта) -- EventContainer(Time, st), принимающий на вход время, когда он должен быть выполнен и строку, что собственно он должен сделать.

# 2. стоп-машина StopEvent(Time). Без такого события расчет длится бесконечно. Если клетки не элиминируют естественно. Удобен простотой вызова
# e.
StopEvent(9)
# Блочная часть модели:
# На входе весь граф блоков принимает dt от событийного куска, и производит перерасчет содержимого по формулам внутреннего (internal) и внешнего (transition) перехода. Под внешним переходом подразумевается количество переходящих в to узел графа. Хорошо бы, что бы небыло висячих концов  
# addCompartment(self, name, internal, transition, to):
# Функции для обоих переходов могут зависить от N (объем компартмента) и dt (дельта времени)
#
#
# оказывается это все-таки надо подругому добавлять
#----------------- метаинформация о модели ---------------------
# Что характерно, нижеследующие операции имеют префикс ex. т.к. это команды для драйвера данных. 
# - setIter(iteration): задает количество итерации для одного раунда монтекарло
# - addVScript(script): задает скрипт монтекарловской обработки векторных (множество реализации скаляров) данных
#   в скриптах используются следующие интерфейсы: matrix и vector -- данные для обработки, записывать в data.имя переменной
#
# - addSScript(script): задает скрипт монтекарловской обработки матричных (множество реализации векторов) данных

# о форматировании скриптов стоит написать отдельно
#
#########################################################
e.DC.addDataPoint('t', 'v'),


e.DC.makeFinalCollector('self.DC.data.t = self.TimeLine')
