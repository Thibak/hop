# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:27:42 2014

@author: russinow
"""


#import argparse
from code import interact 
import sys
sys.path.append('..')
#import hop
from __init__ import load, start
print ("import")

try:
    filename = sys.argv[1]
except IndexError: 
    if sys.argv == [sys.argv[0]]:
        #Если имя файла отсутствует, в качестве опций дальнейшей работы пользователю предлагается:
            #ввести имя файла (запускаются теже процедуры, что и при коротком вызове)
            #запустить командную строку Python с импортированной библиотекой HOP
        yn = raw_input(""" Wecome to HOP. 
To download the experiment file enter its name (with full name if...) 
to download interactive shell enter 'I'
to exit enter 'X'""") 
        if yn in 'iIшШbBиИ':
                #print graph_help
                interact(local=locals()) # перейти в интерактивный режим, вывести хелп по графике
                print ('point')
        elif yn in 'хХЧчxXexitquitqQ':
                print ('EXIT')
                sys.exit()
        else:
                filename = yn

#try:
#hop.
load(filename)
#except:
#    pass
#hop.
start()

#""" Добро пожаловать в HOP.
#    Для загрузке файла эксперимента введите его имя (с полным адресом, если ...)
#    для загрузки интерактивного режима введите 'I'
#    для выхода введите 'X'"""
