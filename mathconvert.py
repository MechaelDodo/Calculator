from mathsigns import TOUPLE_COUNST, DICT_MATH

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

def convertconst(list_expr):        #['e'] => ['2.718281828459045']
    for offset, num in enumerate(list_expr):
        if num in TOUPLE_COUNST:
            resultnum = str(DICT_MATH[num])
            del list_expr[offset]
            list_expr.insert(offset, resultnum)
            return convertconst(list_expr)

                      

