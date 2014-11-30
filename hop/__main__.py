# -*- coding: utf-8 -*-
"""
Replicative MetaObject Network Analyser (ReMONA)
Система Анализа Репликативных МультиОбъектных Сетей (САРМОС)

@author: russinow 
ReMONA V.1.0
http://russinow.me/
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
        yn = raw_input(""" 
          Wecome to ReMON Analyser
=== Replicative MetaObject Network Analyser ===
 - version 1.0
 http://russinow.me/
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

load(filename)

start()

#""" Добро пожаловать в ReMON Analyser
# === Replicative MetaObject Network Analyser ===
# Система Анализа Репликативных МультиОбъектных Сетей
#    Для загрузке файла эксперимента введите его имя (с полным адресом, если ...)
#    для загрузки интерактивного режима введите 'I'
#    для выхода введите 'X'"""
