from parser import *
#import collections

#falar no relatorio

class Semantica():

    def __init__(self, codigo):
        self.table = {}
        self.scope = "global"
        self.tree = parse_tree(codigo)

    def raiz(self):
        if(self.tree.type == "programa_principal"):
            self.scope = "principal"
            self.principal(self.tree.child[0])
            self.scope = "global"

        if(self.tree.type == "programa_funcao"):
            self.func_loop(self.tree.child[0])
            self.principal(self.tree.child[1])

        if(self.tree.type == "programa_varglobal"):
            self.declara_var(self.tree.child[0])
            self.programa(self.tree.child[1])

# def p_programa_1(p):
#     'programa : principal'
#     p[0] = Tree('programa_principal', [p[1]])

# #mais de uma funcao
# def p_programa_2(p):
#     'programa : func_loop principal'
#     p[0] = Tree('programa_funcao', [p[1],p[2]])

# #variavel global
# def p_programa_3(p):
#     'programa : declara_var programa'
#     p[0] = Tree('programa_varglobal', [p[1],p[2]])

# def p_programa_3(p):
#     'programa : declara_var programa'
#     p[0] = Tree('programa_varglobal', [p[1],p[2]])
    def programa(self, node):
        if(node.type == "programa_principal"):
            self.scope = "principal"
            self.principal(node.child[0])
            self.scope = "global"

        if(node.type  == "programa_funcao"):
            self.func_loop(node.child[0])
            self.principal(node.child[1])

        if(node.type  == "programa_varglobal"):
            self.declara_var(node.child[0])
            self.programa(node.child[1])

# def p_principal(p):
#     'principal : VAZIO PRINCIPAL ABRE_PAR FECHA_PAR NOVA_LINHA sequencia_decl FIM'
#     p[0] = Tree('principal', [p[6]])

    def principal(self, node):
        self.scope = "principal"
        self.sequencia_decl(node.child[0])

        self.scope = "global"

# def p_func_loop_1(p):
#     'func_loop : func_decl'
#     p[0] = Tree('func_loop', [p[1]])

# def p_func_loop_2(p):
#     'func_loop : func_loop func_decl'
#     p[0] = Tree('func_loop_loop', [p[1], p[2]])

    def func_loop(self, node):
        #if(node.child == func_decl)
        if(len(node.child) == 2) :
            self.func_loop(node.child[0])
            self.func_decl(node.child[1])
        else:
            self.func_decl(node.child[0])

# def p_func_decl(p):
#     'func_decl : tipo ID ABRE_PAR parametro_decl FECHA_PAR NOVA_LINHA sequencia_decl FIM NOVA_LINHA'
#     p[0] = Tree('func_decl', [p[1], p[4], p[7]], [p[2]])

    def func_decl(self, node):
        if(node.value in self.table.keys()): #se ja tem funcao com esse nome na tabela
            print("Erro Semântico, o nome "+  node.value + " já esta sendo utilizado")
            exit(1)

        tipo = ""

        if self.tipo(node.child[0]) == 1:
            tipo = "INTEIRO"

        elif self.tipo(node.child[0]) == 2:
            tipo = "FLUTUANTE"

        elif self.tipo(node.child[0]) == 3:
            tipo = "VAZIO"

        self.table[node.value] = {}
        self.table[node.value]["var"] = False
        self.table[node.value]["tipo"] = tipo
        self.table[node.value]["num_parametros"] = 0

        self.sequencia_decl(node.child[2])
        self.scope = node.value  #escopo nome da função
        self.table[node.value]["num_parametros"] = self.parametro_decl(node.child[1]) #recebe a quantidade de parametros declarados

        self.scope = "global"

# def p_sequencia_decl_1(p):
#     'sequencia_decl : declaracao'
#     p[0] = Tree('sequencia_decl', [p[1]])

# def p_sequencia_decl_2(p):
#     'sequencia_decl : sequencia_decl declaracao'
#     p[0] = Tree('sequencia_decl_loop', [p[1], p[2]])

    def sequencia_decl(self, node):
        if(node.type == "sequencia_decl_loop") :
            self.sequencia_decl(node.child[0])
            self. declaracao(node.child[1])
        else :
            self. declaracao(node.child[0])

# def p_declaracao_1(p):
#     'declaracao : se_decl'
#     p[0] = Tree('declaracao_se', [p[1]])

