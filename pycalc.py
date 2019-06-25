from mathexception import calculatorException
from mathcheck import *
from mathtransform import *
from mathconvert import *
from mathexpression import *


class Calculator:
    def __init__(self, expression = None):
        self.expression = expression
        self.result = 0
    def new_expression(self, expression):
        self.__init__(expression)
    def calculation(self):
        list_expression = list(self.expression)
        list_expression = mathtransformation(list_expression)
        convertconst(list_expression)                       #Later
        
        check_spacesAndSeparatrix(list_expression)
        spacetransformation(list_expression)
        check_brackets(list_expression)                     #Late UNION to one function
        signtransformation(list_expression)
        check_wrongvalues(list_expression)
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
            self.result = normalization(list_expression)  
            
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
