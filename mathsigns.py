import math

DICT_ABS = {'abs': lambda num: abs(num)}

DICT_ROUND = {'round': lambda num: round(num)}

DICT_POW = {'^': lambda aleft, aright: pow(float(aleft), float(aright))}             #Later make the exception which checks the integers numbers(maybe it is not neccessery)

DICT_MUL_DIV = {'*': lambda aleft, aright: float(aleft) * float(aright),
                '/': lambda aleft, aright: float(aleft) / float(aright),
                '//': lambda aleft, aright: float(aleft) // float(aright)}

DICT_ADD_SUB = {'+': lambda aleft, aright: float(aleft) + float(aright),
                '-': lambda aleft, aright: float(aleft) - float(aright)}

BOOL_DICT = {'>': lambda aleft, aright: float(aleft) > float(aright),
             '<': lambda aleft, aright: float(aleft) < float(aright),
             '>=': lambda aleft, aright: float(aleft) >= float(aright),
             '<=': lambda aleft, aright: float(aleft) <= float(aright),
             '==': lambda aleft, aright: float(aleft) == float(aright),
             '!=': lambda aleft, aright: float(aleft) != float(aright)}

TOUPLE_COUNST = ('e', 'pi', 'tau')

DICT_MATH = {}                          #DICT_MATH['tan'](25)
for attr in math.__dict__:
    if not attr.startswith('__'):
        DICT_MATH[attr] = math.__dict__[attr]

DICT_MATH_ARGS = {}                     #this dict has more attrs than 1
for attr in ('atan2', 'copysign', 'fmod', 'gcd', 'hypot', 'isclose', 'ldexp', 'pow', 'remainder', 'log'):       #Later i need think about 'log' because
                                                                                                                #'log' can take as 1 arg and 2 args
    DICT_MATH_ARGS[attr] = DICT_MATH[attr]
    del DICT_MATH[attr]
