# -*- coding: utf-8 -*-
"""
@author: russinow m a
ReMONA V.1.0
http://russinow.me/
"""
from core import Engine
from core.MOb import StopEvent
from core.AOb import Event
from DataDriver import XMLDriver, DataMachine
from subprocess import call
from code import interact 
from sys import exit, stdout
import datetime
 

# Создаем болванку для общедоступности
ex = None
ex_path  = 'hop/experiments/'
mod_path = 'hop/models/'

#--------------------------------------
# хелпы:
# два штуки: графика, новый файл
new_task_help =\
"""
To create a new task set the following parameters:
Use ex as a prefix.
- setModel(name):
sets the name of the model - the name of file .py with model structure description. Whether the name of the file has .py extension or not, the program automatically makes the name complete. In case the path to the file is not specified directly and only name is given, the program carries out the search in the inner directory ./models; in case there is no such file, the user is advised to create an absolute path to the file or create a file with such name in the inner directory. Many programs of the experiment may refer to one model. Calculations do not alter the program of the experiment. 
- makeMatrix(Xvar, XX, Yvar, YY): creates cartesian product of parameters Xvar*Yvar on vectors XX, YY. Vectors are created by the following procedure
np.arange(start, stop, step)
- makeVec(Xvar, XX): creates a vector on variable Xvar, from vector XX,
XX is set by procedure np.arange(start, stop, step)
A task cannot contain more than one matrix or vector. An attempt to create a new one is blocked. 
- delTask(): However, before the start of calculation, the task can be deleted and a new one created (with the task type changed and parameters iterated)
"""
graph_help =\
"""
The following fuction are avilable for graphic works:
Use ex.plot(VarName, aprType)
"""



new_task_help_ru =\
"""
Для создания нового задания задайте следующие параметры:
Как префикс используйте ex.
- setModel(name):
задает имя модели -- имя файла .py с описанием структуры модели. Имя файла может иметь или не иметь расширения .py, программа автоматически дополняет имя до полного. В том случае если путь к файлу непосредственно не задан, и указано только имя, программа производит поиск во внутренней директории ./models, в том случае, если такого файла нет, пользователю предлагается задать абсолютный путь к файлу, или создать файл с таким именем во внутренней директории. 
На одну модель может ссылаться много программ эксперимента. Расчеты не вносят изменений в программу эксперимента.
- makeMatrix(Xvar, XX, Yvar, YY): создает декартово произведение параметров Xvar*Yvar по векторам XX, YY. Вектора создаются процедурой np.arange(start, stop, step)
- makeVec(Xvar, XX): создает вектор по переменной Xvar, из вектора XX, XX задается процедурой np.arange(start, stop, step)
Задание не может содержать более одной матрицы или вектора. Попытка создания нового блокируется.
- delTask(): Однако до начала расчета задание может быть удалено и создано новое (с заменой типа задачи и итерируемых параметров) 
"""

