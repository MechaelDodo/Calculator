from .mathsigns import TOUPLE_COUNST, DICT_MATH, TOUPLE_COUNST_inf_nan


class Convert:

    def __init__(self, list_expr):
        self.list_expression = list_expr

    def convert_digit(self):        # returns new list(doesn't change list):
        index = 0                   # ['3','3'] => ['33']
        digitlist = []
        list_expr_res = []
        while True:
            if index == len(self.list_expression):
                digitlist = ''.join(digitlist)
                list_expr_res.append(digitlist)
                index += 1
                digitlist = []
                break
            if (not str(self.list_expression[index]).isdigit() and
                    bool(digitlist)):
                digitlist = ''.join(digitlist)
                list_expr_res.append(digitlist)
                list_expr_res.append(self.list_expression[index])
                index += 1
                digitlist = []
            elif (not str(self.list_expression[index]).isdigit() and
                    not digitlist):
                list_expr_res.append(self.list_expression[index])
                index += 1
            else:
                digitlist.append(self.list_expression[index])
                index += 1
        self.list_expression = list_expr_res

    def convert_float(self):        # changes list: ['2', '.', '3'] => ['2.3']
        for offset, num in enumerate(self.list_expression[:]):
            if (num == '.' and self.list_expression[offset-1].isdigit() and
                offset != 0 and
                    self.list_expression[offset+1].isdigit()):
                floatnum = ''.join(self.list_expression[offset-1:offset+2])
                del self.list_expression[offset-1:offset+2]
                self.list_expression.insert(offset-1, floatnum)
                return self.convert_float()
            if num == '.' and not self.list_expression[offset+1].isdigit():
                self.list_expression.insert(offset+1, '0')
                floatnum = ''.join(self.list_expression[offset-1:offset+2])
                del self.list_expression[offset-1:offset+2]
                self.list_expression.insert(offset-1, floatnum)
                return self.convert_float()
            elif (num == '.' and offset == 0) or num == '.':
                self.list_expression.insert(offset, '0')
                floatnum = ''.join(self.list_expression[offset:offset+3])
                del self.list_expression[offset:offset+3]
                self.list_expression.insert(offset, floatnum)
                return self.convert_float()

    def convert_const(self):        # ['e'] => ['2.718281828459045']
        for offset, num in enumerate(self.list_expression):
            if num in TOUPLE_COUNST:
                resultnum = str(DICT_MATH[num])
                del self.list_expression[offset]
                self.list_expression.insert(offset, resultnum)
                return self.convert_const()
            elif num in TOUPLE_COUNST_inf_nan:
                self.list_expression[offset] = float(num)

    def normalization(list_expr):
        res = list_expr[0]
        resoff = list(res)
        tail = None
        for offset, num in enumerate(resoff):
            if num == '.':
                tail = resoff[offset+1:]
                break
        sumtail = 0
        if tail is not None:
            for num in tail:
                sumtail += int(num)
        if sumtail == 0:
            res = int(float(res))
        return res

if __name__ == '__main__':
    c = Convert(['3', '3', '+', '2', '.', '3', '+', 'e'])
    c.convert_digit()
    c.convert_float()
    c.convert_const()
    print(c.list_expression)

    a = ['2.0']
    a = Convert.normalization(a)
    print(a)
