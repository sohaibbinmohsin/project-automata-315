import ply.yacc as yacc
from yapl_lexer import *
import sys

start = 'S'

def p_start(p):
    """
        S: stmt S
    """
    p[0] = p[1] + p[2]
    
def p_start_empty(p):
    """
        S:
    """
    p[0] = []
    
def p_print_stat(p):
    """
        stmt: PRINT exp SEMICOL
    """
    p[0] = ('PRINT', p[2])
    
def p_exp_bin(p):
    """
        exp: exp PLUS exp
    """
    p[0] = (p[2], p[1], p[3])
    
def p_exp_num(p):
    """
        exp: INT
            | FLOAT
    """
    p[0] = p[1]
    
def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)
    
parser = yacc.yacc()