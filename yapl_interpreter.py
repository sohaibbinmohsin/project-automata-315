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
    
def var_info(p):
    print(p)
    if (p[2] in variables) == False:
        if p[0] == p[1]:
            return True
        else:
            return False
    else:
        print(p[0])
        print(variables[p[2]][0])
        if variables[p[2]][0] == p[0]:
            return True
        else:
            return False
        
def exp_assign(p):
    # if p[1] != 'int' and p[1] != 'float' and p[1] != 'bool':
    exp = (p[1], p[2], str(p[3]))
    if var_info(exp) == False:
        raise TypeError('TypeError')
    if (p[0] in variables) == True:
        raise TypeError('RedeclerationError')
    variables[p[0]] = [p[1], p[3]]

def stmt_eval(p):
    print(p)
    stype = p[0]
    if stype == 'PRINT':
        for i in range(1, len(p)):
            exp = p[i]
            if len(exp) == 1:
                if variables[exp].has_key():
                    print(var_info(exp))
                else:
                    print(exp, end=' ')
            else:
                print(exp_eval(exp), end=' ')
        print()
    else:
        exp_assign(p)
        print(variables)

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