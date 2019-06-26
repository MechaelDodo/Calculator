from .mathsigns import *


class Transformer:

    def __init__(self, list_expr):
        self.list_expression = list_expr

    def sign_transformation(self):      # ['2', '<', '=', '3']=>['2', '<=', 3]
        for offset, num in enumerate(self.list_expression[:]):
            if offset == 0:
                continue
            sign = str(self.list_expression[offset-1]) + str(num)
            if sign in DICT_MUL_DIV or sign in BOOL_DICT:
                del self.list_expression[offset-1:offset+1]
                self.list_expression.insert(offset-1, sign)
                self.sign_transformation()

    def sub_transformation(self):       # ['-', '5', '+', '1']=>['-5', '+','1']
        if self.list_expression[0] in DICT_ADD_SUB:
            num = self.list_expression[0] + self.list_expression[1]
            del self.list_expression[0:2]
            self.list_expression.insert(0, num)

    def space_transformation(self):     # deletes all spaces
        for offset, num in enumerate(self.list_expression[:]):
            if num == ' ':
                del self.list_expression[offset]
                self.space_transformation()

    def math_transformation(self):      # ['a','b','s','(','2','-','10',')']
        firstoffset = 0                 # => ['abs','(','2','-','10',')']
        secondoffset = 0
        self.list_expression.append('')                 # QUICK'N'DIRTY
        while True:
            checkvalue = self.list_expression[firstoffset:secondoffset]
            checkvalue = ''.join(checkvalue)
            if (checkvalue in DICT_MATH_ARGS or
                checkvalue in DICT_ROUND or
                checkvalue in DICT_ABS or
                checkvalue in DICT_MATH or
                    checkvalue in TOUPLE_COUNST_inf_nan):
                if checkvalue + self.list_expression[secondoffset] != 'atan2':
                    del self.list_expression[firstoffset:secondoffset]
                    self.list_expression.insert(firstoffset, checkvalue)
                    secondoffset -= len(checkvalue)     # +1
                    firstoffset += 1
                else:
                    checkvaluesecond = self.list_expression[secondoffset]
                    checkvalue = checkvalue + checkvaluesecond
                    del self.list_expression[firstoffset:secondoffset+1]
                    self.list_expression.insert(firstoffset, checkvalue)
                    secondoffset -= len(checkvalue)
                    firstoffset += 1
            elif secondoffset == len(self.list_expression):
                secondoffset = firstoffset+2
                firstoffset += 1
            elif firstoffset == len(self.list_expression):
                break
            else:
                secondoffset += 1
        Transformer.delete_empty(self.list_expression)

    def delete_empty(list_expr):
        for offset, num in enumerate(list_expr):
            if num == '':
                del list_expr[offset]
                return Transformer.delete_empty(list_expr)

if __name__ == '__main__':
    t = Transformer(['-', '5', '+', ' ', '1', '<', '=', '3', '+',
                    'a', 'b', 's', '(', '2', '-', '10', ')'])
    t.sign_transformation()
    t.sub_transformation()
    t.space_transformation()
    t.math_transformation()
    print(t.list_expression)
