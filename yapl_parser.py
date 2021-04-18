import ply.yacc as yacc
from yapl_lexer import *

#sys.tracebacklimit = 0 # to prevent traceback debug output since it is not needed

precedence = (
    ('right', 'INCREMENT', 'DECREMENT', 'POW', 'MULTIPLICATION', 'DIVISION', 'MODULO', 'PLUS', 'MINUS', 'LESSTHAN', 'GREATERTHAN', 'LESSTHANOREQUALTO', 'GREATERTHANOREQUALTO', 'EQUALTO', 'NOTEQUALTO', 'AND', 'OR', 'NOT'), ('right', 'UMINUS'),
)

variables = {}
functions = {}

start = 'S'

def p_start(p): 
    """
    S : stmt S
    """
    p[0] = [p[1]] + p[2] 
    

def p_start_empty(p):
    """
    S :
    """
    p[0] = []


def p_print_stmt(p):
    """
    stmt : PRINT exp SEMICOL
    """
    p[0] = ('PRINT', p[2])
    
def p_var_assign(p):
    """
    stmt: INT NAME ASSIGN exp SEMICOL
        | FLOAT NAME ASSIGN exp SEMICOL
        | CHAR NAME ASSIGN exp SEMICOL
        | STRING NAME ASSIGN exp SEMICOL
        | BOOL NAME ASSIGN exp SEMICOL
        | FLOAT NAME ASSIGN FLOAT SEMICOL
        | INT NAME ASSIGN INT SEMICOL
        | STRING NAME ASSIGN STRING SEMICOL
        | CHAR NAME ASSIGN CHAR SEMICOL
        | BOOL NAME ASSIGN BOOL SEMICOL
    """


def p_exp_bin(p):
    """ 
    exp : exp PLUS exp
        | exp MINUS exp
        | exp MULTIPLICATION exp
        | exp DIVISION exp
        | exp MODULO exp
        | exp GREATERTHAN exp
        | exp LESSTHAN exp
        | exp GREATERTHANOREQUALTO exp
        | exp LESSTHANOREQUALTO exp
        | exp EQUALTO exp
        | exp NOTEQUALTO exp
        | exp AND exp
        | exp OR exp
        | exp POW exp
        | exp INCREMENT
        | exp DECREMENT
        | exp NOT
        | STRING
    """
    if len(p) > 3:
        p[0] = (p[2], p[1], p[3])
    elif len(p) == 2:
        p[0] = ('STRING', p[1])
    else:
        p[0] = (p[2], p[1])

def p_exp_num(p):
    """
    exp : INT
    """
    p[0] = ('NUM', p[1])
    
def p_exp_uminus(p):
     'exp : MINUS exp %prec UMINUS'
     p[0] = ('UMINUS', p[2])

def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)

parser = yacc.yacc() 