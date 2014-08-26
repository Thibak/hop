# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:27:42 2014

@author: russinow
"""
#import argparse
from code import interact 
import sys
import hop


if sys.argv == [sys.argv[0]]:
    #Если имя файла отсутствует, в качестве опций дальнейшей работы пользователю предлагается:
        #ввести имя файла (запускаются теже процедуры, что и при коротком вызове)
        #запустить командную строку Python с импортированной библиотекой HOP
    yn = raw_input(""" Добро пожаловать в HOP.
Для загрузке файла эксперимента введите его имя (с полным адресом, если ...)
для загрузки интерактивного режима введите "I"
для выхода введите "X" 
    """) 
    if   yn == 'i' or 'I' or 'ш' or 'Ш' or 'b' or 'B' or 'и' or 'И' or '':
            #print graph_help
            interact(local=locals()) # перейти в интерактивный режим, вывести хелп по графике
    elif yn == 'х' or 'Х' or 'Ч' or 'ч' or 'x' or 'X' or 'exit' or 'quit' or 'q' or 'Q':
            sys.exit()
            print ('досвидания')
    else:
            filename = yn
filename = sys.argv[1]
hop.load(filename)
hop.start()