# def p_declaracao_2(p):
#     'declaracao : repita_decl'
#     p[0] = Tree('declaracao_repita', [p[1]])

# def p_declaracao_3(p):
#     'declaracao : atribuicao_decl'
#     p[0] = Tree('declaracao_atribuicao', [p[1]])

# def p_declaracao_4(p):
#     'declaracao : leia_decl'
#     p[0] = Tree('declaracao_leia', [p[1]])

# def p_declaracao_5(p):
#     'declaracao : escreva_decl'
#     p[0] = Tree('declaracao_escreva', [p[1]])

# def p_declaracao_6(p):
#     'declaracao : declara_var'
#     p[0] = Tree('declaracao_declaravar', [p[1]])

# #retorna em outra parte do codigo
# def p_declaracao_7(p):
#     'declaracao : retorna_decl'
#     p[0] = Tree('declaracao_retorna', [p[1]])

# def p_declaracao_8(p):
#     'declaracao : chama_func'
#     p[0] = Tree('declaracao_chamafunc', [p[1]])

    def declaracao(self, node) :
        if(node.type == "declaracao_se"):
            self.se_decl(node.child[0])

        elif(node.type == "declaracao_repita"):
            self.repita_decl(node.child[0])

        elif(node.type == "declaracao_atribuicao"):
            self.atribuicao_decl(node.child[0])

        elif(node.type == "declaracao_leia"):
            self.leia_decl(node.child[0])

        elif(node.type == "declaracao_escreva"):
            self.escreva_decl(node.child[0])

        elif(node.type == "declaracao_declaravar"):
            self.declara_var(node.child[0])

        elif(node.type == "declaracao_retorna"):
            self.retorna_decl(node.child[0])

        elif(node.type == "declaracao_chamafunc"):
            self.chamada_func(node.child[0])

# def p_retorna_decl_1(p):
#     'retorna_decl : RETORNA ABRE_PAR ID FECHA_PAR'
#     p[0] = Tree('retorna_id', [], [p[3]])

# def p_retorna_decl_2(p):
#     'retorna_decl : RETORNA ABRE_PAR numero_decl FECHA_PAR'
#     p[0] = Tree('retorna_numero', [p[3]])

    def retorna_decl(self, node):
        if (node.type == "retorna_numero"):

            tipo = self.numero_decl(node.child[0])

            # if self.scope != "global":
            #     if self.table[self.scope]["tipo"] == "INTEIRO" and tipo == 2:
            #         print("Warning : Função do tipo INTEIRO retorna um valor FLUTUANTE : " + self.scope)

            #     elif self.table[self.scope]["tipo"] == "FLUTUANTE" and tipo == 1:
            #         print("Warning : Função do tipo INTEIRO retorna um valor FLUTUANTE : " + self.scope)

        else:
            return node.value #retorna o id

# def p_numero_1(p):
#     'numero_decl : INTEIRO'
#     p[0] = Tree('numero_decl_inteiro', [], [p[1]])

# def p_numero_2(p):
#     'numero_decl : FLUTUANTE'
#     p[0] = Tree('numero_decl_flutuante', [], [p[1]])

    def numero_decl(self, node):
        if(node.type == "numero_decl_inteiro"):
            return 1 #inteiro
        else:
            return 2 #float

# def p_se_decl_1(p):
#     'se_decl : SE exp_decl ENTAO NOVA_LINHA sequencia_decl NOVA_LINHA FIM NOVA_LINHA'
#     p[0] = Tree('se_decl', [p[2], p[5]])

# def p_se_decl_2(p):
#     'se_decl : SE exp_decl ENTAO NOVA_LINHA sequencia_decl NOVA_LINHA SENAO NOVA_LINHA sequencia_decl NOVA_LINHA FIM NOVA_LINHA'
#     p[0] = Tree('se_decl_senao', [p[2], p[5], p[9]])

    def se_decl(self, node):
        if(len(node.child) == 2):
            self.exp_decl(node.child[0])
            self.sequencia_decl(node.child[1])

        else:
            self.exp_decl(node.child[0], "nada")
            self.sequencia_decl(node.child[1])
            self.sequencia_decl(node.child[2])

