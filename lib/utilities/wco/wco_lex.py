tokens = (
    'STRING', 'NAME', 'LPAREN', 'RPAREN', 'COMMENT'
    )
t_STRING = r'\"[^"]*\"'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME = r'\w+'
t_COMMENT = r'\#.*'
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.skip(1)
