import ply.lex as lex
import re

tokens = [
    'INT',
    'FLOAT',
    'CHAR',
    'STRING',
    'BOOL',
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'DIVISION',
    'MODULO',
    'POW',
    'INCREMENT',
    'DECREMENT',
    'SEMICOL',
    'NAME',
    'PRINT',
    'LESSTHAN',
    'GREATERTHAN',
    'LESSTHANOREQUALTO',
    'GREATERTHANOREQUALTO',
    'NOTEQUALTO',
    'EQUALTO',
    'NOT',
    'AND',
    'OR',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'IF',
    'ELSEIF',
    'ELSE',
    'DO',
    'WHILE',
    'FUNCTION',
    'RETURN',
    'ASSIGN',
    'COMMA',
    'VARTYPE',
    'LSQB',
    'RSQB',
    'LIST',
    'POP',
    'PUSH',
    'INDEX',
    'SLICE'
]

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_AND = r'\&\&'
t_OR = r'\|\|'
t_EQUALTO = r'\=\='
t_NOTEQUALTO = r'\!\='
t_NOT = r'\!'
t_LESSTHANOREQUALTO = r'\<\='
t_GREATERTHANOREQUALTO = r'\>\='
t_LESSTHAN = r'\<'
t_GREATERTHAN = r'\>'
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'\/'
t_MODULO = r'\%'
t_POW = r'\^'
t_SEMICOL = r'\;'
t_ignore = '\t\r\n\f\v '
t_ignore_COMMENT = r'\#.*'
t_ASSIGN = r'\='
t_COMMA = r'\,'
t_LSQB = r'\['
t_RSQB = r'\]'

def t_VARTYPE(t):
    r'int|float|char|string|bool'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_POP(t):
    r'.pop'
    return t

def t_PUSH(t):
    r'.push'
    return t

def t_INDEX(t):
    r'.index'
    return t

def t_SLICE(t):
    r'.slice'
    return t

def t_LIST(t):
    r'list'
    return t

def t_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'true|false'
    if t.value == 'true':
        t.value = True
    else:
        t.value = False
    return t

def t_STRING(t):
    r'\".*?\"'
    t.value = t.value.strip('"')
    # print(t)
    return t

def t_CHAR(t):
    r'\'[a-zA-Z0-9]*\''
    # t.value = t.value.strip("'")
    return t

def t_NAME(t): #keywords
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'if':
        t.type = 'IF'
    elif t.value == 'elseif':
        t.type = 'ELSEIF'
    elif t.value == 'else':
        t.type = 'ELSE'
    elif t.value == 'do':
        t.type = 'DO'
    elif t.value == 'while':
        t.type = 'WHILE'
    elif t.value == 'def':
        t.type = 'DEF'
    else:
        t.type = 'NAME'
    return t

def t_lineno(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("[Lexer Error] Line", t.lineno)
    print(f"Illegal character: {t.value}")
    t.lexer.skip(1)
    
lexer = lex.lex()

# while True:
#     print("YAPL_LEXER>>", end='')
#     lexer.input(input())
    
#     while True:
#         tokenEntered = lexer.token()
#         if not tokenEntered:
#             break
#         print(tokenEntered)