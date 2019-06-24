from mathexception import *
from mathsigns import *

def check_brackets(list_expr):
    leftbr = []     # '('
    rightbr = []    # ')'    
    for offset, num in enumerate(list_expr):
        if num == '(':
            leftbr.append(num)
        elif num == ')':
            rightbr.append(num)
        elif ((num in  DICT_MATH or        #just 2 + abs (if some math expression stands in the end)
              num in  DICT_ABS or
              num in DICT_ROUND) and offset == len(list_expr)-1):            
            raise check_bracketsException
        elif ((num in  DICT_MATH or         # not 'abs(' (if '(' doesn't stand after some math expression)
              num in  DICT_ABS or
              num in DICT_ROUND) and list_expr[offset+1] != '('):            
            raise check_bracketsException
    if len(leftbr) != len(rightbr): raise check_bracketsException
    

def check_mathseparatrix(list_expr):            #checks ',' in args DICT_MATH_ARGS and DICT_MATH
                                                #Later add checking to check nested math expression
                                                #Now it just checks one math expression without other expressions
    for offset, num in enumerate(list_expr):
        if num in DICT_MATH or num in DICT_MATH_ARGS:
            check_list = list_expr[offset+1:]
            count_leftbrackets = 0
            count_rightbrackets = 0
            for offsetcheck, numcheck in enumerate(check_list):
                if numcheck =='(':   count_leftbrackets += 1
                elif numcheck ==')':
                    count_rightbrackets += 1
                    if count_leftbrackets == count_rightbrackets:
                        check_list = check_list[:offsetcheck+1]
            countsep = 0
            for sign in check_list:
                if sign == ',': countsep += 1
            print(num, countsep)
            if num in DICT_MATH and countsep > 0:
                raise check_mathseparatrixException(DICT_MATH)
            elif num in DICT_MATH_ARGS and countsep > 1:
                raise check_mathseparatrixException(DICT_MATH_ARGS)

def check_spacesAndSeparatrix(list_expr):
    for offset, num in enumerate(list_expr):
        if offset == 0 and num == ' ':  raise check_spacesException
        elif (offset == 0 and
              num == '.' and
              not list_expr[offset+1].isdigit()):
            raise check_separatrixException
        elif (offset == len(list_expr)-1 and
              num == '.' and
              not list_expr[offset-1].isdigit()):
            raise check_separatrixException
    
        elif (num == '.' and
              not list_expr[offset-1].isdigit() and
              not list_expr[offset+1].isdigit()):
                raise check_separatrixException

def check_comparison(list_expr):
    count = 0
    for num in list_expr:
        if num in BOOL_DICT:
            count += 1
    if count > 1:   raise check_comparisonException



