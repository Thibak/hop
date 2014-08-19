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
# функционал вычисляется для всех возможных событий, определяется ближайший и закладывается в Сервер Событий, когда приходит время для события, выполняется вторая строка
# Для второй строки доступны следующие функции:
# - sleep() 
# - division()
# - assymDivision(name) -- имя состояния по умолчанию
# - differentiation(cmprt) -- имя состояния куда переходит клетка
# - apoptosys()
# - toMature()
# Хитрость состоит в том, что действие выполняется по прошествии времени. Например действие sleep, не делает ни чего кроме выбрасывания нового времени. Это значит, что клетка "проспола" это время.
#
#
# setDefCond(self, name):
#
# Compartment = namedtuple ('Compartment', 'int tran')
# addCompartment(self, name, internal, transition, to):
#
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
    