# def p_repita_decl(p):
#     'repita_decl : REPITA NOVA_LINHA sequencia_decl ATE exp_decl NOVA_LINHA'
#     p[0] = Tree('repita_decl', [p[3], p[5]])

    def repita_decl(self, node):
        self.sequencia_decl(node.child[0])
        self.exp_decl(node.child[1], "nada")

# def p_atribuicao_decl(p):
#     'atribuicao_decl : ID ATRIBUICAO exp_decl NOVA_LINHA'
#     p[0] = Tree('atribuicao_decl', [p[3]], [p[1]])

    def atribuicao_decl(self, node):
        if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)

        else :
            if self.scope + "." + node.value in self.table.keys():
                self.table[self.scope + "." + node.value]["inicializada"] = True 
                self.exp_decl(node.child[0], node.value) #passa o nome da variável

            elif "global." + node.value in self.table.keys():
                self.table["global." + node.value]["inicializada"] = True
                self.exp_decl(node.child[0], node.value) #passa o nome da variável

# def p_leia_decl(p):
#     'leia_decl : LEIA ABRE_PAR ID FECHA_PAR NOVA_LINHA'
#     p[0] = Tree('leia_decl', [], [p[3]])

    def leia_decl(self, node) :
        if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
            print("Erro Semântico. Variável " + node.value + " não encontrada")
            exit(1)

# def p_escreva_decl_1(p):
#     'escreva_decl : ESCREVA ABRE_PAR exp_decl FECHA_PAR NOVA_LINHA'
#     p[0] = Tree('escreva_decl_exp', [p[3]])

# def p_escreva_decl_2(p):
#     'escreva_decl : ESCREVA ABRE_PAR chamada_func FECHA_PAR NOVA_LINHA'
#     p[0] = Tree('escreva_decl', [p[3]])

    def escreva_decl(self, node):
        if(node.child[0].type == "escreva_decl_exp"):
            self.exp_decl(node.child[0], "nada")

        else :
            self.chamada_func_escreva(node.child[0])

# def p_chamada_func(p):
#     'chamada_func : ID ABRE_PAR parametro_chama_func FECHA_PAR NOVA_LINHA'
#     p[0] = Tree('chamada_func', [p[3]], [p[1]]
    def chamada_func(self, node) :

        if(node.value not in self.table.keys()) :
            print("Erro Semântico, nome de funcao não declarado : " + node.value )
            exit(1)

        if self.parametro_chama_func(node.child[0]) != self.table[node.value]["num_parametros"]:
            print("Erro Semântico, número de parametros não correspondem com os da função : " + node.value )
            exit(1)

# def p_chamada_func(p):
#     'chamada_func : ID ABRE_PAR parametro_chama_func FECHA_PAR'
#     p[0] = Tree('chamada_func', [p[3]], [p[1]]
    def chamada_func_escreva(self, node) :

        if(node.value not in self.table.keys()) :
            print("Erro Semântico, nome de funcao não declarado : " + node.value )
            exit(1)

        if self.parametro_chama_func(node.child[0]) != self.table[node.value]["num_parametros"]:
            print("Erro Semântico, número de parametros não correspondem com os da função : " + node.value )
            exit(1)

# def p_parametro_chama_func_1(p):
#     'parametro_chama_func : ID'
#     p[0] = Tree('parametro_chama_func', [], [p[1]])

# def p_parametro_chama_func_2(p):
#     'parametro_chama_func : numero_decl'
#     p[0] = Tree('parametro_chama_func_num', [p[1]])

# def p_parametro_chama_func_3(p):
#     'parametro_chama_func : parametro_chama_func VIRGULA ID'
#     p[0] = Tree('parametro_chama_func_paramentros', [p[1]], p[2])

