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

def t_lineno(t):
    r'\n'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("[Lexer Error] Line", t.lineno)
    print(f"Illegal character: {t.value}")
    t.lexer.skip(1)
    
lexer = lex.lex()

while True:
    print("YAPL_LEXER>>", end='')
    lexer.input(input())
    
    while True:
        tokenEntered = lexer.token()
        if not tokenEntered:
            break
        print(tokenEntered)