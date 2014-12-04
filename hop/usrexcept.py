# -*- coding: utf-8 -*-
"""
@author: russinow m a
ReMONA V.1.0
http://russinow.me/
"""

def setScript(ExClass, s):
        ExClass.script = compile(s,'<string>', 'exec')

class AbsractUException(Exception): 
    def __init__(self, val1 = None, val2 = None):
        self.val1 = val1
        self.val2 = val2            
    def __str__(self):
        return repr(self.value)

        
AUE = AbsractUException

class UException1(AUE): pass
class UException2(AUE): pass
class UException3(AUE): pass
class UException4(AUE): pass
class UException5(AUE): pass
class UException6(AUE): pass  

#setScript(UException1,'print("getit!")')

#try:
#    raise UException1
#except UException2 as UE2:
#    eval(UE2.script)
#except UException1 as UE1:
#    eval(UE1.script)