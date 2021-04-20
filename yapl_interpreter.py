from yapl_lexer import *
from yapl_parser import *
import sys

variables = {}

def exp_eval(p):
    operator = p[0]
    # print(operator)
    # if type(p[1]) == str:
    #     p[1] = var_val(p[1])
    # print('p1:',p[1])
    if operator == 'PAREN':
        return exp_eval(p[1])
    elif operator == '+':
        return exp_eval(p[1]) + exp_eval(p[2])
    elif operator == ',':
        # exp = [p[1], exp_eval(p[2])]
        return str(exp_eval(p[1])) + " " + str(exp_eval(p[2]))
    elif operator == '-':
        return exp_eval(p[1]) - exp_eval(p[2])
    elif operator == '*':
        return exp_eval(p[1]) * exp_eval(p[2])
    elif operator == '/':
        return exp_eval(p[1]) / exp_eval(p[2])
    elif operator == '%':
        return exp_eval(p[1]) % exp_eval(p[2])
    elif operator == '^':
        return exp_eval(p[1]) ** exp_eval(p[2])
    elif operator == '++':
        return exp_eval(p[1]) + 1
    elif operator == '--':
        return exp_eval(p[1]) - 1
    elif operator == '<':
        return exp_eval(p[1]) < exp_eval(p[2])
    elif operator == '>':
        return exp_eval(p[1]) > exp_eval(p[2])
    elif operator == '<=':
        return exp_eval(p[1]) <= exp_eval(p[2])
    elif operator == '>=':
        return exp_eval(p[1]) >= exp_eval(p[2])
    elif operator == '==':
        return exp_eval(p[1]) == exp_eval(p[2])
    elif operator == '!=':
        return exp_eval(p[1]) != exp_eval(p[2])
    elif operator == '&&':
        return exp_eval(p[1]) and exp_eval(p[2])
    elif operator == '||':
        return exp_eval(p[1]) or exp_eval(p[2])
    elif operator == '!':
        return not exp_eval(p[1])
    elif operator == 'UMINUS':
        return (- exp_eval(p[1]))
    elif operator == 'POP':
        return variables[p[1]][1].pop(p[2])
    elif operator == 'PUSH':
        # print(variables[p[1]][1])
        return variables[p[1]][1].append(exp_eval(p[2]))
    elif operator == 'INDEX' or operator == 'ACCESS':
        return variables[p[1]][1][p[2]]
    elif operator == 'SLICE':
        x = slice(p[2], p[3])
        return variables[p[1]][1][x]
    else:
        non_int = str(p[1])
        # non_int_ans = var_val(non_int)
        # if non_int_ans != '':
        #     return non_int_ans
        # print('p1:', p[1])
        if not non_int in variables:
            return p[1]
        else:
            return var_val(p[1])
        
def assign_list(p, var):
    operator = p[0]
    if operator == ",":
        assign_list(p[1], var)
        assign_list(p[2], var)
    else:
        variables[var][1].append(p[1])
    
def var_check(p):
    # print(p)
    # print(str(p[1]))
    var = str(p[1])
    # print('var:',var)
    # print(type(var))
    if (var in variables) == False:
        # print(p[0])
        if p[0] == 'int':
            # print('hrr')
            # print(p[1])
            # print(type(p[1][1]))
            if type(p[1]) == int:
                # print('here')
                return True
            return False
        elif p[0] == 'float':
            if type(p[1]) == float:
                return True
            return False
        elif p[0] == 'char':
            v = p[1].strip("'")
            # print(v)
            # print(len(v))
            if len(v) == 1:
                return True
            return False
        elif p[0] == 'string':
            # print(type(p[1][1]))
            # v = p[1][1].strip('"')
            # if type(p[1][1]) == tuple:
            #     # print('here')
            #     return var_check(p[1][1])
            if type(p[1]) == str:
                return True
            return False
        elif p[0] == 'bool':
            if type(p[1]) == bool:
                return True
            return False
        else:
            return False
    else:
        # print(p[0])
        # print(variables[p[2]][0])
        var_type = variables[var][0]
        if  var_type == p[0]:
            return True
        else:
            return False
        
def exp_assign(p):
    # if p[1] != 'int' and p[1] != 'float' and p[1] != 'bool':
    # print('p2:', p[2])
    ans = exp_eval(p[2])
    exp = (p[1], ans)
    # print('ans:', ans)
    if var_check(exp) == False:
        raise TypeError('TypeError')
    if (p[0] in variables) == True:
        raise TypeError('RedeclerationError')
    if p[1] == 'char' and p[2][0] == 'CHAR':
        val = ans[1].strip("'")
        variables[p[0]] = [p[1], (ans[0], val)]
    else:
        variables[p[0]] = [p[1], ans]    
    
    
def var_val(p):
    # print(p)
    val = variables[p][1]
    # print (val)
    # print(val in variables)
    if variables[p][0] == 'list':
        return val
    if not val in variables:
        # print('here')
        # print('val:', val)
        return val
    else:
        # print('here1')
        var_val(val)
        
def stmt_eval(p):
    # print(p)
    stype = p[0]
    # print(stype)
    if stype == 'PRINT':
        for i in range(1, len(p)):
            exp = p[i]
            # print('exp:', exp)
            # print(len(exp))
            # print(exp[1][0])
            # print(exp[1][1])
            if exp[1][0] == 'NAME':
                # if exp in variables:
                    
                # else:
                #     print(exp, end=' ')
                # print(exp[1][1])
                print(var_val(exp[1][1]), end=' ')
            else:
                print(exp_eval(exp), end=' ')
        print(end='\n')
    elif stype == 'IF-ELSEIF-ELSE':
        # print('here')
        # print(exp_eval(p[1]))
        # print(p[2])
        # print(p[3][3][1])
        # print(exp_eval(p[3][1]))
        # print(p[5])
        if exp_eval(p[1]) == True:
            run_program(p[2])
        elif exp_eval(p[3][1]) == True:
            run_program(p[3][2])
        else:
            run_program(p[3][3][1])
    elif stype == 'DOWHILE':
        run_program(p[1])
        while exp_eval(p[2][1]) == True:
            run_program(p[1])
    elif stype == 'ASSIGN-LIST':
        # print(p[1])
        # print(p[2])
        # print(exp_eval(p[2]).split(" "))
        # print(len(p[2]))
        # variables[p[1]] = exp_eval(p[2]).split(" ")
        variables[p[1]] = ('list', [])
        assign_list(p[2], p[1])
        # print(variables)
    elif stype == 'ASSIGN-EMPTY-LIST':
        variables[p[1]] = ('list', [])
        # print(variables)
    elif stype == 'POP' or stype == 'PUSH' or stype == 'INDEX' or stype == 'SLICE' or stype == 'ACCESS':
        # variables[p[1]].pop(p[2])
        exp_eval(p)
        # print(variables)
    else:
        exp_assign(p)
        # print(variables)

def run_program(p):
    for stmt in p:
        # print ("stmt:", stmt)
        if stmt != None:
            stmt_eval(stmt)
            
if len(sys.argv) == 1:
    print('File name/path not provided as cmd arg.')
    exit(1)

while True:
    fileHandler = open(sys.argv[1], "r")
    userIn = fileHandler.read()
    fileHandler.close()
    
    print("Welcome to your YAPL's Interpreter")
    parsed = parser.parse(userIn)
    if not parsed:
        continue
    
    for line in userIn.split('\n'):
        print(line)
        
    print('===================================\n{OUTPUT}')
    try:
        run_program(parsed)
    except Exception as e:
        print(e)
        
    input("Press any key to run code again")
    
exit()