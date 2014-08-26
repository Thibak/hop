﻿hop
===

hematopoiesys on Python

Архитектура библиотек питона диктует двухуровневую иерархизацию. Т.е. в любом случае есть пакет, и есть егоо муодули. Из модулей мы можем подгружать функции. Однако, в __init__.py есть возможность прописать прямой импорт класса

После паузы приходится пересмотреть архитектуру. Ряд основопологающих моментов:
 - для хранения задач и результатов более целесообразным выглядит использование XML, более гибкий, а главное редактируемый вручную!
 - В каждом файле хранится описание объектов и объекты. Причем в описании в частности хранится ход прогресса. Т.е. через один файл реализуется возможность 
	- восстановления упавшего в ходе рассчетов результата
	- реализация параллелизма и блокировки 
	- PROFIT
 - в связи с этим новая архитектура должна выглядеть следующим образом:
 - HOP
	- __init__.py
	- __mine__.py
    - core - библиотека, т.е. просто папка, в ней все связанное непосредственно с рассчетами.
        Мейнидея такой структуры такая, что все, что не вызывается извне должно лежать в специальных либах.  
        - __init__.py -- то, что непосредственно ядро, и то, что вызывается из скрипта 
            - Engine -- собственно вся система. Запускается с параметрами определяющими работу системы.  
            Движок имеет три части, 
            1. подготовка структуры модели
            2. препрогонка с фиксированными обратными связями
            3. расчет.
                - события генерирующие шаг времени, т.е. шаг ивентсервера
                - события принимающие шаг времени.
        - MOb.py -- Modell Objects -- объекты собственно модели
            - Cell -- 
              - SetEventTime() -- кладем время до события
              - EventTime() -- время до события  
              - PerformEvent() -- выполнить событие. 
        - AOb.py -- Auxiliary Objects -- вспомогательные объекты
            - EventServer
                - GetEvent
                - MakeEvent

Мысль 0. По большому счету я могу не прописывать компартменты, а только правила
Тогда создание инфраструктуры задача анализватора правил
         

На данный момент сервер событий организован в виде самоосортирующейся очереди (после вставки нового элемента)
Хотя надо переписать, что бы сортировка производилась перед возвращением элемента, возможно, это экономичней
Вся информация хранится в самой клетке, и о том что должно произойти и о том когда. 

Переделка на будущее: дело в том, что во время ожидания в очереди ситуация изменяется,
и она может влиять на скорость процессов. Отсюда необходимость делать поправку очереди.
Однако можно делать ленивый пересчет не после каждого такта, а только тогда,
когда среднее (минимальное?) время поправки превосходит зазоры в очереди. (это делается легко)
Кроме того, можно делать два стека событий и сортировать отдаленные редко, а потом забирать оттуда положим сотнями.
Но тут не вполне понятно как делать поправку.

	- xml - интерфейс взаимодействия с памятью т.е. с XML 
		- пространство допустимых имен и их атрибутов. Строится фабрика создающая конкретный элемент. Т.е. по функции запичвающей каждый вид данных. Фабрика сосздает элементы фиксированной структуры. Для набирания бус, используется .append, который вставляет В тег. *
		- интерфейсы ввода
			- создания структуры данных
			- сохранения данных
				- метаинформации
				- экспериментов, в каком-то виде
		- интерфейсы вывода
			- чтения данных
				- метаинформации
				- обратной функции чтения данных
	- TaskServer - сервер задач. Наверное, надо прописывать его импорт прямо в ините. Не смог найти запуск библиотеки как приложения. Осуществялется это через __main__.py в котором прописывается запуск всех нужных модулей, и сервера соответственно
	- graph.py - модуль вывода графической информации
	- interface.py - совокупность интерфейсов -- ВОПРОС. надо ли оно мне

