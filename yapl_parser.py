import ply.yacc as yacc
from yapl_lexer import *

#sys.tracebacklimit = 0 # to prevent traceback debug output since it is not needed

precedence = (
    (('right', 'UMINUS'),
    ('AND', 'OR', 'NOT'),
    ('left', 'EQUALTO', 'NOTEQUALTO'),
    ('left', 'LESSTHANOREQUALTO', 'GREATERTHANOREQUALTO'),
    ('left', 'LESSTHAN', 'GREATERTHAN'), 
    ('left', 'INCREMENT', 'DECREMENT'),
    ('left', 'MULTIPLICATION', 'DIVISION','MODULO'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'POW'),
    ('left', 'LPAREN', 'RPAREN'),
))

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

def p_exp_paren(p):
    'exp : LPAREN exp RPAREN'
    p[0] = ('PAREN', p[2])

def p_print_stmt(p):
    """
    stmt : PRINT exp COMMA exp SEMICOL
         | PRINT exp SEMICOL
         | PRINT LPAREN exp RPAREN SEMICOL
    """
    # if len(p) == 5:
        
    if len(p) == 4:
        p[0] = ('PRINT', p[2])
    else:
        # p[0] = ('PRINT', p[2], p[4])
        p[0] = ('PRINT', p[3])
    
def p_var_assign(p):
    """
    stmt : VARTYPE NAME ASSIGN exp SEMICOL
         | VARTYPE NAME ASSIGN stmt SEMICOL
         | NAME ASSIGN exp SEMICOL
         | VARTYPE NAME
    """
    if len(p) == 5:
        p[0] = ('ASSIGN', p[1], p[3])
    elif len(p) == 3:
        p[0] = ('EMPTY-VAR', p[1], p[2])
    else: 
        p[0] = (p[2], p[1], p[4])
    
def p_exp_float(p):
    """
    exp : FLOAT
    """
    p[0] = ('FLOAT', p[1])
    
def p_exp_num(p):
    """
    exp : INT
    """
    p[0] = ('NUM', p[1])
    
def p_exp_bool(p):
    """
    exp : BOOL
    """
    p[0] = ('BOOL', p[1])
    
def p_exp_char(p):
    """
    exp : CHAR
    """
    p[0] = ('CHAR', p[1])
    
def p_INCREMENT(p):
    """
    stmt : NAME INCREMENT SEMICOL
    """
    p[0] = ('INCREMENT', p[1])
    
def p_DECREMENT(p):
    """
    stmt : NAME DECREMENT SEMICOL
    """
    p[0] = ('DECREMENT', p[1])
    
def p_LIST_ACCESS(p):
    """
    exp : NAME LSQB INT RSQB
    """
    p[0] = ('ACCESS', p[1], p[3])
    
def p_LIST_POP(p):
    """
    exp : NAME POP LPAREN INT RPAREN
    """
    p[0] = ('POP', p[1], p[4])
    
def p_LIST_INDEX(p):
    """
    exp : NAME INDEX LPAREN INT RPAREN
    """
    p[0] = ('INDEX', p[1], p[4])
    
def p_LIST_SLICE(p):
    """
    exp : NAME SLICE LPAREN INT COMMA INT RPAREN
    """
    p[0] = ('SLICE', p[1], p[4], p[6])
    
def p_LIST_PUSH(p):
    """
    stmt : NAME PUSH LPAREN exp RPAREN SEMICOL
    """
    p[0] = ('PUSH', p[1], p[4])
    
def p_exp_name(p):
    """
    exp : NAME
    """
    p[0] = ('NAME', p[1])
    
def p_NOT(p):
    """
    exp : NOT exp
    """
    p[0] = ('NOT', p[2])

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
        | exp COMMA exp
        | exp AND exp
        | exp OR exp
        | exp POW exp
        | STRING
    """
    if len(p) > 3:
        p[0] = (p[2], p[1], p[3])
    elif len(p) == 2:
        p[0] = ('STRING', p[1])
    else:
        p[0] = (p[2], p[1])

def p_exp_uminus(p):
     'exp : MINUS exp %prec UMINUS'
     p[0] = ('UMINUS', p[2])
     
def p_LIST(p):
    """
    stmt : LIST NAME ASSIGN LSQB exp RSQB SEMICOL
         | LIST NAME ASSIGN LSQB RSQB SEMICOL
    """
    if len(p) == 7:
        p[0] = ('ASSIGN-EMPTY-LIST', p[2])
    else:
        p[0] = ('ASSIGN-LIST', p[2], p[5])

def p_IF(p):
    """
    stmt : IF LPAREN exp RPAREN LCURLY S RCURLY block
    """
    p[0] = ('IF-ELSEIF-ELSE', p[3], p[6], p[8])
    
def p_ELSEIF(p):
    """
    block : ELSEIF LPAREN exp RPAREN LCURLY S RCURLY block
    """
    p[0] = ('IF-ELSEIF-ELSE', p[3], p[6], p[8])
    
def p_ELSE(p):
    """
    block : ELSE LCURLY S RCURLY
    """
    p[0] = ('IF-ELSEIF-ELSE', p[3])
    
def p_ELSE_EMPTY(p):
    """
    block : 
    """
    p[0] = []
    
def p_DO(p):
    """
    stmt : DO LCURLY S RCURLY block_w
    """
    p[0] = ('DOWHILE', p[3], p[5])
    
def p_WHILE(p):
    """
    block_w : WHILE LPAREN exp RPAREN SEMICOL
    """
    p[0] = ('DOWHILE', p[3])
    
def p_FUNCTION(p):
    """
    stmt : FUNCTION NAME LPAREN stmt RPAREN LCURLY S RCURLY
    """
    p[0] = ('FUNCTION', p[2], p[4], p[7])
    
def p_RETURN(p):
    """
    stmt : RETURN LPAREN exp RPAREN SEMICOL
    """
    p[0] = ('RETURN', p[3])
    
def p_CALL(p):
    """
    exp : NAME LPAREN exp RPAREN
    """
    p[0] = ('CALL', p[1], p[3])

def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)

parser = yacc.yacc() 