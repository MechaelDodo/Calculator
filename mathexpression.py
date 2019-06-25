from mathsigns import *
from mathconvert import *
from mathtransform import *
from mathcheck import check_comparison

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
  
    #list_expr.append('')                                #QUICK'N'DIRTY
    for offset, sign in enumerate(list_expr):               
        if (sign in desiredDICT and                     #for MATH DICT_MATH_ARGS
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

def expressioneval_computemath(list_expr):                          #Later abs(-2)+abs(-3) = 5
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
                    break        

        for num in check_list:                                      #if for example 'abs' has math expression inside itself
            if  (num in DICT_MATH or                 
                num in DICT_ROUND or
                num in DICT_ABS or
                 num in DICT_MATH_ARGS):
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
            convertfloat(rightlist) 
            check_mathseparatrix(rightlist)
            expressioneval_computemath(rightlist)
            convertfloat(rightlist)                         #
            bracketspriority(rightlist)                     #
            expressioneval(rightlist, DICT_POW)             #
            expressioneval(rightlist, DICT_MUL_DIV)         #
            expressioneval(rightlist, DICT_ADD_SUB)         #

            list_expr = BOOL_DICT[num](''.join(str(leftlist[0])), ''.join(str(rightlist[0])))
            return list_expr
    return list_expr


