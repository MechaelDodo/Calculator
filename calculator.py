import sys
import math

def mulForCal(aleft, aright):
    return float(aleft) * float(aright)     #Later add the exception which checks the integers numbers

def divForCal(aleft, aright):
    return float(aleft) / float(aright)

def divfloorForCal(aleft, aright):          #Later!!!!!!
    return float(aleft) // float(aright)

def addForCal(aleft, aright):
    return float(aleft) + float(aright)

def subForCal(aleft, aright):
    return float(aleft) - float(aright)

def powForCal(aleft, aright):
    return pow(float(aleft), float(aright))

def moreForCal(aleft, aright):
    return float(aleft) > float(aright)

def lessForCal(aleft, aright):
    return float(aleft) < float(aright)

def moreequalForCal(aleft, aright):
    print(aleft, aright)
    return float(aleft) >= float(aright)

def lessequalForCal(aleft, aright):
    return float(aleft) <= float(aright)

def equalForCal(aleft, aright):
    return float(aleft) == float(aright)

def notequalForCal(aleft, aright):
    return float(aleft) != float(aright)

def absForCal(num):                   #Later
    return abs(num)

def roundForCal(num):                 #Later
    return round(num)


DICT_ABS = {'abs': absForCal}
DICT_ROUND = {'round': roundForCal}
DICT_POW = {'^': powForCal}             #Later remake to lambda-function later
DICT_MUL_DIV = {'*': mulForCal, '/': divForCal, '//': divfloorForCal}
DICT_ADD_SUB = {'+': addForCal,'-': subForCal}

BOOL_DICT = {'>': moreForCal, '<': lessForCal, '>=': moreequalForCal, '<=': lessequalForCal, '==': equalForCal, '!=': notequalForCal}

TOUPLE_COUNST = ('e', 'pi', 'tau')

DICT_MATH = {}                          #DICT_MATH['tan'](25)
for attr in math.__dict__:
    if not attr.startswith('__'):
        DICT_MATH[attr] = math.__dict__[attr]

DICT_MATH_ARGS = {}                     #this dict has more attrs than 1
for attr in ('atan2', 'copysign', 'fmod', 'gcd', 'hypot', 'isclose', 'ldexp', 'pow', 'remainder', 'log'):       #Later i will think about 'log' because
                                                                                                                #'log' can take as 1 arg and 2 args
    DICT_MATH_ARGS[attr] = DICT_MATH[attr]
    del DICT_MATH[attr]


class calculatorException(Exception):   pass

class check_bracketsException(calculatorException):
    def __str__(self):
        return 'You have an exception with brackets'

class check_comparisonException(calculatorException):
    def __str__(self):
        return 'You have more signs of comparison than 1'

class check_spacesException(calculatorException):
    def __str__(self):
        return 'You have an exception with spaces'

class check_separatrixException(calculatorException):
    def __str__(self):
        return 'Separatrix should not be between not digit numbers'

class check_mathseparatrixException(calculatorException):
    def __init__(self, mathdict):
        calculatorException.__init__(self)
        self.mathdict = mathdict
    def __str__(self):
        if self.mathdict == DICT_MATH:
            return 'Separatrix should not be here'
        elif self.mathdict == DICT_MATH_ARGS:
            return 'Separatrix should not be more than 1'




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
                        

def expressioneval(list_expr, desiredDICT):     #general function for expressions
    list_expr = subtransformation(list_expr)
    for offset, sign in enumerate(list_expr):               
        if sign in desiredDICT:         
            numleft = list_expr[offset-1]
            numright = list_expr[offset+1]
            res = str(desiredDICT[sign](numleft, numright))
            del list_expr[offset-1:offset+2]
            list_expr.insert(offset-1, res)
            return expressioneval(list_expr, desiredDICT)            


def expressioneval_math(list_expr, desiredDICT):        #Later (function for expressions from module math and abs,round)
                                                        #may be will make a new function for DICT_MATH_ARGS
    print('expressioneval_math', list_expr)
    for offset, sign in enumerate(list_expr):               
        if (sign in desiredDICT and                   #for MATH DICT_MATH_ARGS
              list_expr[offset+1] != '(' and
              list_expr[offset+2] == ','):
            numleft = list_expr[offset+1]
            numright = list_expr[offset+3]
            res = str(desiredDICT[sign](float(numleft), float(numright)))
            del list_expr[offset:offset+4]
            list_expr.insert(offset, res)
            return expressioneval_math(list_expr, desiredDICT)
        elif sign in desiredDICT and list_expr[offset+1] != '(':
            numright = list_expr[offset+1]
            res = str(desiredDICT[sign](float(numright)))
            del list_expr[offset:offset+2]
            list_expr.insert(offset, res)
            return expressioneval_math(list_expr, desiredDICT)
            
        