Общая архитектура:
Импортируем HOP в скрипт, выполнение скрипта и есть работа приложения. 
Скрипт делится на части, можно при запуске HOP спрашивать где, и создавать файл-шаблон.
Скрипт представляет собой последовательность процедур по определенному правилу.
Надо придумать как проверять правильность написанного скрипта. Какой-то препроцессор.
Часть 1. Описание архитектуры
    Создание связей между компартментами
    Задание правил предпрогонки
Часть 2. Препрогонка
    Блокировка изменения архитектуры модели, 
    запуск ивент-сервера, итератора и пр. на препрогонку
Часть 3. Собственно расчет.
Часть 4. Сохранееие, Вывод

#-----------------
Важная мысль. Так как мы можем на лету добавлять атрибуты и методы класса, то вызов метода addCondition вызывает модификацию класса Cell, в который мы добавляем условия.
Однако, эксперименты показали, что модификация одной сущности вызывает модификацию другой и самого класса.
Чем это хорошо -- хранится ссылка на объект, а значит не забивается память, модификация отражается на всех сущностях.
#-----------------

Попробую описать проблему.
как работает сейчас:
    1. объект Условия -- словарь с доступом по имени условия, и вектором исходов (ивентов)
    создается в движке, передается ссылка в клетку <-- надо так
    2. Объект Компартменты -- словарь с доступом по имени компартмента (читай условия) и цифрой-количеством клеток
    создается в прототипе клетки?? 

Что хоцца -- собрать в один объект. Объект словрь? Нет. А что? Ответка словаря. Это объект-компартмент, представлет собой объединение 1 и 2, т.е. ...

ВНИММАНИЕ!!
Eval vs exec

Первичный этап работает нормально. т.е.
    Взаимодействие ивент-сервера
    стволовые клетки
    добавление на лету состояний клетки
    Выполнение функций времени
    запуск результата по прошествии времени
    автогенератор компартментов СКК
    Итератор
    система компартментов
        для созревающих/зрелых клеток -- 
            добавление функций (сделать по подобию такой же системы для стволовых клеток)
            выполнение оного
    переход стволовые-созревающие
    инфраструктура архитектуры 
        результаты действий!!
    Метасобытия
        абстрактный контейнер события
        инфраструктура метасобытий
    сервер обратных связей....
    двойной механизм работы
    перепилить ссылки внутри объектов. 
        Пояснение: после создания основного контейнера Engine, необходимо всем используемым классам передать ссылку на него. Тогда все дочки будут иметь доступ друг к другу. После этого создать объекты-дочки.
    Прописать структуру итема и интерфейс закладки параметров туда
    функция-генератор элемента задача.
    Функция 
    Управляющая система:
        сохранение созданного эксперимента, бинд к цсв
            имя файла архитектуры модели
            досчет, прогресс
    допилить загрузку файла, автоматическое определение статуса и необходимых переменных
    Для обеспечения обратной совместимости, загрузка файла должна происходить с группой траев. По результатам выводится отчет о статусе файла, а он и так выводится УПшкой, можно просто запиливать что-то типа: subj loaded \n
    Я понаписал каких-то хитростей с 
     1.	 абстракт ивентами, т.е. надо рассмотреть механизм его создания и добавления в ивент сервер, а так же форматы действий -- сменить словарь ивентсервера - основной механизм, вызывается специальной функцией ивентсервера, с селфом его сущности. Т.к. вызов происходит после создания сущности, надо вызывать метод сущности (посмотреть имя сущности)
     2.	 Форматы указателей на самого себя в екзекьютах, селф ли, имя сущности ли, передавать ли в екзекьюте ли указатель на локальный словарь ли? -- думаю, требует непосредственных экспериментов.
     3.	 Фидбек сервер. Формирование сл оваря, форматы указателей, заглушки?
     Пока так.
    форматы сумматоров для фидбека 
    запилить прекомпиляцию на все строки
    запуск расчета

            значения, диапазоны значений
            собираемые показатели -- видимо следует собирать все
    как собирать выходные значения
    Написать класс обработки и хранения данных. В частности их пуш в память
    разобраться как вынимать данные после скриптовки
    монтекарловские итераторы, характеры усреднения
    имена итерируемых параметров
    хелп для таска
    создать метод удаления задания
    добавить константы в сервер
    закидывать таймлайн в метаинформацию <--- больше НИКОГДА не писать такой ерунды!
    итерирование по итемам. Связано с частичным расчетом
    переименовать XMLI во что-то вразумительное.
    Догрузка параметров  => итерирование... 
    хелп по новой задаче
    Разобраться с путем хранения.
    запуск как приложения

