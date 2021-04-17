import ply.lex as lex

tokens = [
    'INT',
    'FLOAT',
    'CHAR'
    'STRING',
    'BOOL',
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'DIVISION',
    'REMAINDER',
    'SEMICOLON',
    'PRINT'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'\\'
t_REMAINDER = r'\%'
t_SEMICOLON = r'\;'
t_ignore = '\t\r\n\f\v '

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
    return t