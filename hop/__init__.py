# -*- coding: utf-8 -*-
"""
@author: russinow
"""
from core import Engine
from xmli import Experiment
from subprocess import call

# Создаем болванку для общедоступности
ex = None

#--------------------------------------
# хелпы:
# два штуки: графика, новый файл

new_task_help =\
"""
Для создания нового задания задайте следующие параметры:
Как префикс используйте ex.
-
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
            pass # перейти в интерактивный режим, вывести хелп по графике
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
            pass # перейти в интерактивный режим, вывести хелп по созданию задания
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
        
     

