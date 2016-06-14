import ply.yacc as yacc
from lex import tokens

class Tree:

    def __init__(self, type_node, child=[], value=None):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self, level = 0):
        ret = "| "*level + repr(self.type)+"\n"
        for child in self.child:
#            print("Passou \n")
#            contador = contador + 1
            ret += child.__str__(level + 1)
        return ret

precedence = (
    ('left', 'SOMA', 'SUB'),
    ('left', 'MULT', 'DIVISAO'),
)

#uma funcao
def p_programa_1(p):
    'programa : principal'
    p[0] = Tree('programa_principal', [p[1]])

#mais de uma funcao
def p_programa_2(p):
    'programa : func_loop principal'
    p[0] = Tree('programa_funcao', [p[1],p[2]])

#variavel global
def p_programa_3(p):
    'programa : declara_var programa'
    p[0] = Tree('programa_varglobal', [p[1],p[2]])

#funcao principal
def p_principal(p):
    'principal : VAZIO PRINCIPAL ABRE_PAR FECHA_PAR NOVA_LINHA sequencia_decl FIM'
    p[0] = Tree('principal', [p[6]])

#uma funcao
def p_func_loop_1(p):
    'func_loop : func_decl'
    p[0] = Tree('func_loop', [p[1]])

#mais de uma funcao
def p_func_loop_2(p):
    'func_loop : func_loop func_decl'
    p[0] = Tree('func_loop_loop', [p[1], p[2]])

#funcao
def p_func_decl(p):
    'func_decl : tipo ID ABRE_PAR parametro_decl FECHA_PAR NOVA_LINHA sequencia_decl FIM NOVA_LINHA'
    p[0] = Tree('func_decl', [p[1], p[4], p[7]], p[2])

#uma declaracao
def p_sequencia_decl_1(p):
    'sequencia_decl : declaracao'
    p[0] = Tree('sequencia_decl', [p[1]])

#mais de uma declaracao
def p_sequencia_decl_2(p):
    'sequencia_decl : sequencia_decl declaracao'
    p[0] = Tree('sequencia_decl_loop', [p[1], p[2]])

def p_declaracao_1(p):
    'declaracao : se_decl'
    p[0] = Tree('declaracao_se', [p[1]])

def p_declaracao_2(p):
    'declaracao : repita_decl'
    p[0] = Tree('declaracao_repita', [p[1]])

def p_declaracao_3(p):
    'declaracao : atribuicao_decl'
    p[0] = Tree('declaracao_atribuicao', [p[1]])

def p_declaracao_4(p):
    'declaracao : leia_decl'
    p[0] = Tree('declaracao_leia', [p[1]])

def p_declaracao_5(p):
    'declaracao : escreva_decl'
    p[0] = Tree('declaracao_escreva', [p[1]])

def p_declaracao_6(p):
    'declaracao : declara_var'
    p[0] = Tree('declaracao_declaravar', [p[1]])

#retorna em outra parte do codigo
def p_declaracao_7(p):
    'declaracao : retorna_decl'
    p[0] = Tree('declaracao_retorna', [p[1]])

def p_declaracao_8(p):
    'declaracao : chamada_func'
    p[0] = Tree('declaracao_chamafunc', [p[1]])


def p_retorna_decl_1(p):
    'retorna_decl : RETORNA ABRE_PAR ID FECHA_PAR NOVA_LINHA'
    p[0] = Tree('retorna_id', [], p[3])

def p_retorna_decl_2(p):
    'retorna_decl : RETORNA ABRE_PAR numero_decl FECHA_PAR NOVA_LINHA'
    p[0] = Tree('retorna_numero', [p[3]])

def p_numero_1(p):
    'numero_decl : INTEIRO'
    p[0] = Tree('numero_decl_inteiro', [], p[1])

def p_numero_2(p):
    'numero_decl : FLUTUANTE'
    p[0] = Tree('numero_decl_flutuante', [], p[1])

def p_se_decl_1(p):
    'se_decl : SE exp_decl ENTAO NOVA_LINHA sequencia_decl FIM NOVA_LINHA'
    p[0] = Tree('se_decl', [p[2], p[5]])

def p_se_decl_2(p):
    'se_decl : SE exp_decl ENTAO NOVA_LINHA sequencia_decl SENAO NOVA_LINHA sequencia_decl FIM NOVA_LINHA'
    p[0] = Tree('se_decl_senao', [p[2], p[5], p[8]])

def p_repita_decl(p):
    'repita_decl : REPITA NOVA_LINHA sequencia_decl ATE exp_decl NOVA_LINHA'
    p[0] = Tree('repita_decl', [p[3], p[5]])

def p_atribuicao_decl(p):
    'atribuicao_decl : ID ATRIBUICAO exp_decl NOVA_LINHA'
    p[0] = Tree('atribuicao_decl', [p[3]], p[1])

def p_leia_decl(p):
    'leia_decl : LEIA ABRE_PAR ID FECHA_PAR NOVA_LINHA'
    p[0] = Tree('leia_decl', [], p[3])

def p_escreva_decl_1(p):
    'escreva_decl : ESCREVA ABRE_PAR exp_decl FECHA_PAR NOVA_LINHA'
    p[0] = Tree('escreva_decl_exp', [p[3]])

