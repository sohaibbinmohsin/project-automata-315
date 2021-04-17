import ply.lex as lex

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
    'REMAINDER',
    'SEMICOL',
    'PRINT',
    'NAME'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'\\'
t_REMAINDER = r'\%'
t_SEMICOL = r'\;'
t_ignore = '\t\r\n\f\v '

def t_NAME(t): #keywords
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'bool':
        t.type = 'BOOL'
    elif t.value == 'char':
        t.type = 'CHAR'
    elif t.value == 'string':
        t.type = 'STRING'
    else:
        t.type = 'NAME'
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d*\.\d+'
    t.value = float(t.value)
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