Далее:    

    Следующее реализуется через систему ексепшенов:
        условный останов. Реализуется через эксепшены. 
        условия остановки в специальную переменную
    взаимодействие с матплотлибом? Вторичное формирование?     
    дописать хелпы графике
    описание формирования скриптов обработки

Далее:
    
    дописать метод блокировки модели (а вернее вытягивания копии в XML)
    Хорошо бы сделать систему проверки целостности модулей.
    производительность и примерное время рассчета. Крайне полезная фича была бы.
    оптимизировать работу сервера обратных событий. Пока переключаются только словари, но нет возможности переключать отдельные переменные.
--------------------------------
Ясно, что реализовываать условный останов надо через ексепшены. Их легко сортировать и вылавливать. Однако! Как их добавлять, и как делать проверки? 
Вариант: предоставить модельеру возможность использовать их в любом месте. В частности в юзердефаинд ивентах.
Ну и сделать соответствующий набор ексепшенов и их вылавливалку. По большому счету этого достаточно

Выяснилось следующее:
class a(Exception): 
    def __init__(self, p):
        self.p = p
def b(): raise a('point') 
def c(): b()    
def d(): c()   
    
try: d()
except a as f: print f.p

Что значит, что механизм ексепшенов можно крайне гибко использовать дле передачи ЛЮБОЙ информации из любого места. Главное поставить обработчик на выходе.
--------------------------------
Куда складывать константы? Надо бы наверное единое хранилище. Но другой вопрос зачем... Можно и протсо определять.
Догрузка различна для вектора и матрицы. Видимо надо прописывать специальную функцию
Для того, что бы было понятно в каком неймспейсе они существуют, проще всего прописать их как поле самого Движка. Тогда понятно что моифицировать.
--------------------------------
Для монтекарловской обработки нужен скрипт. 
Функции скрипта (а вернее двух) и скорее всего хранящегося в XML-e, как в общем обработчике, применяться ко всем (вниание! Без привязки к конкретному значению, а только к типу) ко всем скалярам/векторам в зависимости от типа. Что-то типа лямбды, штоле...

***
лямбда в каком-то смысле работает как eval. 
***

После каждого раунда скрипт должен применять полученное значение к накапливаемому. Тут подумать. 
Кажется все-таки не после каждого раунда, а к массивам, которые формируются путем прибавления результатов из каждого раунда. А потом все затирать.

Вопрос, в том, что можно вообще все содержимое __dict__ запиливать, а можно делать разбор по ходу, вот и думай.

--------------------------------
Основная проблема состоит в том, что данные могут быть скалярными, векторными и интегральными. Например, общая продукция, или потактовая продукция, или кумулятивная продукция.
По последним соображениям самым рациональным является следующее решение:
Имеем объект-сборщик информации (ОСИ), специальными методами в нем реализуется 4 возможных случая:
 - периодический
 - конечный
 - потактный
 - событийный