# def p_parametro_chama_func_4(p):
#     'parametro_chama_func : parametro_chama_func VIRGULA numero_decl'
#     p[0] = Tree('parametro_chama_func_numeros', [p[1]], p[2])

    def parametro_chama_func(self, node):

        if node.type == "parametro_chama_func_paramentros":
            if self.scope + "." + node.value not in self.table.keys() and "global" + "." + node.value not in self.table.keys():
                print("Erro semântico : Variável não declarada  " + node.value)
                exit(1)

            elif self.scope + "." + node.value in self.table.keys():
                if self.table[self.scope + "." + node.value]["inicializada"] == False:
                    print("Erro semântico : Variável não inicializada " + node.value)
                    exit(1)

                else:
                    return self.parametro_chama_func(node.child[0]) + 1

            elif "global" + "." + node.value in self.table.keys():
                if self.table["global" + "." + node.value]["inicializada"] == False:
                    print("Erro semântico : Variável não inicializada " + node.value)
                    exit(1)

                else:
                    return self.parametro_chama_func(node.child[0]) + 1

        elif node.type == "parametro_chama_func_numeros":
            self.numero_decl(node.child[0])
            self.parametro_chama_func(node.child[0]) + 1

        elif node.type == "parametro_chama_func_num":
            self.numero_decl(node.child[0])
            return 1

        elif node.type == "parametro_chama_func":
            if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
                print("Erro semântico : Variável não declarada " + node.value)
                exit(1)

            elif self.scope + "." + node.value in self.table.keys():
                if self.table[self.scope + "." + node.value]["inicializada"] == False:
                    print("Erro semântico : Variável não inicializada " + node.value)
                    exit(1)
                else:
                    return 1

            elif "global" + "." + node.value in self.table.keys():
                if self.table["global" + "." + node.value]["inicializada"] == False:
                    print("Erro semântico : Variável não inicializada " + node.value)
                    exit(1)
                else:
                    return 1

# def p_exp_decl_1(p):
#     'exp_decl : simples_exp'
#     p[0] = Tree('exp_decl', [p[1]])

# def p_exp_decl_2(p):
#     'exp_decl : simples_exp compara_op simples_exp'
#     p[0] = Tree('exp_decl_compara', [p[1], p[2], p[3]])

    def exp_decl(self, node, nomeVariavel) :
        if( node.child[0].type == "exp_decl_compara" ):
            self.simples_exp(node.child[0], nomeVariavel)
            self.compara_op(node.child[1])
            self.simples_exp(node.child[2], nomeVariavel)

        else :
            self.simples_exp(node.child[0], nomeVariavel)

# def p_compara_op_1(p):
#     'compara_op : IGUAL'
#     p[0] = Tree('compara_op_igual', [], [p[1]])

# def p_compara_op_2(p):
#     'compara_op : MENOR'
#     p[0] = Tree('compara_op_menor', [], [p[1]])

# def p_compara_op_3(p):
#     'compara_op : MAIOR'
#     p[0] = Tree('compara_op_maior', [], [p[1]])

# def p_compara_op_4(p):
#     'compara_op : MENOR_IGUAL'
#     p[0] = Tree('compara_op_menorIgual', [], [p[1]])

# def p_compara_op_5(p):
#     'compara_op : MAIOR_IGUAL'
#     p[0] = Tree('compara_op_maiorIgual', [], [p[1]])

    def compara_op(self, node):
            return node.value

# def p_simples_exp_1(p):
#     'simples_exp : termo'
#     p[0] = Tree('simples_exp', [p[1]])

# def p_simples_exp_2(p):
#     'simples_exp : simples_exp soma_sub termo'
#     p[0] = Tree('simples_exp_somasub', [p[1], p[2], p[3]])

    def simples_exp(self, node, nomeVariavel) :
        if(node.child[0].type == "simples_exp_somasub"):
            self.simples_exp(node.child[0], nomeVariavel)
            self.soma_sub(node.child[1])
            self.termo(node.child[2], nomeVariavel)

        else :
            self.termo(node.child[0], nomeVariavel)

# def p_soma_sub_1(p):
#     'soma_sub : SOMA'
#     p[0] = Tree('soma_sub_soma', [], [p[1]])

# def p_soma_sub_2(p):
#     'soma_sub : SUB'
#     p[0] = Tree('soma_sub_subtracao', [], [p[1]])

    def soma_sub(self, node):
        return node.value

# def p_termo_1(p):
#     'termo : fator'
#     p[0] = Tree('termo_fator', [p[1]])

# def p_termo_2(p):
#     'termo : termo mult_div fator'
#     p[0] = Tree('termo_multdiv', [p[1], p[2], p[3]])

    def termo(self, node, nomeVariavel) :
        if(node.child[0].type == "termo_multdiv"):
            self.termo(node.child[0], nomeVariavel)
            self.mult_div(node.child[1])
            self.fator(node.child[2], nomeVariavel)

        else :
            self.fator(node.child[0], nomeVariavel)

