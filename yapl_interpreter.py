from yapl_lexer import *
from yapl_parser import *
import sys

variables = {}

def exp_eval(p):
    operator = p[0]
    # print(operator)
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
    else:
        return p[1]
    
def var_check(p):
    # print(p)
    var = str(p[1])
    if (var in variables) == False:
        # print(p[0])
        if p[0] == 'int':
            if type(p[1][1]) == int:
                return True
            return False
        elif p[0] == 'float':
            if type(p[1][1]) == float:
                return True
            return False
        elif p[0] == 'char':
            v = p[1][1].strip("'")
            # print(v)
            # print(len(v))
            if len(v) == 1:
                return True
            return False
        elif p[0] == 'string':
            # print(type(p[1][1]))
            v = p[1][1].strip('"')
            if type(v) == str:
                return True
            return False
        elif p[0] == 'bool':
            if type(p[1][1]) == bool:
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
    exp = (p[1], p[2])
    if var_check(exp) == False:
        raise TypeError('TypeError')
    if (p[0] in variables) == True:
        raise TypeError('RedeclerationError')
    if p[1] == 'char' and p[2][0] == 'CHAR':
        val = p[2][1].strip("'")
        variables[p[0]] = [p[1], (p[2][0], val)]
    else:
        variables[p[0]] = [p[1], p[2]]    
    
    
def var_val(p):
    val = variables[p][1][1]
    if val in variables == False:
        return val
    else:
        var_val(val)
    

def stmt_eval(p):
    # print(p)
    stype = p[0]
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
                print(var_val(exp[1][1]))
            else:
                print(exp_eval(exp), end=' ')
        print()
    else:
        exp_assign(p)
        # print(variables)

def run_program(p):
    for stmt in p:
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