Для реализации периодического прописывается вспомогательный потомок событийного контейнера (который реализует что? м.б. просто контейнеры создавать) Метод ОСИ создает серию ивентов с заданной периодичностью до стоп-машины. Куда и что прописывается передается в качестве строки
А может быть создавать опять же слоты, которые запускать теми или иными способами. Так удасться достигнуть большей нибкости и лаконичности
Конечный сборщик вызывается один раз после окончания раунда. 
ВАЖНО. К конечным методами относятся постобработчики сериализованных данных. 
Потактный сборщик самый спорный, т.к. добавление дополнительных рассчетов обременяет вычисления, а при росте объема колонии объем вычислений растет пропорционально (не квадратично!! Т.к. прямого взаимодействия между клетками нет, что не может ни радовать)
Единственным способом работы потактового сборщика является его вызов... wait a moment!! вызов... ПОТАКТНО! т.е. при каждом вызове ивента попутно вызывается метод сборщика
Для снижания наклодных расходов, т.е. в том случае, когда пользователю таки не нужен потактовый сбор можно вызывать какой-то нуль-метод. Т.е. ссылку на пустой метод. def localFunc():pass, на рабочей машине вызов такой функции занимает 0.85*10**(-7)

Что тестится следующей процедурой

import datetime
 
def localFunc():pass

def testCall(f):
  st = datetime.datetime.now()
  for x in xrange(10**7): f()
  et = datetime.datetime.now()
  return (et-st).total_seconds()
  
testCall(localFunc)

*** пометка, что замена функции на a=1 или a=1+1 вообще не изменяет скорости вычисления. Зато перевызов другой пустой функции линейно (ПРОВЕРИТЬ!!!) увеличивает время, что значит, что это время необходимое на вызов. Это говорит о том, что данный метод вообще может быть оценочным для быстродействия
Холостой вызов занимает 0.15, т.е. накладные расходы на итерирование. Арифметическое сложение занимает дополнительно где-то 0.05 
Большая беда состоит в том, что вызов через exec замедляет выполнение (pass) в 40 раз

Если такой метод все-таки нужен, то мы просто приписываем вместо болванки вызов слота сборщика  

событийный сборщик самый непонятный, и накладной, т.к. надо как-то вытаскивать тип события, необходимость же является наиболее спорной. Более перспективным видится создание каскада событий (в случае такой необходимости) с участием суррогатного пустого состояния, вызывающего слот сборщика 

Важно понимать, сто после окончания раунда вся инфа затирается, если она не сохранена. 


Итак, что получается: 
ОСИ должен иметь ряд слотов, которые представляют собой совокупность методов записывающих в сущность ОСИ (а точнее его data структуру) данные. Кроме того должны быть методы генерирующие и организующие слоты. В сущности, это все.

Вопрос, надо ли заранее объявлять данные? Ну видимо надо

Я умею делать всякие экзерсисы с автодополнением полей и словарей. Можно на этом объекте потренироваться нормальной архитектуре такого рода. Фактически это экранирование от пользователя. Хотя это правильный и перспективный подход

--------------------------------
Сумматоры для фидбека, есть суть опрашиваемые компартменты, причем по единому интерфейсу для стволовых и для созревающих клеток, что осуществляется через AbstractCompartment, от которого наследуются оба класса компартментов
--------------------------------
нуль-модель:
    надо прописать генератор нуль-модели -- болванки с хелпом
--------------------------------
примерная структура вычислителя:
1. загружаем файл структуры модели
2. загружаем параметры модели (таск)
3. формируем монтекарловские переменные
4. формируем монтекарловский цикл
5. создаем ядро
6. загружаем модель, характеристики модели
7. запускаем расчет
8. останов расчета по критерию (какому? Допилить в ядре. Прописывается в модели, кстати)
9. подсчет монтекарловских величин
10. конец

--------------------------------
Предположение по архитектуре управляющего модуля.
необходима реализация 2-х режимов работы:
 - создание/редактирование эксперимента
 - выполнение эксперимента, доделка результатов

Первое может быть реализовано в виде импорта либы в интерактивный режим Самого Питона
Второе запускается как скрипт или специальной процедурой. В майне прописывается чтение строки параметров
    майн -- отдельный файл, в который мы делаем from hop import из инита хопа, где распологается управляющая функция (Кажется, что не класс.)

