# -*- coding: utf-8 -*-
"""
@author: russinow
"""
from core import Engine
from xmli import Experiment
from subprocess import call
from code import interact 

# Создаем болванку для общедоступности
ex = None

#--------------------------------------
# хелпы:
# два штуки: графика, новый файл

new_task_help =\
"""
Для создания нового задания задайте следующие параметры:
Как префикс используйте ex.
- MakeMatrix
-
-

"""

graph_help =\
"""
Для работы с графикой доступны следующие функции:
Как префикс используйте ex.
-
-
-

""" 
#----- болванка для модели (нуль-модель)
null_model = """
#########################################################
############# Модель системы кроветсоврения #############
#########################################################
# Описание:
# все функции вызываются как методы класса e. (* точнее e является сущностью класса Experiment)
# Модель состоит из двух частей: модуль клеточной динамики и блочной модели
# Для описания первого служит система состояний (Condition). Состояние состоит из названия сосоятония клетки и вектора событий (Event).
# для добавления события служит вызов функции
# e.addCondition(name, vec)
# Каждое событие описывается парой функций: функционал и результат события.
# Формат: [Event('функция','результат'), ...]
# Функционал является случайной функцией возвращающей время до события. Для использования доступны любые алгеброические функции и пр. доступное в библиотеке numpy, в частности рекомендуется использование библиотеки random и numpy.random, и в частности numpy.random.weibull
# Управляющие обратные связи работают через сервер обратных связей. О добавлении значений написано ниже, здесь же оговорим возможность использования значения из слотов сервера обратных связей. Слоты возвращают значение в зависимости от подключенного словаря. Обращение к слотам происходит через функцию self.Engine.FB.val(имя слота)
<----может быть стоит сделать какие-то шортхенды для этого 
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
№
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
#
# 
# Блочная часть модели:
# На входе весь граф блоков принимает dt от событийного куска, и производит перерасчет содержимого по формулам внутреннего (internal) и внешнего (transition) перехода. Под внешним переходом подразумевается количество переходящих в to узел графа. Хорошо бы, что бы небыло висячих концов  
# addCompartment(self, name, internal, transition, to):
# Функции для обоих переходов могут зависить от N (объем компартмента) и dt (дельта времени)
#
#
#########################################################

"""


#----- блок работы с файлом -----  

def load(filename):
    global ex
    try:
        ex = Experiment(filename)
    except IOError:
        print('No such file')

def start():
    global ex
    """
    Запускаем рассчет по иксемелю
    Вначале каждого варианта надо выводить информацию о файле, полную.
    """
    if ex == None:
        print("""
        Experiment not loaded. Please load or make new
            - load(filename)
            - new()        
        """)
    elif ex.status() == 'complete':
        print ex
        yn = raw_input("Расчет завершен. Прейти в интерактивный режим для построения графики?\n(y/n):")
        if   yn == 'y' or 'Y' or 'у' or 'У' or 'yes' or 'д' or 'Д' or '':
            print graph_help
            interact(local=locals()) # перейти в интерактивный режим, вывести хелп по графике
        elif yn == 'n' or 'N' or 'No' or 'x' or 'X' or 'exit' or 'quit' or 'q' or 'Q':
            return
        else:
            print('Что-то не то. Закрываюсь.')
    elif ex.status() == 'progress':
        print ex        
        yn = raw_input("Расчет завершен на " + str(ex.progress()) + "%, продолжить расчет?\n(y/n):")
        # селектор
        if   yn == 'y' or 'Y' or 'у' or 'У' or 'yes' or 'д' or 'Д' or '':
            pass# начать выполнение
        elif yn == 'n' or 'N' or 'No' or 'x' or 'X' or 'exit' or 'quit' or 'q' or 'Q':
            return
        else:
            print('Что-то не то. Закрываюсь.')
    elif ex.status() == 'Null':
        print ex
        yn = raw_input("Это только заготовка, Вы хотите создать задание?\n(y/n):")
        # селектор
        if   yn == 'y' or 'Y' or 'у' or 'У' or 'yes' or 'д' or 'Д' or '':
            print new_task_help            
            interact(local=locals()) # перейти в интерактивный режим, вывести хелп по созданию задания
        elif yn == 'n' or 'N' or 'No' or 'x' or 'X' or 'exit' or 'quit' or 'q' or 'Q':
            return
        else:
            print('Что-то не то. Закрываюсь.')

    elif ex.status() == 'task':
        print ex
        yn = raw_input("Задание на расчет. Начать выполнение?\n(y/n):")
        # селектор
        if   yn == 'y' or 'Y' or 'у' or 'У' or 'yes' or 'д' or 'Д' or '':
            pass# начать выполнение
        elif yn == 'n' or 'N' or 'No' or 'x' or 'X' or 'exit' or 'quit' or 'q' or 'Q':
            return
        else:
            print('Что-то не то. Закрываюсь.')
    else:
        print ex
        yn = raw_input('Что-то не то... Попробуйте другой файл, или поправьте этот вручную\n Поправить вручную/посмотреть/выйти: (e/c/x)')
        if   yn == 'e' or 'E' or 'Е' or 'е' or 'edit':
            call("notepad "+ str(ex.filename))
        elif yn == 'c' or 'с' or 'C' or 'С' or 'check':
            call(str(ex.filename))
        elif yn == 'x' or 'х' or 'X' or 'exit' or 'quit' or 'q' or 'Q':
            return
        else:
            print('Что-то опять не то. Закрываюсь.')

def new(filename):
    global ex
    ex = Experiment()
    ex.new(filename)
    print new_task_help
        
     
# Итератор рассчета
def calculation(exp):
    # проверка статуса модели 
    #примерная структура вычислителя:
#1. загружаем файл структуры модели
    # а вернее компилируем, т.к. в течении запуска надо каждый раз обновлять его 
    model = compile(open(exp.modelFN).read(),'model','exec') 
    #ВНИМАНИЕ!! После компиляции содержимое файла уже не модифицируется, т.ч. надо это учесть при итерировании
#2. загружаем параметры модели (таск) ПЕРВЫЙ ЦИКЛ 
    # т.е. загружаем его как текущуий таск для данного эксперимента
    exp.LoadTask() # <--- НЕ ЗАБЫТЬ, что тут надо делать трай, т.к. обработка идет до эксепшена, вырабатываемого этой функцией. Т.е. while True, do.
#3. формируем монтекарловские переменные
    # МК переменные вытаскиваются из модели, это значит делаем это циклом
#4. формируем монтекарловский цикл
    for MKiter in range(exp.iterations):
#5. создаем ядро
        e = Engine()
        # запускаем модель
        exec(model,locals())#<-- загружаем в локальный неймспейс
        
#6. загружаем модель, характеристики модели
#7. запускаем расчет
#8. останов расчета по критерию (какому? Допилить в ядре. Прописывается в модели, кстати)
#9. подсчет монтекарловских величин
#10. конец
    