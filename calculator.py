import sys
import math

def mulForCal(aleft, aright):
    return float(aleft) * float(aright)     #add the exception which checks the integers numbers

def divForCal(aleft, aright):
    return float(aleft) / float(aright)

def divfloorForCal(aleft, aright):          #!!!!!!
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
    return abs(float(num))

def roundForCal(num):                 #Later
    return round(float(num))


DICT_ABS = {'abs': absForCal}
DICT_ROUND = {'round': roundForCal}
DICT_POW = {'^': powForCal}             #remake to lambda-function later
DICT_MUL_DIV = {'*': mulForCal, '/': divForCal, '//': divfloorForCal}
DICT_ADD_SUB = {'+': addForCal,'-': subForCal}

BOOL_DICT = {'>': moreForCal, '<': lessForCal, '>=': moreequalForCal, '<=': lessequalForCal, '==': equalForCal, '!=': notequalForCal}

TOUPLE_COUNST = ('e', 'pi', 'tau')

DICT_MATH = {}      #DICT_MATH['tan'](25)
for attr in math.__dict__:
    if not attr.startswith('__'):
        DICT_MATH[attr] = math.__dict__[attr]



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
        #else:   continue
    if len(leftbr) != len(rightbr): raise check_bracketsException

    

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
        #else:   continue

def expressioneval_math(list_expr, desiredDICT):        #Later (function for expressions from module math and abs,round)
    list_expr = subtransformation(list_expr)
    for offset, sign in enumerate(list_expr):               
        if sign in desiredDICT:         
            numright = list_expr[offset+1]
            res = str(desiredDICT[sign](numright))
            del list_expr[offset:offset+2]
            list_expr.insert(offset, res)
            return expressioneval(list_expr, desiredDICT) 
        

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
            print(resultlist)
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
            bracketspriority(leftlist)                      #
            expressioneval(leftlist, DICT_POW)              #
            expressioneval(leftlist, DICT_MUL_DIV)          #
            expressioneval(leftlist, DICT_ADD_SUB)          #

            check_brackets(rightlist)                       #
            rightlist = convertdigit(rightlist)             #
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
            checkvalue in DICT_ABS):
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

def expressioneval_mathexpression(list_expr):               #Later
    for offset, num in enumerate(list_expr):
        if (num in DICT_MATH or
            num in DICT_ROUND or
            num in DICT_ABS):
            aftermath = list_expr[offset+1:]
            count_leftbrackets = 0
            count_rightbrackets = 0
            offset_lastrightbracket = 0
            for offsetafter, numafter in enumerate(aftermath):
                if numafter == '(':
                    count_leftbrackets += 1
                elif numafter == ')':
                    count_rightbrackets += 1
                    if count_leftbrackets == count_rightbrackets:
                        offset_rightbracket = offsetafter
                        aftermath = aftermath[:offset_rightbracket+1]
                        ### if the math expression has other expression
                        for offsetin, numin in enumerate(aftermath):
                            if (numin in DICT_MATH or                                
                                numin in DICT_ROUND or
                                numin in DICT_ABS):
                                expressioneval_mathexpression(aftermath)
                        ###
                        bracketspriority(aftermath)
                        
                        expressioneval(aftermath, DICT_POW)       
                        expressioneval(aftermath, DICT_MUL_DIV)   
                        expressioneval(aftermath, DICT_ADD_SUB)
                        aftermath = ''.join(aftermath)
                        del list_expr[offset+1:offset+offset_rightbracket+2]
                        list_expr.insert(offset+1, aftermath)

                        expressioneval_math(list_expr, DICT_ABS)        #Later    
                        
                        return expressioneval_mathexpression(list_expr)
                        
                        
                    
                    
                    
            
            
    




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
        check_brackets(list_expression)                     #UNION to one function
        signtransformation(list_expression)
        list_expression = comparison(list_expression)
        if list_expression == True or list_expression == False:
            self.result = list_expression
        else:
            list_expression = convertdigit(list_expression) #
            convertfloat(list_expression)                   #

            expressioneval_mathexpression(list_expression)
            
            bracketspriority(list_expression)               #
            expressioneval(list_expression, DICT_POW)       #
            expressioneval(list_expression, DICT_MUL_DIV)   #
            expressioneval(list_expression, DICT_ADD_SUB)   #
            self.result = list_expression
            
    def __str__(self):
        return 'result: %s' % self.result



    
if __name__ == '__main__':
    #"""
    print(DICT_MATH)
    calc = Calculator()
    
    while True:
        expr = input('Enter the expression (exit - y):\n')
        if expr == 'y' or expr == 'Y':      # add the exception when someone enters 'Y' or 'y'
            break
        else:
            calc.new_expression(expr)            
            try:
                calc.calculation()
            except calculatorException as E:
                print('ERROR:', E)        
            else:
                print(calc)
    """
    a = ['abs', '(','2','+','3','3','.', '3',')','+','3']
    a = convertdigit(a)
    convertfloat(a)

    bracketspriority(a)
    print(a)
    """