XML:
F.root( 
    meta(modelFN = , iteration = , TaskType = (M/V), status = (Null/task/progress/complete)
        time(CreationTime = 
            )
        *matrix(
            x( name = 
                vectorized X-mtrx
                )
            y( name = 
                vectorized Y-mtrx                
                )
            )
        *vec()
        )
    tasks(
        *vtask(i = , x = 
            )
        *mtask(i = , j = , x = , y = 
            )
        ...
        )
    data(
        item()
        ...
        )
    )

Список доступных атрибутов:
    имя файла архитектуры модели
    кол-во итераций (или другое условие?, например достижение некоей точности? Тогда прописываем это в задание)
    
М.б. имеет смысл иметь в атрибутах меты описание структуры задания (т.е. матрица/вектор), для организации селектора парсера.

    основным рабочим элементом является фабрика. Вопрос, где его создовать. 
Преддожение-ответ:
При загрузке модуля создаем фабрику, в фабрике формируем дочерние элементы. Нет. Плохой вариант. Такое должно создаваться только при создании нового конструкта. При загрузке мы ничего не создаем, но загружаем.
Функция  new должна создавать в точности точно такой же конструкт, как load. ё

Библиотека etree организована примерно следующим образом:
Имеются всякие фабрики и пр. создающие элементы типа Element. Кроме того имеется контейнер для них ElementTree. Мы можем поместить любой элемент (в частности рут, т.е. квазиконтейнер) в обертку, и обертку положим, записывать в файл. А можем поместить в обертку квазиконтейнер, а вернее ссылку на него, и изменять его. Нахер это надо науке не известно.
Видимо надо наследовать от контейнера и использовать его методы чтения/записи, и допичывать. При инициализации мы либо читаем, либо создаем новый (если без атрибутов, то новый) 
Надо прописать структуру:
 - Эксперимент (имя файла архитектуры модели, количество итераций, идентификатор окончания), 
    по большому счету, в любом случае придется применять гридата, т.е. интерполяцию (хотя, может оно и к лучшему). Т.е. какими-то функциями формируем задачу, а потом запускаем рассчет. При том, что данные все равно стохастические, хоть и на сетке
    - итем (значения (переменная = значение),) результат, видимо какие-то теги по результатам рассчетов
    - задача (значения (переменная = значение),) null

Что бы вытащить пару значений из сетки, надо сделать примерно следующее:
x = [1,2,3]
y = [4,5,6]

X,Y = np.meshgrid(x,y)

x = X.tolist()
y = Y.tolist()

z = [[x[i][j]+y[i][j] for i in range(len(x))] for j in range(len(y))]

при развертывании создаем Z размером X*Y и записываем в Z[item.i][item.j] = item.stuf

При свертывании выполняем двойной цикл в котором забиваем item.i = i, item.j = j, item.x = x[i][j], item.y = y[i][j], где x и y -- имена итерируемых переменных