def convertdigit(list_expr):        #returns new list(doesn't change list): ['3','3'] => ['33']
    index = 0
    digitlist = []
    list_expr_res = []
    while True:
        if index == len(list_expr):
            digitlist = ''.join(digitlist)
            list_expr_res.append(digitlist)
            index += 1
            digitlist = []
            break
        if not list_expr[index].isdigit() and bool(digitlist):           
            digitlist = ''.join(digitlist)
            list_expr_res.append(digitlist)
            list_expr_res.append(list_expr[index])
            index += 1
            digitlist = []
        elif not list_expr[index].isdigit() and not digitlist:
            list_expr_res.append(list_expr[index])
            index += 1
        else:
            digitlist.append(list_expr[index])
            index += 1
    return list_expr_res


def convertfloat(list_expr):        #changes list: ['2', '.', '3'] => ['2.3']
    for offset, num in enumerate(list_expr[:]):            
        if num == '.' and list_expr[offset-1].isdigit() and offset != 0 and list_expr[offset+1].isdigit():
            floatnum = ''.join(list_expr[offset-1:offset+2])
            del list_expr[offset-1:offset+2]
            list_expr.insert(offset-1, floatnum)
            return convertfloat(list_expr)
        if num == '.' and not list_expr[offset+1].isdigit():
            list_expr.insert(offset+1, '0')
            floatnum = ''.join(list_expr[offset-1:offset+2])
            del list_expr[offset-1:offset+2]
            list_expr.insert(offset-1, floatnum)
            return convertfloat(list_expr)
        elif (num == '.' and offset == 0) or num == '.':
            list_expr.insert(offset, '0')
            floatnum = ''.join(list_expr[offset:offset+3])
            del list_expr[offset:offset+3]
            list_expr.insert(offset, floatnum)
            return convertfloat(list_expr)


def bracketspriority(list_expr):    #changes list, computes expressions in brackets: ['3', '-', '(', '2', '+', '10', ')', '-', '1'] => ['3', '-', '12', '-', '1']
    for offset, num in enumerate(list_expr):
        if num == '(':
            leftbr = offset
        elif num == ')':
            resultlist = list_expr[leftbr+1:offset]
            resultlist = convertdigit(resultlist)           #
            expressioneval(resultlist, DICT_POW)            #
            expressioneval(resultlist, DICT_MUL_DIV)        #
            expressioneval(resultlist, DICT_ADD_SUB)        #
            
            del list_expr[leftbr:offset+1]
            list_expr.insert(leftbr, ''.join(resultlist))
            bracketspriority(list_expr)


def check_comparison(list_expr):
    count = 0
    for num in list_expr:
        if num in BOOL_DICT:
            count += 1
    if count > 1:   raise check_comparisonException
    

def comparison(list_expr):          #['2', '+', '3', '>=', '4'] => True                                  
    check_comparison(list_expr)
    
    for offset, num in enumerate(list_expr):    
        if num in BOOL_DICT:
            leftlist = list_expr[:offset]
            rightlist = list_expr[offset+1:]

            check_brackets(leftlist)                        #
            leftlist = convertdigit(leftlist)               #
            convertfloat(leftlist)                          #
            check_mathseparatrix(leftlist)
            expressioneval_computemath(leftlist)
            bracketspriority(leftlist)                      #
            expressioneval(leftlist, DICT_POW)              #
            expressioneval(leftlist, DICT_MUL_DIV)          #
            expressioneval(leftlist, DICT_ADD_SUB)          #

            check_brackets(rightlist)                       #
            rightlist = convertdigit(rightlist)             #
            check_mathseparatrix(rightlist)
            expressioneval_computemath(rightlist)
            convertfloat(rightlist)                         #
            bracketspriority(rightlist)                     #
            expressioneval(rightlist, DICT_POW)             #
            expressioneval(rightlist, DICT_MUL_DIV)         #
            expressioneval(rightlist, DICT_ADD_SUB)         #
            
            list_expr = BOOL_DICT[num](''.join(leftlist), ''.join(rightlist))
            return list_expr
    return list_expr

            
def signtransformation(list_expr):      #['2', '<', '=', '3'] => ['2', '<=', 3]
    for offset, num in enumerate(list_expr[:]):
        if offset == 0: continue
        sign = list_expr[offset-1] + num
        
        if sign in DICT_MUL_DIV or sign in BOOL_DICT:
            del list_expr[offset-1:offset+1]
            list_expr.insert(offset-1, sign)
            signtransformation(list_expr)
    return list_expr


def subtransformation(list_expr):       #['-', '5', '+', '1'] => ['-5', '+', '1']
    if list_expr[0] in DICT_ADD_SUB:
        num = list_expr[0] + list_expr[1]
        del list_expr[0:2]
        list_expr.insert(0, num)
        return list_expr
    else:
        return list_expr 


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

    
def spacetransformation(list_expr):     #deletes all spaces
    for offset, num in enumerate(list_expr[:]):
        if num == ' ':
            del list_expr[offset]
            return (spacetransformation(list_expr))
        

