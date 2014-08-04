# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 15:32:42 2014

@author: russinow

Синтаксис фабрики:
>>> from lxml.builder import ElementMaker
>>> E = ElementMaker()
>>> d = E.e
>>> ff = E('ddd')

* Для XML-фабрики есть волшебная функция, выполняющая роль сериализатора списка. Т.к. фабрика понимает на входе как строку так и эелемент типа _element, то функция может спокойно использовать в построении фабрики.
>>> def a(l, f):
...  for i in range(len(l)):
...   f.append(l[i])
...  return f
ggg = d(a([d('1'),d('2')], d()))

Для пуша объектов в память используем str(), для извлечения используем eval()


Извлечение элементов

>>> from lxml import etree
>>> etree.tostring(ff)


"""



import xml.etree.ElementTree as ET


def load(name):
    tree = ET.parse(load) #(file_in)
    root = tree.getroot()
    return root
    
    