Описание архитектуры осуществляется набором функций описывающих взаимодействие между компартментами
1. архитектура поклеточного описания. 
Расширяет класс клетки (не забывать указывать self, или сделать это в качествее обертки
 - как-то указываем что используем в качестве аргументов обратной связи. Или просто имеем набор показателей?
   - 1. События (Events) Состояние клетки . Вероятность и исход. Исход задается как функция (несколько принципиальных видов) от конечной точки назначения 
Видимо надо организовывать как 
    AddCondition(имя,[список условий],[список исходов])
    При этом, это должен быть метод в Engine, который потом передается в клетки при создании, например в виде вектора. Интересно, что можно присвоить значение переменной класса, потом создать несколько экземпляров. Расточительство памяти, кстати. Т.ч. держим  в енжине. И решатель там же.
2. архитектура непрерывных компартментов
 - формулы переходов. Очень гибкий механизм через eval(), фактически можно передавать как строку любую ерунду на питоне
 - формулы изменения собственного объема
* Для XML-фабрики есть волшебная функция, выполняющая роль сериализатора списка. Т.к. фабрика понимает на входе как строку так и эелемент типа _element, то функция может спокойно использовать в построении фабрики.
>>> def a(l, f):
...  for i in range(len(l)):
...   f.append(l[i])
...  return f
ggg = d(a([d('1'),d('2')], d()))

Для пуша объектов в память используем str(), для извлечения используем eval()


Может быть, когда-нибудь в будующем... http://www.dmg.org/
http://sourceforge.net/projects/pmml/
===

В конечном итоге архитектура предпологается следующая:

- HOP 
	- __init__.py
	- model.py -- расчетное ядро
		- cell
		- clone
	- core.py -- менеджер задач, загружает ядро 
		- taskmeneger
		- Plan
	- graph.py
		- 


Судя по всему надо использовать к обычному питону еще библиотеки NumPy или шире SciPy, IPython & Mathplotlib
см. тут: http://stackoverflow.com/questions/17481672/fitting-a-weibull-distribution-using-scipy
С япитоном пока приостановил, видится слишком сложным. Для установки япитона на винду требуется поставить продукт Anaconda, который является каким-то коммерческим. Но судя по всему он в своиз 300ста мегах тягает все либы для научных вычислений.
Оказалось, что у него есть очень удобный, а что самое главное, очень понятный Spyder -- IDE.


----------------------------------------------------

===ВНИМАНИЕ===

Вот он, ключ к успеху, прекомпиляция и хранение прекомпелированных строк

import datetime

def testCall(f, n = 1):
  st = datetime.datetime.now()
  for x in xrange(10**n): f()
  et = datetime.datetime.now()
  return (et-st).total_seconds()

def compare(a,b, n = 1):
    for x in xrange(10):
      lt = testCall(a, n)
      ct = testCall(b, n)
      print "%s %s %s%% slower" % (lt, ct, int(100.0*(ct-lt)/lt))
      
s = 'pass'

d = compile(s, '<string>', 'exec') <----------- ОБРАТИТЬ внимание на то, что тут может быть 'eval', и тогда фция будет возвращать значение

Важно! Что после компиляции изменение строки не влияет на скомпелированный объект (хотя впрочим это и так не происходит)
но он также модифицирует объекты в текущей области видимости
    
def a(): exec(d)
 
def b(): exec(s)

compare(a,b,6)   

>>> compare(a,b,6)

0.359 4.767 1227% slower
0.35 4.749 1256% slower
0.35 4.739 1254% slower
0.348 4.779 1273% slower
0.349 4.746 1259% slower
0.352 4.747 1248% slower
0.348 4.753 1265% slower
0.349 4.756 1262% slower
0.348 4.761 1268% slower
0.348 4.798 1278% slower

--------------------------------------------
магическая вызывалка через dot-notation

Спасибо lxml factory

class a:
 def __getattr__(self, s):
  return self.p(s)
 def p(self,f):
     print f
 def __repr__(self):
    return 'point'
 def __call__(self,d):
    self.p(d)

a1 = a()
-------------------------------------------
Еще одна магическая программулина. Делает минимальный расширяемый класс, чуть более минимальный чем просто пасс, но в стиле 3.0
# пока впишу сюда
class X(object):
    def __init__(self,_d={},**kwargs):
        kwargs.update(_d)
        self.__dict__=kwargs
class Y(X):
    def __repr__(self):
        return '<Y:%s>'%self.__dict__

----------------------------------------



Проверять тип, или компилировать константы:
>>> def a(): 
...  if type(d) == CodeType: 
...   return eval(d) 
...  else: return d
... 
>>> def b():
...  if type(c) == CodeType: 
...   return eval(d) 
...  else: return d
... 
>>> def b():
...  if type(c) == CodeType: 
...   return eval(c) 
...  else: return c
... 
>>> c = 1
>>> d = compile('1','','eval')
>>> compare(a,b,5)
0.102 0.043 -57% slower
0.082 0.04 -51% slower
0.082 0.04 -51% slower
0.083 0.04 -51% slower
0.081 0.04 -50% slower
0.087 0.043 -50% slower
0.081 0.041 -49% slower
0.084 0.041 -51% slower
0.082 0.041 -50% slower
0.084 0.04 -52% slower

Разница в исполнении существует, значит быстрее проверять чем прекомпелировать

------------------------------------------

type() или  isinstance()

>>> def a(): type(d) == 1
... 
>>> def b(): isinstance(d,int)
... 
>>> compare(a,b,5)
0.059 0.061 3% slower
0.04 0.062 54% slower
0.044 0.061 38% slower
0.042 0.06 42% slower
0.044 0.063 43% slower
0.041 0.061 48% slower
0.042 0.06 42% slower
0.042 0.06 42% slower
0.042 0.065 54% slower
0.042 0.062 47% slower

>>> def a(): type(d) == CodeType
... 
>>> def b(): isinstance(d,CodeType)
... 
>>> compare(b,a,5)
0.037 0.042 13% slower
0.035 0.039 11% slower
0.036 0.039 8% slower
0.035 0.038 8% slower
0.037 0.042 13% slower
0.036 0.037 2% slower
0.035 0.039 11% slower
0.037 0.037 0% slower
0.037 0.037 0% slower
0.035 0.038 8% slower

>>> def a(): type(d) == IntType
... 
>>> def b(): isinstance(d,IntType)
... 
>>> compare(a,b,5)
0.066 0.061 -7% slower
0.038 0.058 52% slower
0.038 0.058 52% slower
0.039 0.058 48% slower
0.037 0.062 67% slower
0.04 0.062 54% slower
0.038 0.058 52% slower
0.039 0.06 53% slower
0.039 0.059 51% slower
0.039 0.059 51% slower

>>> def a(): type(d) == IntType
... 
>>> def b(): type(c) == IntType
... 
>>> compare(a,b,5)
0.039 0.042 7% slower
0.038 0.042 10% slower
0.038 0.044 15% slower
0.038 0.041 7% slower
0.038 0.042 10% slower
0.038 0.041 7% slower
0.039 0.052 33% slower
0.039 0.042 7% slower
0.038 0.042 10% slower
0.038 0.042 10% slower
>>> def a(): isinstance(d,IntType)
... 
>>> def b(): isinstance(c,IntType)
... 
>>> compare(b,a,5)
0.043 0.062 44% slower
0.044 0.057 29% slower
0.039 0.057 46% slower
0.039 0.058 48% slower
0.039 0.058 48% slower
0.039 0.058 48% slower
0.039 0.058 48% slower
0.038 0.059 55% slower
0.038 0.061 60% slower
0.042 0.064 52% slower
>>> 

ВЫВОД!
Сравнивать лучше с CodeType методом isinstance()

------------------------------------

>>> def a(): isinstance(d,int)
... 
>>> def b(): isinstance(d,IntType)
... 
>>> compare(b,a,5)
0.063 0.066 4% slower
0.065 0.066 1% slower
0.064 0.069 7% slower
0.066 0.067 1% slower
0.063 0.073 15% slower
0.064 0.069 7% slower
0.068 0.069 1% slower
0.062 0.067 8% slower
0.063 0.067 6% slower
0.063 0.067 6% slower

Так-то!

-----------------------------------

>>> def c():pass
... 
>>> def a():exec(c.func_code)
... 
>>> def b():exec(d)
... 
>>> compare(b,a,5)
0.077 0.066 -14% slower
0.058 0.064 10% slower
0.058 0.065 12% slower
0.062 0.065 4% slower
0.059 0.07 18% slower
0.059 0.066 11% slower
0.06 0.064 6% slower
0.059 0.064 8% slower
0.059 0.067 13% slower
0.066 0.066 0% slower
>>> 