from mathsigns import DICT_MATH, DICT_MATH_ARGS


class calculatorException(Exception):
    pass


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


class check_wrongvaluesException(calculatorException):
    def __init__(self, num, offset):
        calculatorException.__init__(self)
        self.value = num
        self.index = offset

    def __str__(self):
        return 'Wrong value: index:%s, value:\'%s\'' % (self.index, self.value)
