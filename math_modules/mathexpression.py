from mathsigns import *
from mathconvert import *
from mathtransform import Transformer
from mathcheck import check_comparison, check_brackets, check_mathseparatrix


class Proccessor:

    def __init__(self, list_expr):
        self.list_expression = list_expr

    def expression_evaluation(self, desiredDICT):       # general function for
        transform = Transformer(self.list_expression)   # expressions
        transform.sub_transformation()
        self.list_expression = transform.list_expression
        for offset, sign in enumerate(self.list_expression):
            if sign in desiredDICT:
                numleft = self.list_expression[offset-1]
                numright = self.list_expression[offset+1]
                res = str(desiredDICT[sign](numleft, numright))
                del self.list_expression[offset-1:offset+2]
                self.list_expression.insert(offset-1, res)
                return self.expression_evaluation(desiredDICT)

    def expression_evaluation_math(self, desiredDICT):  # ['abs','-5'] => ['5']
        self.list_expression.append('')                 # QUICK'N'DIRTY
        for offset, sign in enumerate(self.list_expression):
            if (sign in desiredDICT and             # for MATH DICT_MATH_ARGS
                self.list_expression[offset+1] != '(' and
                    self.list_expression[offset+2] == ','):
                numleft = self.list_expression[offset+1]
                numright = self.list_expression[offset+3]
                res = str(desiredDICT[sign](float(numleft), float(numright)))
                del self.list_expression[offset:offset+4]
                self.list_expression.insert(offset, res)
                return self.expression_evaluation_math(desiredDICT)
            elif sign in desiredDICT and self.list_expression[offset+1] != '(':
                numright = self.list_expression[offset+1]
                res = str(desiredDICT[sign](float(numright)))
                del self.list_expression[offset:offset+2]
                self.list_expression.insert(offset, res)
                return self.expression_evaluation_math(desiredDICT)

    def expression_evaluation_computemath(self):    # Later abs(-2)+abs(-3)=2+3
        index = 0
        while index != len(self.list_expression):
            if((self.list_expression[index] in DICT_MATH or
                self.list_expression[index] in DICT_ROUND or
                self.list_expression[index] in DICT_ABS or
                self.list_expression[index] in DICT_MATH_ARGS) and
                    self.list_expression[index+1] == '('):
                check_list = self.list_expression[index+1:]
            else:
                index += 1
                continue

            count_leftbrackets = 0
            count_rightbrackets = 0
            for offset, num in enumerate(check_list):
                if num == '(':
                    count_leftbrackets += 1
                elif num == ')':
                    count_rightbrackets += 1
                    if count_leftbrackets == count_rightbrackets:
                        check_list = check_list[:offset+1]
                        endbr = offset
                        break

            for num in check_list:      # if for example 'abs' has
                if(num in DICT_MATH or    # math expression inside itself
                    num in DICT_ROUND or
                    num in DICT_ABS or
                        num in DICT_MATH_ARGS):
                    list_expr = self.list_expression
                    self.list_expression = check_list
                    self.expression_evaluation_computemath()
                    check_list = self.list_expression
                    self.list_expression = list_expr

            for offset, num in enumerate(check_list):   # in math expr
                if num == ',':                          # which has any args
                    leftcheck_list = check_list[1:offset]
                    rightcheck_list = check_list[offset+1:-1]
                    for lst in (leftcheck_list, rightcheck_list):
                        lst.insert(0, '(')  # QUICK'N'DIRTY
                        lst.append(')')
                        list_expr = self.list_expression
                        self.list_expression = lst
                        self.bracketspriority()
                        lst = self.list_expression
                        self.list_expression = list_expr

                    leftcheck_list = ''.join(leftcheck_list)
                    rightcheck_list = ''.join(rightcheck_list)
                    del self.list_expression[index+1:endbr+2+index]
                    for inlist in (rightcheck_list, ',', leftcheck_list):
                        self.list_expression.insert(index+1, inlist)
                    self.expressioneval_math(DICT_MATH_ARGS)
                    index += 1                                          # ?
                    return self.expressioneval_computemath()

            list_expr = self.list_expression
            self.list_expression = check_list
            self.bracketspriority()
            check_list = self.list_expression
            self.list_expression = list_expr
            check_list = ''.join(check_list)
            del self.list_expression[index+1:endbr+2+index]
            self.list_expression.insert(index+1, check_list)

            for dict_math in (DICT_ABS, DICT_ROUND, DICT_MATH):
                self.expression_evaluation_math(dict_math)
            index += 1                                  # ?
            return self.expression_evaluation_computemath()

    def bracketspriority(self):    # ['3','-','(','2','+','10',')','-','1']
        for offset, num in enumerate(self.list_expression):     # =>
            if num == '(':          # ['3','-','12','-','1']
                leftbr = offset
            elif num == ')':
                list_expr = self.list_expression

                self.list_expression = self.list_expression[leftbr+1:offset]
                convert = Convert(self.list_expression)
                convert.convert_digit()
                self.list_expression = convert.list_expression

                dicts = (DICT_POW, DICT_MUL_DIV, DICT_ADD_SUB)
                for dict_math in dicts:
                    self.expression_evaluation(dict_math)

                del list_expr[leftbr:offset+1]
                list_expr.insert(leftbr, ''.join(self.list_expression))
                self.list_expression = list_expr
                self.bracketspriority()

    def comparison(self):          # ['2', '+', '3', '>=', '4'] => True
        check_comparison(self.list_expression)

        for offset, num in enumerate(self.list_expression):
            if num in BOOL_DICT:
                leftlist = self.list_expression[:offset]
                rightlist = self.list_expression[offset+1:]

                check_brackets(leftlist)                        #
                convert = Convert(leftlist)
                convert.convert_digit()
                convert.convert_float()
                leftlist = convert.list_expression
                check_mathseparatrix(leftlist)
                self.list_expression = leftlist
                self.expression_evaluation_computemath()
                self.bracketspriority()
                for dict_math in (DICT_POW, DICT_MUL_DIV, DICT_ADD_SUB):
                    self.expression_evaluation(dict_math)
                leftlist = self.list_expression

                check_brackets(rightlist)                        #
                convert = Convert(rightlist)
                convert.convert_digit()
                convert.convert_float()
                rightlist = convert.list_expression
                check_mathseparatrix(rightlist)
                self.list_expression = rightlist
                self.expression_evaluation_computemath()
                self.bracketspriority()
                for dict_math in (DICT_POW, DICT_MUL_DIV, DICT_ADD_SUB):
                    self.expression_evaluation(dict_math)
                rightlist = self.list_expression

                leftlist = ''.join(str(leftlist[0]))
                rightlist = ''.join(str(rightlist[0]))
                self.list_expression = BOOL_DICT[num](leftlist, rightlist)


if __name__ == '__main__':
    p = Proccessor(['2', '+', '3', '>=', '4'])
    p.comparison()
    print(p.list_expression)