graph_help_ru =\
"""
Для отрисовки полученных характеристик используйте:
ex.plot(VarName, aprType)
В зависимости от типа эксперимента (варьирование одной или двух характеристик) выводится 2-х или 3-х мерный график зависимости переменной VarName от аргументов. aprType задает тип усреднения полученных значений (задается в скрипте монтекарловской обработки)
""" 
#----- болванка для модели (нуль-модель)
null_model = """
#########################################################
### Модель репликативной мультиобъектной системы ########
#########################################################
# Гайдлайн по написанию модели
# Описание:
# все функции вызываются как методы класса e. (* точнее e является сущностью класса XMLDriver)
# Константы должны определяться в виде e.const.имя_константы = значение
# Модель состоит из двух частей: модуль расчета единичных событий и блочной модели мультиобъектных (массовых) нод
# Для описания первого служит система состояний (Condition). Состояние состоит из идентификатора сосоятония и вектора событий (Event).
# для добавления события служит вызов функции
# e.addCondition(name, vec)
# Каждое событие описывается парой функций: функционал и результат события.
# Формат: [Event('функция','результат'), ...]
# Функционал является случайной функцией возвращающей время до события. Для использования доступны любые алгеброические функции и пр. доступное в библиотеке numpy, в частности рекомендуется использование библиотеки random и numpy.random, и в частности numpy.random.weibull (для подробностей см. документацию по numpy)
# Управляющие обратные связи работают через сервер обратных связей. О добавлении значений написано ниже, здесь же оговорим возможность использования значения из слотов сервера обратных связей. Слоты возвращают значение в зависимости от подключенного словаря. Обращение к слотам происходит через функцию self.Engine.FB.val(имя слота)
# функционал вычисляется для всех возможных событий, определяется ближайший и закладывается в Сервер Событий, когда приходит время для события, выполняется вторая строка
# Для второй строки доступны следующие функции (не забывать префикс self.):
# - sleep() 
# - divide()
# - assymDivide(name) -- имя состояния дочернего объекта
# - reconfigurate(cmprt) -- имя состояния куда переходит объект
# - destroy()
# - toMOC()
# Хитрость состоит в том, что действие выполняется по прошествии времени. Например действие sleep, не делает ничего кроме выбрасывания нового времени. Это значит, что объект "проспал" это время.
# Т.к. управление происходит "изнутри" объекта, вызов происходит с префиксом self.
#
# Кроме того, для использования доступны управляющие события. Т.к. управление происходит "изнутри" объекта, то использовать необходимо абсолютный адресс:
# self.Engine.
#  
# После того, как все состояния созданы, необходимо задать начальное состояние для объектов. e.setDefCond(name)
#  
№
# Управление сервером обратных связей:
# e.FB.
#  -  addDict(name, dict = {}) -- где dict - словарь, т.е. пары имя_слота:строка_для_выполнения. Имя слота -- имя по которому происходит обращение из событий, строка -- функционал, возвращающий управляющее значение. В общем случае может содержать все, что угодно. В частном предпологается использование сумматоров из компартментов по формату:
# self.MCC[name].n и self.SCC[name].n -- количество объектов в компартменте с таким-то именем. Естественно, возможно суммирование по всем компартментам для списков, какие-то генераторы и пр.
#  -  addSlot(name, dict, string) -- вообще не понятно зачем, т.к. есть общая функция, но для полноты она имеется. Добавляет слот к созданному ранее словарю. Причем если такого нет, то программа вылетает.
# При создании сервера обратных связей автоматически словарем по умолчанию становится пустой словарь default, потому необходимо его переопределить функцией:
# self.Engine.FB.changeDict(имя словаря)
# Добавление псевдособытия
# в основном псевдособытия предназначены для переключения словарей обратных связей, т.е. замена словаря-болванки (начальные значения), рабочей версией обратных связей. Отдельное переключение слотов не пердпологается. 
# Контейнеры сами добавляется в сервер событий, потому вполне достаточно их создать
# 1. Абстрактный контейнер события (например генерирующий клетку-мутанта) -- EventContainer(Time, st), принимающий на вход время, когда он должен быть выполнен и строку, что собственно он должен сделать.

# 2. стоп-машина StopEvent(Time). Без такого события расчет длится бесконечно. Если объекты не элиминируют естественно. Удобен простотой вызова
#
# 
# Блочная часть модели:
# На входе весь граф блоков принимает dt от событийного куска, и производит перерасчет содержимого по формулам внутреннего (internal) и внешнего (transition) перехода. Под внешним переходом подразумевается количество переходящих в to узел графа. Хорошо бы, что бы небыло висячих концов  
# addCompartment(self, name, internal, transition, to):
# Функции для обоих переходов могут зависить от N (объем компартмента) и dt (дельта времени)
#
#
#
#----------------- метаинформация о модели ---------------------
# Нижеследующие операции имеют префикс ex. т.к. это команды для драйвера данных. 
# - setIter(iteration): задает количество итерации для одного раунда монтекарло
# - addVScript(script): задает скрипт монтекарловской обработки векторных (множество реализации скаляров) данных
# - addSScript(script): задает скрипт монтекарловской обработки матричных (множество реализации векторов) данных
#########################################################

"""


#----- блок работы с файлом -----  

def load(filename):
    global ex
    if '/' not in filename:
        filename = ex_path + filename
    try:
        ex = XMLDriver(filename)
    except IOError:
        print('No file with such name\n')
        yn = raw_input("Would you like to create a file with this name? \n(y/n):")
        if   yn in 'yYуУyesдД':
            new(filename)
        else:
            print('Shutting down.')
            exit()


def start():
    global ex
    """
    Запускаем рассчет по программе эксперимента
    """
    if ex == None:
        print("""
        XML file not loaded. Please load or make new
            - load(filename)
            - new()        
        """)
    elif ex.status() == 'complete':
        print ex
        yn = raw_input("Calculation complete. Would you like to load interactive shell?\n(y/n):")
        if   yn in 'yYуУyesдД':
            print graph_help
            interact(local=dict(globals(), **locals()))
            #interact(local=locals()) # перейти в интерактивный режим, вывести хелп по графике
        elif yn in 'nNNoxXexitquitqQ':
            return
        else:
            print("Something's wrong. Shutting down.")
    elif ex.status() == 'progress':
        print ex        
        yn = raw_input("Calculation complete at " + str(ex.progress()) + "%, would you like to continue calculation?\n(y/n/number of iterations):")
        # селектор
        if   yn in 'yYуУyesдД':
            calculate(ex)# начать выполнение
        elif yn in 'nNNoxXexitquitqQ':
            return
        else:
            try: 
                n = int(yn)
                if n<0:
                    raise SyntaxWarning
            except SyntaxWarning:
                print ('the number of operations cannot be less than zero')
                #break
            except ValueError:
               print("Something's wrong. Shutting down.") 
            else:
                calculate(ex,n)# начать выполнение
            
    elif ex.status() == 'Null':
        print ex
        yn = raw_input("It's just a dummy. Would you like to make a task?\n(y/n):")
        # селектор
        if   yn in 'yYуУyesдД':
            print new_task_help 
            interact(local=dict(globals(), **locals()))
            # перейти в интерактивный режим, вывести хелп по созданию задания
        elif yn in 'nNNoxXexitquitqQ':
            return
        else:
            print("Something's wrong. Shutting down.") 
                

    elif ex.status() == 'task':
        print ex
        yn = raw_input("Task file, would you like to start calculation?\n(y/n/number of iteration/e):")
        # селектор
        if yn in 'eEЕеedit':
            print new_task_help 
            interact(local=dict(globals(), **locals()))
        elif yn in 'nNNoxXexitquitqQ':
            return
        elif   yn in 'yYуУyesдД':
            calculate(ex)# начать выполнение
        else:
            try: 
                n = int(yn)
                if n<0:
                    raise SyntaxWarning
            except SyntaxWarning:
                print ('the number of operations cannot be less than zero')
                #break
            except ValueError:
                print("Something's wrong. Shutting down.")  
                #break
            else:
                calculate(ex,n)# начать выполнение
    else:
        print ex
        yn = raw_input('Something is wrong. Try another file or correct this one by hand\n edit/check/exit: (e/c/x)')
        if   yn in 'eEЕеedit':
            call("notepad "+ str(ex.filename))
        elif yn in 'cсCСcheck':
            call(str(ex.filename))
        elif yn in 'nNNoxXxitquitqQ':
            return
        else:
            print("Something's wrong. Shutting down.") 

