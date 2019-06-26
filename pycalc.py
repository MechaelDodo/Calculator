from math_modules.mathexception import calculatorException
from math_modules.mathcheck import *
from math_modules.mathtransform import Transformer
from math_modules.mathconvert import Convert
from math_modules.mathexpression import Proccessor


class Calculator:
    def __init__(self, expression = None):
        self.expression = expression
        self.result = 0
    def new_expression(self, expression):
        self.__init__(expression)
    def calculation(self):
        list_expression = list(self.expression)
        transformer = Transformer(list_expression)
        convert = Convert(list_expression)
        transformer.math_transformation()
        convert.list_expression = transformer.list_expression
        convert.convert_const()
        check_spacesAndSeparatrix(convert.list_expression)
        transformer.list_expression = convert.list_expression
        transformer.space_transformation()
        check_brackets(transformer.list_expression)
        transformer.sign_transformation()
        check_wrongvalues(transformer.list_expression)

        proccessor = Proccessor(transformer.list_expression)
        proccessor.comparison()
        if type(proccessor.list_expression) == bool:
            self.result = proccessor.list_expression
        else:
            convert.list_expression = proccessor.list_expression
            convert.convert_digit()
            convert.convert_float()
            check_mathseparatrix(convert.list_expression)
            proccessor.list_expression = convert.list_expression
            proccessor.expression_evaluation_computemath()
            proccessor.bracketspriority()
            for dict_math in (DICT_POW, DICT_MUL_DIV, DICT_ADD_SUB):
                proccessor.expression_evaluation(dict_math)
            self.result = Convert.normalization(proccessor.list_expression)           
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
