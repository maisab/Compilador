import ply.lex as lex

# Dicionario reservadas
reservadas = {
    'se':'SE',
    'então':'ENTAO',
    'senão':'SENAO',
    'fim':'FIM',
    'repita':'REPITA',
    'vazio':'VAZIO',
    'até':'ATE',
    'leia':'LEIA',
    'escreva':'ESCREVA',
    'retorna':'RETORNA',
    'principal':'PRINCIPAL',
    'inteiro' : 'INTEIRO',
    'flutuante' : 'FLUTUANTE'
    }

# Lista de Tokens
tokens = [
    'SOMA', 'SUB', 'MULT', 'DIVISAO', 'IGUAL', 'VIRGULA', 'ATRIBUICAO',
    'MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL', 'ABRE_PAR', 'FECHA_PAR', 'DOIS_PONTOS', 'ID',
    'NOVA_LINHA'] + list(reservadas.values())

# Expressões simples

t_SOMA      = r'\+'
t_SUB     = r'-'
t_MULT     = r'\*'
t_DIVISAO   = r'\/'
t_IGUAL     = r'\='
t_VIRGULA   = r'\,'
t_ATRIBUICAO = r':\='
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_MENOR_IGUAL = r'<='
t_MAIOR_IGUAL = r'>='
t_ABRE_PAR = r'\('
t_FECHA_PAR = r'\)'
t_DOIS_PONTOS = r':'

def t_ID(t):
    r'[a-zA-Zà-ú][0-9a-zà-úA-Z]*'
    t.type = reservadas.get(t.value,'ID')
    return t

def t_FLUTUANTE(t):
    r'[0-9]+(\.[0-9]+)(e(\+|\-)?(\d+))?'
    t.value = float(t.value)
    return t

def t_INTEIRO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMENTARIO(t):
    r'{[^\{^\}]*}'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NOVA_LINHA"
    return t

#Ignora tabs e espacos
t_ignore  = ' \t'

# Erro
def t_error(t):
    print ("Erro '%s', linha %d" %(t.value[0], t.lineno))
    print (type(t.value))
    #t.lexer.skip(1)
    exit(0)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    import sys
    code = open(sys.argv[1])
    lex.input(code.read())
    while True:
        tok = lex.token()
        if not tok:
            break
        print (tok)