def new(filename):
    global ex
    if '/' not in filename:
        filename = ex_path + filename
    ex = XMLDriver()
    ex.new(filename)
    print new_task_help






     
     
# Итератор рассчета
def calculate(exp, n = float('inf')):
    # проверка статуса модели 
    #примерная структура вычислителя:
#1. загружаем файл структуры модели
    # а вернее компилируем, т.к. в течении запуска надо каждый раз обновлять его
    print('Loading model...')
    model = compile(open(exp.modelFN).read(),exp.modelFN,'exec') 
    exp.loadScript()
    if n > exp.remain: n = exp.remain
    #ВНИМАНИЕ!! После компиляции содержимое файла уже не модифицируется, т.ч. надо это учесть при итерировании
#2. загружаем параметры модели (таск) ПЕРВЫЙ ЦИКЛ 
    # т.е. загружаем его как текущую задачу для данного эксперимента
    st = datetime.datetime.now()
    print('Start at '+ str(st))
    tottime = (st-st).total_seconds()
    taskdone = 0
    while n != 0:
        n -= 1
        try:
            st = datetime.datetime.now()
            print('\ncalculating: ' + str(n+1) + ' task left')
            exp.LoadTask() 
    #3. формируем монтекарловские переменные
            # МК переменные вытаскиваются из модели, это значит делаем это циклом
            # нулевой цикл, для определения имен переменных в ДатаКоллекторе
            DM = DataMachine()
            DM.LoadScripts(exp) # загружаем скрипты 
            e = Engine()
            # НЕ запускаем модель, а только загружаем, для опрпделения типов, можно сделать стоп с нулевым временем....
            exec(model,dict(globals(), **locals()))
            #e.start()
            
            # запускаем сортировщик
            DM.AnalizeModel(e.DC.dict())
        #4. формируем монтекарловский цикл
               
            for MKiter in range(exp.iterations):
                stdout.write("\r" + 'calculating iteration ' + str(MKiter+1) + ' out of ' + str(exp.iterations))
        #5. создаем ядро
                e = Engine()
                # запускаем модель
                exec(model,dict(globals(), **locals()))#<-- загружаем в локальный неймспейс
                
                # Догрузка итерируемых параметров, а на самом деле перегрузка.
                e.const.__dict__.update(exp.loadConst())
                
        #7. запускаем расчет
                e.start()
        #8. останов расчета по критерию (реализован через exception)
                #сбор данных
                DM.addData(e.DC)
            et = datetime.datetime.now()
            deltatime = (et-st).total_seconds()
            tottime += deltatime
            taskdone += 1
            ovtime = tottime/taskdone
            stdout.write("\r" + 'Complete.                              \nIt took ' + str(deltatime) + ' sec.\n')
        #9. подсчет монтекарловских величин
            print ('expected time of complition: ' + str(datetime.datetime.now() + datetime.timedelta(seconds = ovtime*(n+1))))
            DM.CollapseData()  
            DM.PushData(exp)      
        except IndexError:
            print "No more tasks, load interactive shell..."
            print graph_help
            interact(local=locals())
        
    print ('\nCalculation complit at:      '+ str(datetime.datetime.now()) + '\nTotal time '+ str(tottime) + ' sec.' )
    try:
        exp.LoadTask() # пытаемся подгрузить последнюю задачу, если расчет закончен (нет тасков), то автоматически помечается как законченый файл данных, если нет, то ни чего не меняет.
    except IndexError:
        print "No more tasks, load interactive shell..."
        print graph_help
        interact(local=locals())
        #except:
        #    print "somthing wrong."
    #10. конец
    