# def p_mult_div_1(p):
#     'mult_div : MULT'
#     p[0] = Tree('mult_div_multiplicacao', [], [p[1]])

# def p_mult_div_2(p):
#     'mult_div : DIVISAO'
#     p[0] = Tree('mult_div_divisao', [], [p[1]])

    def mult_div(self, node):
            return node.value

# def p_fator_1(p):
#     'fator : ID'
#     p[0] = Tree('fator_id', [], [p[1]])

# def p_fator_2(p):
#     'fator : numero_decl'
#     p[0] = Tree('fator_numero', [p[1]])

# def p_fator_3(p):
#     'fator : ABRE_PAR exp_decl FECHA_PAR'
#     p[0] = Tree('fator_exp', [p[2]])

    def fator(self, node, nomeVariavel):

        if node.type == "fator_numero":
            if nomeVariavel != "nada": #atribuicao
                if self.scope + "." + nomeVariavel in self.table.keys():
                    tipo = self.numero_decl(node.child[0])

                    if self.table[self.scope + "." + nomeVariavel]["tipo"] == "INTEIRO" and tipo == 2: #inteiro e float
                        print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                    elif self.table[self.scope + "." + nomeVariavel]["tipo"] == "FLUTUANTE" and tipo == 1: #float e inteiro
                        print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)

                elif "global." + nomeVariavel in self.table.keys():
                    tipo = self.numero_decl(node.child[0])

                    if self.table["global." + nomeVariavel]["tipo"] == "INTEIRO" and tipo == 2: #inteiro e float
                        print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                    elif self.table["global." + nomeVariavel]["tipo"] == "FLUTUANTE" and tipo == 1: #float e inteiro
                        print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)

            else:
                self.numero_decl(node.child[0])

        elif node.type == "fator_id":

            if nomeVariavel != "nada": #atribuicao

                if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
                    print("Erro semântico : Variável não declarada : " + node.value)
                    exit(1)

                else:
                    if self.scope + "." + node.value in self.table.keys():

                        if self.scope + "." + nomeVariavel in self.table.keys():

                            if self.table[self.scope + "." + node.value]["inicializada"] == True: #recebenco ID inicializado    
                                if self.table[self.scope + "." + nomeVariavel]["tipo"] == "INTEIRO" and self.table[self.scope + "." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                                    print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                                elif self.table[self.scope + "." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.table[self.scope + "." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                                    print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                            else:
                                print("Erro semântico : Variável não inicializada : " + node.value)
                                exit(1)

                        elif "global." + nomeVariavel in self.table.keys():
                            
                            if self.table[self.scope + "." + node.value]["inicializada"] == True: #recebenco ID inicializado                              
                            
                                if self.table["global." + nomeVariavel]["tipo"] == "INTEIRO" and self.table[self.scope + "." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                                    print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                                elif self.table["global." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.table[self.scope + "." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                                    print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                            else:
                                print("Erro semântico : Variável não inicializada : " + node.value)
                                exit(1)

                    elif "global." + node.value in self.table.keys():  

                        if self.scope + "." + nomeVariavel in self.table.keys():

                            if self.table["global." + node.value]["inicializada"] == True: #recebenco ID inicializado 
                                if self.table[self.scope + "." + nomeVariavel]["tipo"] == "INTEIRO" and self.table["global." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                                    print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                                elif self.table[self.scope + "." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.table["global." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                                    print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                            
                            else:
                                print("Erro semântico : Variável não inicializada : " + node.value)
                                exit(1)

                        elif "global." + nomeVariavel in self.table.keys():
                            
                            if self.table["global." + node.value]["inicializada"] == True: #recebenco ID inicializado 
                                
                                if self.table["global." + nomeVariavel]["tipo"] == "INTEIRO" and self.table["global." + node.value]["tipo"] == "FLUTUANTE": #inteiro e float
                                    print("Warning : Voce está associando um tipo FLUTUANTE a um tipo INTEIRO : " + nomeVariavel)

                                elif self.table["global." + nomeVariavel]["tipo"] == "FLUTUANTE" and self.table["global." + node.value]["tipo"] == "INTEIRO": #float e inteiro
                                    print("Warning : Voce está associando um tipo INTEIRO a um tipo FLUTUANTE : " + nomeVariavel)
                            
                            else:
                                print("Erro semântico : Variável não inicializada : " + node.value)
                                exit(1)

            else:
                if self.scope + "." + node.value not in self.table.keys() and "global." + node.value not in self.table.keys():
                    print("Erro semântico : Variável não declarada : " + node.value)
                    exit(1)
                    
                    return node.value
        else :            
            self.exp_decl(node.child[0], "nada")


# def p_tipo_1(p):
#     'tipo : VAZIO'
#     p[0] = Tree('tipo_vazio', [], [p[1]])

# def p_tipo_2(p):
#     'tipo : INTEIRO'
#     p[0] = Tree('tipo_inteiro', [], [p[1]])

# def p_tipo_3(p):
#     'tipo : FLUTUANTE'
#     p[0] = Tree('tipo_flutuante', [], [p[1]])

    def tipo(self, node) :
        if(node.type == "tipo_inteiro"):
            return 1

        elif(node.type == "tipo_flutuante"):
            return 2

        elif(node.type == "tipo_vazio"):
            return 3

# def p_declara_var(p):
#     'declara_var : tipo DOIS_PONTOS ID NOVA_LINHA'
#     p[0] = Tree('declara_var', [p[1]], [p[3]])

    def declara_var(self, node) :
        if(self.scope + "." + node.value in self.table.keys()): #se ja tem variavel com esse nome na tabela
            print("Erro Semântico, nome já utilizado : " + node.value )
            exit(1)

        if self.tipo(node.child[0]) == 1:
            tipo = "INTEIRO"

        elif self.tipo(node.child[0]) == 2:
            tipo = "FLUTUANTE"

        elif self.tipo(node.child[0]) == 3:
            print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
            exit(1)

        self.table[self.scope + "." + node.value] = {}
        self.table[self.scope + "." + node.value]["var"] = True
        self.table[self.scope + "." + node.value]["inicializada"] = False
        self.table[self.scope + "." + node.value]["tipo"] = tipo
        self.table[self.scope + "." + node.value]["valor"] = None


# def p_parametro_decl_1(p):
#     'parametro_decl : parametro_decl  VIRGULA tipo DOIS_PONTOS ID'
#     p[0] = Tree('parametro_decl_loop', [p[1], p[3]], [p[5]])

# def p_parametro_decl_2(p):
#     'parametro_decl : tipo DOIS_PONTOS ID'
#     p[0] = Tree('parametro_decl', [p[1]], [p[3]])

    def parametro_decl(self, node) :

        if(node.type == "parametro_decl_loop"):
            if( self.scope + "." + node.value in self.table.keys()): #se ja tem variavel com esse nome na tabela
                print("Erro Semântico, nome já utilizado :" + node.value )
                exit(1)

            tipo = ""

            if self.tipo(node.child[0]) == 1:
                tipo = "INTEIRO"

            elif self.tipo(node.child[0]) == 2:
                tipo = "FLUTUANTE"

            elif self.tipo(node.child[0]) == 3:
                print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
                exit(1)

            self.table[self.scope + "." + node.value] = {}
            self.table[self.scope + "." + node.value]["var"] = True
            self.table[self.scope + "." + node.value]["inicializada"] = True
            self.table[self.scope + "." + node.value]["tipo"] = tipo
            self.table[self.scope + "." + node.value]["valor"] = None

            return self.parametro_decl(node.child[0]) + 1

        else: #se for só um parametro

            if( (self.scope + "." + node.value) in self.table.keys()): #se ja tem variavel com esse nome na tabela
                print("Erro Semântico, nome já utilizado : " + node.value )
                exit(1)

            elif self.tipo(node.child[0]) == 1:
                tipo = "INTEIRO"

            elif self.tipo(node.child[0]) == 2:
                tipo = "FLUTUANTE"

            elif self.tipo(node.child[0]) == 3:
                print("Erro Semântico, o parametro não pode ser do tipo VAZIO: " + node.value )
                exit(1)

            self.table[self.scope + "." + node.value] = {}
            self.table[self.scope + "." + node.value]["var"] = True
            self.table[self.scope + "." + node.value]["inicializada"] = True
            self.table[self.scope + "." + node.value]["tipo"] = tipo
            self.table[self.scope + "." + node.value]["valor"] = None

            return 1

if __name__ == '__main__':
    import sys
    code = open(sys.argv[1])
    s = Semantica(code.read())
    s.raiz()
    print("Tabela de Simbolos:", s.table)