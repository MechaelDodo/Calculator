from mathsigns import *

def signtransformation(list_expr):      #['2', '<', '=', '3'] => ['2', '<=', 3]
    for offset, num in enumerate(list_expr[:]):
        if offset == 0: continue
        
        sign = str(list_expr[offset-1]) + str(num)        
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

def spacetransformation(list_expr):     #deletes all spaces
    for offset, num in enumerate(list_expr[:]):
        if num == ' ':
            del list_expr[offset]
            return (spacetransformation(list_expr))
        

def mathtransformation(list_expr):      #['a', 'b', 's', '(', '2', '-', '10', ')'] => ['abs', '(', '2', '-', '10', ')']
    firstoffset = 0
    secondoffset = 0
    list_expr.append('')                #QUICK'N'DIRTY      
    while True:
        checkvalue = ''.join(list_expr[firstoffset:secondoffset])
        if (checkvalue in DICT_MATH_ARGS or
            checkvalue in DICT_ROUND or
            checkvalue in DICT_ABS or
            checkvalue in DICT_MATH or
            checkvalue in TOUPLE_COUNST_inf_nan):
            if checkvalue + list_expr[secondoffset] != 'atan2':
                del list_expr[firstoffset:secondoffset]
                list_expr.insert(firstoffset, checkvalue)
                secondoffset -= len(checkvalue) #+1          
                firstoffset += 1
            else:
                checkvalue = checkvalue + list_expr[secondoffset]
                del list_expr[firstoffset:secondoffset+1]
                list_expr.insert(firstoffset, checkvalue)
                secondoffset -= len(checkvalue)
                firstoffset += 1
        elif secondoffset == len(list_expr):
            secondoffset = firstoffset+2
            firstoffset += 1
        elif firstoffset == len(list_expr):
            break
        else:
            secondoffset += 1
    return list_expr

def delete_empty(list_expr):
    for offset, num in enumerate(list_expr):
        if num == '':
            del list_expr[offset]
            return delete_empty(list_expr)