def p_escreva_decl_2(p):
    'escreva_decl : ESCREVA ABRE_PAR chamada_func_escreva FECHA_PAR NOVA_LINHA'
    p[0] = Tree('escreva_decl', [p[3]])

def p_chamada_func(p):
    'chamada_func : ID ABRE_PAR parametro_chama_func FECHA_PAR NOVA_LINHA'
    p[0] = Tree('chamada_func', [p[3]], p[1])

def p_chamada_func_escreva(p):
    'chamada_func_escreva : ID ABRE_PAR parametro_chama_func FECHA_PAR'
    p[0] = Tree('chamada_func_escreva', [p[3]], p[1])

def p_parametro_chama_func_1(p):
    'parametro_chama_func : parametro_chama_func VIRGULA ID'
    p[0] = Tree('parametro_chama_func_paramentros', [p[1]], p[3])

def p_parametro_chama_func_2(p):
    'parametro_chama_func : parametro_chama_func VIRGULA numero_decl'
    p[0] = Tree('parametro_chama_func_numeros', [p[1]], p[3])

def p_parametro_chama_func_3(p):
    'parametro_chama_func : ID'
    p[0] = Tree('parametro_chama_func', [], p[1])

def p_parametro_chama_func_4(p):
    'parametro_chama_func : numero_decl'
    p[0] = Tree('parametro_chama_func_num', [p[1]])

def p_exp_decl_1(p):
    'exp_decl : simples_exp'
    p[0] = Tree('exp_decl', [p[1]])

def p_exp_decl_2(p):
    'exp_decl : simples_exp compara_op simples_exp'
    p[0] = Tree('exp_decl_compara', [p[1], p[2], p[3]])

def p_compara_op_1(p):
    'compara_op : IGUAL'
    p[0] = Tree('compara_op_igual', [], p[1])

def p_compara_op_2(p):
    'compara_op : MENOR'
    p[0] = Tree('compara_op_menor', [], p[1])

def p_compara_op_3(p):
    'compara_op : MAIOR'
    p[0] = Tree('compara_op_maior', [], p[1])

def p_compara_op_4(p):
    'compara_op : MENOR_IGUAL'
    p[0] = Tree('compara_op_menorIgual', [], p[1])

def p_compara_op_5(p):
    'compara_op : MAIOR_IGUAL'
    p[0] = Tree('compara_op_maiorIgual', [], p[1])

def p_simples_exp_1(p):
    'simples_exp : termo'
    p[0] = Tree('simples_exp', [p[1]])

def p_simples_exp_2(p):
    'simples_exp : simples_exp soma_sub termo'
    p[0] = Tree('simples_exp_somasub', [p[1], p[2], p[3]])

def p_soma_sub_1(p):
    'soma_sub : SOMA'
    p[0] = Tree('soma_sub_soma', [], p[1])

def p_soma_sub_2(p):
    'soma_sub : SUB'
    p[0] = Tree('soma_sub_subtracao', [], p[1])

def p_termo_1(p):
    'termo : fator'
    p[0] = Tree('termo_fator', [p[1]])

def p_termo_2(p):
    'termo : termo mult_div fator'
    p[0] = Tree('termo_multdiv', [p[1], p[2], p[3]])

def p_mult_div_1(p):
    'mult_div : MULT'
    p[0] = Tree('mult_div_multiplicacao', [], p[1])

def p_mult_div_2(p):
    'mult_div : DIVISAO'
    p[0] = Tree('mult_div_divisao', [], p[1])

def p_fator_1(p):
    'fator : ID'
    p[0] = Tree('fator_id', [], p[1])

def p_fator_2(p):
    'fator : numero_decl'
    p[0] = Tree('fator_numero', [p[1]])

def p_fator_3(p):
    'fator : ABRE_PAR exp_decl FECHA_PAR'
    p[0] = Tree('fator_exp', [p[2]])

def p_declara_var(p):
    'declara_var : tipo DOIS_PONTOS ID NOVA_LINHA'
    p[0] = Tree('declara_var', [p[1]], p[3])

def p_parametro_decl_1(p):
    'parametro_decl : parametro_decl  VIRGULA tipo DOIS_PONTOS ID'
    p[0] = Tree('parametro_decl_loop', [p[1], p[3]], p[5])

def p_parametro_decl_2(p):
    'parametro_decl : tipo DOIS_PONTOS ID'
    p[0] = Tree('parametro_decl', [p[1]], p[3])

def p_tipo_1(p):
    'tipo : VAZIO'
    p[0] = Tree('tipo_vazio', [], p[1])

def p_tipo_2(p):
    'tipo : INTEIRO'
    p[0] = Tree('tipo_inteiro', [], p[1])

def p_tipo_3(p):
    'tipo : FLUTUANTE'
    p[0] = Tree('tipo_flutuante', [], p[1])

def p_error(p):
    if p:
        print("Erro sintático: '%s', linha %d" % (p.value, p.lineno))
        exit(1)
        #p.lexer.skip(1)
    else:
        yacc.restart()
        print('Erro sintático: definições incompletas!')
        exit(1)
        #p.lexer.skip(1)

def parse_tree(code):
    parser = yacc.yacc(debug=True)
    return parser.parse(code)

if __name__ == '__main__':
    import sys
    parser = yacc.yacc(debug=True)
    code = open(sys.argv[1])
    if 'a' in sys.argv:
        print(parser.parse(code.read()))
    else:
        parser.parse(code.read())