def mathtransformation(list_expr):      #['a', 'b', 's', '(', '2', '-', '10', ')'] => ['abs', '(', '2', '-', '10', ')']
    firstoffset = 0
    secondoffset = 0
    while True:
        checkvalue = ''.join(list_expr[firstoffset:secondoffset])
        if (checkvalue in DICT_MATH or
            checkvalue in DICT_ROUND or
            checkvalue in DICT_ABS or
            checkvalue in DICT_MATH_ARGS):
            del list_expr[firstoffset:secondoffset]
            list_expr.insert(firstoffset, checkvalue)
            secondoffset -= len(checkvalue) #+1          
            firstoffset += 1
        elif secondoffset == len(list_expr):
            secondoffset = firstoffset+2
            firstoffset += 1
        elif firstoffset == len(list_expr):
            break
        else:
            secondoffset += 1
    return list_expr
           
                        
def expressioneval_computemath(list_expr):                          #Later this fun has a bag: abs(-2)+abs(-3)=> 2 (must be 5)
    print('expressioneval_computemath', list_expr)
    index = 0    
    while index != len(list_expr):                          
        if (list_expr[index] in DICT_MATH or                
            list_expr[index] in DICT_ROUND or
            list_expr[index] in DICT_ABS or
            list_expr[index] in DICT_MATH_ARGS) and list_expr[index+1] == '(':
            check_list = list_expr[index+1:]
        else:
            index += 1
            continue
        
        count_leftbrackets = 0
        count_rightbrackets = 0
        for offset, num in enumerate(check_list):
            if num =='(':   count_leftbrackets += 1
            elif num ==')':
                count_rightbrackets += 1
                if count_leftbrackets == count_rightbrackets:
                    check_list = check_list[:offset+1]
                    endbr = offset
        

        for num in check_list:                                      #if for example 'abs' has math expression inside itself
            if  (num in DICT_MATH or                 
                num in DICT_ROUND or
                num in DICT_ABS or
                 num in DICT_MATH_ARGS):
                print('check_list', check_list)
                expressioneval_computemath(check_list)
                
        for offset, num in enumerate(check_list):                   #in math expr which has any args 
            if num == ',':
                leftcheck_list = check_list[1:offset]
                rightcheck_list = check_list[offset+1:-1]                
                for lst in (leftcheck_list, rightcheck_list):       #QUICK'N'DIRTY
                    lst.insert(0, '(')
                    lst.append(')')
                    bracketspriority(lst)
                    
                leftcheck_list = ''.join(leftcheck_list)
                rightcheck_list = ''.join(rightcheck_list)
                del list_expr[index+1:endbr+2+index]
                for inlist in (rightcheck_list, ',', leftcheck_list):
                    list_expr.insert(index+1, inlist)
                expressioneval_math(list_expr, DICT_MATH_ARGS)
                
                index += 1                                          #?         
                return expressioneval_computemath(list_expr)              
        bracketspriority(check_list)
        check_list = ''.join(check_list)
        del list_expr[index+1:endbr+2+index]                      
        list_expr.insert(index+1, check_list)
                
        expressioneval_math(list_expr, DICT_ABS)
        expressioneval_math(list_expr, DICT_MATH)
        
        index += 1                                  #?
        return expressioneval_computemath(list_expr)

                            
def convertconst(list_expr):        #['e'] => ['2.718281828459045']
    for offset, num in enumerate(list_expr):
        if num in TOUPLE_COUNST:
            resultnum = str(DICT_MATH[num])
            del list_expr[offset]
            list_expr.insert(offset, resultnum)
            return convertconst(list_expr)
                        
            
class Calculator:
    def __init__(self, expression = None):
        self.expression = expression
        self.result = 0
    def new_expression(self, expression):
        self.__init__(expression)
    def calculation(self):
        list_expression = list(self.expression)
        list_expression = mathtransformation(list_expression)
        convertconst(list_expression)
        
        check_spacesAndSeparatrix(list_expression)
        spacetransformation(list_expression)
        check_brackets(list_expression)                     #Late UNION to one function
        signtransformation(list_expression)
        
        list_expression = comparison(list_expression)
        
        if list_expression == True or list_expression == False:
            self.result = list_expression
        else:
            list_expression = convertdigit(list_expression) #
            convertfloat(list_expression)                   #
                       
            check_mathseparatrix(list_expression)
            expressioneval_computemath(list_expression)
            
            bracketspriority(list_expression)               #
            expressioneval(list_expression, DICT_POW)       #
            expressioneval(list_expression, DICT_MUL_DIV)   #
            expressioneval(list_expression, DICT_ADD_SUB)   #
            self.result = list_expression                   #Later 'result' must be a number(now it's a list)
            
    def __str__(self):
        return 'result: %s' % self.result

    
if __name__ == '__main__':
    
    calc = Calculator()
    
    while True:
        expr = input('Enter the expression (exit - y):\n')
        if expr == 'y' or expr == 'Y':                  # add the exception .when someone enters 'Y' or 'y'
            break
        else:
            calc.new_expression(expr)            
            try:
                calc.calculation()
            except calculatorException as E:
                print('ERROR:', E)        
            else:
                print(calc)




