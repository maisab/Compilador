import ply.yacc as yacc
from lex import tokens

class Tree:

    def __init__(self, type_node, child=[], value=''):
        self.type = type_node
        self.child = child
        self.value = value

    def __str__(self):
        return self.type

#uma funcao
def p_programa_principal(p):
    'programa : principal'
    p[0] = Tree('programa', [p[1]])

#mais de uma funcao
def p_programa_multiplas(p):
    'programa : func_loop principal'
    p[0] = Tree('programa', [p[1],p[2]])

#funcao principal
def p_principal(p):
    'principal : tipo PRINCIPAL ABRE_PAR FECHA_PAR sequencia_decl FIM'
    p[0] = Tree('principal', [p[1],p[5]])

#uma funcao
def p_func_loop_unica(p):
    'func_loop : func_decl'
    p[0] = Tree('func_loop', [p[1]])

#mais de uma funcao
def p_func_loop_multiplas(p):
    'func_loop : func_decl func_loop'
    p[0] = Tree('func_loop', [p[1], p[2]])

#funcao
def p_func_decl(p):
    'func_decl : tipo ID ABRE_PAR parametro_decl FECHA_PAR sequencia_decl RETORNA ABRE_PAR ID FECHA_PAR FIM'
    p[0] = Tree('func_decl', [p[1], p[4],p[6]], [[p[2], p[9]])

#uma declaracao
def p_sequencia_decl_declaracao(p):
    'sequencia_decl : declaracao'
    p[0] = Tree('sequencia_decl', [p[1]])

#mais de uma declaracao
def p_sequencia_decl_loop(p):
    'sequencia_decl : declaracao sequencia_decl'
    p[0] = Tree('sequencia_decl', [p[1], p[2]])

def p_declaracao_1(p):
    'declaracao : se_decl'
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_2(p):
    'declaracao : repita_decl'
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_3(p):
    'declaracao : atribuicao_decl'
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_4(p):
    'declaracao : leia_decl'
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_5(p):
    'declaracao : escreva_decl'
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_6(p):
    'declaracao : declara_var'
    p[0] = Tree('declaracao', [p[1]])

def p_se_decl_1(p):
    'se_decl : SE exp_decl ENTAO sequencia_decl FIM'
    p[0] = Tree('se_decl', [p[2], p[4]])

def p_se_decl_2(p):
    'se_decl : SE exp_decl ENTAO sequencia_decl SENAO sequencia_decl FIM'
    p[0] = Tree('se_decl', [p[2], p[4], p[6]])

def p_repita_decl(p):
    'repita_decl : REPITA seq_decl ATE exp_decl'
    p[0] = Tree('repita_decl', [p[2], p[4]])

def p_atribuicao_decl(p):
    'atribuicao_decl : ID ATRIBUICAO exp_decl'
    p[0] = Tree('atribuicao_decl', [p[3]], p[1])

def p_leia_decl(p):
    'leia_decl : LEIA ID'
    p[0] = Tree('leia_decl', [], p[1])

def p_escreva_decl(p):
    'escreva_decl : ESCREVA exp_decl'
    p[0] = Tree('leia_decl', [], p[1])

def p_exp_decl_simples(p):
    'exp_decl : simples_exp'
    p[0] = Tree('exp_decl', [p[1]])

def p_exp_decl_composta(p):
    'exp_decl : simples_exp compara_op simples_exp'
    p[0] = Tree('exp_decl', [p[1], p[2], p[3]])

def p_compara_op_1(p):
    'compara_op : IGUAL'
    p[0] = Tree('compara_op', [], p[1])

def p_compara_op_2(p):
    'compara_op : MENOR'
    p[0] = Tree('compara_op', [], p[1])

def p_compara_op_3(p):
    'compara_op : MAIOR'
    p[0] = Tree('compara_op', [], p[1])

def p_compara_op_4(p):
    'compara_op : MENOR_IGUAL'
    p[0] = Tree('compara_op', [], p[1])

def p_compara_op_5(p):
    'compara_op : MAIOR_IGUAL'
    p[0] = Tree('compara_op', [], p[1])

def p_simples_exp_1(p):
    'simples_exp : termo'
    p[0] = Tree('simples_exp', [p[1]])

def p_simples_exp_2(p):
    'simples_exp : simples_exp soma_sub termo'
    p[0] = Tree('simples_exp', [p[1], p[2], p[3]])

def p_soma_sub_1(p):
    'soma_sub : SOMA'
    p[0] = Tree('soma_sub', [], p[1])

def p_soma_sub_2(p):
    'soma_sub : SUB'
    p[0] = Tree('soma_sub', [], p[1])

def p_termo_1(p):
    'termo : fator'
    p[0] = Tree('termo', [p[1]])

def p_termo_2(p):
    'termo : termo mult_div fator'
    p[0] = Tree('termo', [p[1], p[2], p[3]])

def p_mult_div_1(p):
    'mult_div : MULT'
    p[0] = Tree('mult_div', [], p[1])

def p_mult_div_2(p):
    'mult_div : DIVISAO'
    p[0] = Tree('mult_div', [], p[1])

def p_fator_1(p):
    'fator : ID'
    p[0] = Tree('fator', [], p[1])

def p_fator_2(p):
    'fator : ABRE_PAR exp_decl FECHA_PAR'
    p[0] = Tree('fator', [p[2]])

def p_declara_var(p):
    'declara_var : ID DOIS_PONTOS ID'
    p[0] = Tree('declara_var', [], [p[1], p[2]])

def p_parametro_decl_1(p):
    'parametro_decl : declara_var VIRGULA parametro_decl'
    p[0] = Tree('parametro_decl', [p[1], p[3]])

def p_parametro_decl_2(p):
    'parametro_decl : declara_var'
    p[0] = Tree('parametro_decl', [p[1]])

def p_tipo_1(p):
    'tipo : VAZIO'
    p[0] = Tree('tipo', [], p[1])

def p_tipo_2(p):
    'tipo : N_INTEIRO'
    p[0] = Tree('tipo', [], p[1])

def p_tipo_2(p):
    'tipo : N_FLUTUANTE'
    p[0] = Tree('tipo', [], p[1])

