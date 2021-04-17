from yapl_lexer import *
from yapl_parser import *
import sys

def exp_eval(p):
    operator = p[0]
    if operator == '+':
        return exp_eval(p[1]) + exp_eval(p[2])
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
    else:
        return p[1] 

def stmt_eval(p):
    stype = p[0]
    if stype == 'PRINT':
        exp = p[1]
        print(exp_eval(exp))

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