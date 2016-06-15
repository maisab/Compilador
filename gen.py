from parser import *
from llvmlite import ir
from semantica import *

class Gen():
	def __init__ (self, code, optz = True, debug = True):
		s = Semantica(code.read())
		s.raiz()
		self.tree = s.tree
		self.table= s.table
		self.builder = None
		self.modulo = ir.Module("programaModulo")
		self.scope = "global"
		self.inicioGen(self.tree)
		print(self.modulo)

	def inicioGen(self, node):

		if self.tree.type == "programa_principal":
			self.principal(self.tree.child[0])

		elif self.tree.type == "programa_funcao":
			self.func_loop(self.tree.child[0])
			self.principal(self.tree.child[1])

		elif(self.tree.type == "programa_varglobal"):
			self.declara_var(self.tree.child[0])
			self.programa(self.tree.child[1])

	def programa(self, node):
		if(node.type == "programa_principal"):
			self.scope = "principal"
			self.principal(node.child[0])
			self.scope = "global"

		# if(node.type  == "programa_funcao"):
		# 	self.func_loop(node.child[0])
		# 	self.principal(node.child[1])

		if(node.type  == "programa_varglobal"):
			self.declara_var(node.child[0])
			self.programa(node.child[1])
 
	def principal(self, node):
		main = ir.Function(self.modulo, ir.FunctionType(ir.VoidType(), ()), name='main')
		bb = main.append_basic_block('entry')
		builder = ir.IRBuilder(bb)

		self.scope = "principal"
		self.sequencia_decl(node.child[0])

		self.scope = "global"

	def sequencia_decl(self, node):
		if(node.type == "sequencia_decl_loop"):
			self.sequencia_decl(node.child[0])
			self. declaracao(node.child[1])
		else:
			self. declaracao(node.child[0])

	def declaracao(self, node) :
		if(node.type == "declaracao_se"):
			self.se_decl(node.child[0])

		# elif(node.type == "declaracao_repita"):
		# 	self.repita_decl(node.child[0])

		# elif(node.type == "declaracao_atribuicao"):
		# 	self.atribuicao_decl(node.child[0])

		# elif(node.type == "declaracao_leia"):
		# 	self.leia_decl(node.child[0])

		# elif(node.type == "declaracao_escreva"):
		# 	self.escreva_decl(node.child[0])

		elif(node.type == "declaracao_declaravar"):
			self.declara_var(node.child[0])

		# elif(node.type == "declaracao_retorna"):
		# 	self.retorna_decl(node.child[0])

	def declara_var(self, node):
		# if(self.scope == "global"):
		if self.table[self.scope + "." + node.value]["tipo"] == "INTEIRO":
			ir.GlobalVariable(self.modulo, ir.IntType(32), self.scope + "." + node.value)

		elif self.table[self.scope + "." + node.value]["tipo"] == "FLUTUANTE":
			ir.GlobalVariable(self.modulo, ir.FloatType(), self.scope + "." + node.value)

	def se_decl(self, node):
		# formula a condição
		cond = self.exp_decl(node.child[0], "nada")
		# Estava dando erro
		#bool_cond = self.builder.fcmp_unordered('==', cond,
		#                              ir.Constant(ir.DoubleType(), 0), 'ifcond')
		# adiciona os blocos básicos
		then_block = self.func.append_basic_block('then')
		else_block = self.func.append_basic_block('else')
		merge_block = self.func.append_basic_block('ifcont')
		#self.builder.cbranch(bool_cond, then_block, else_block)
		self.builder.cbranch(cond, then_block, else_block)
		# emite o valor 'then'
		self.builder.position_at_end(then_block)
		# then_value = self.gen_expr(node.child[1])

		then_value = self.declara_var(node.child[0])

		self.builder.branch(merge_block)
		then_block = self.builder.basic_block

		# emite o valor 'else'

		self.builder.position_at_end(else_block)
		# else_value = self.gen_expr(node.child[2])
		else_value = self.declara_var(node.child[0])
		self.builder.branch(merge_block)
		else_block = self.builder.basic_block
		# finalizando o código e acionando os nós PHI
		self.builder.position_at_end(merge_block)
		phi = self.builder.phi(ir.DoubleType(), 'iftmp')
		phi.add_incoming(then_value, then_block)
		phi.add_incoming(else_value, else_block)
		return phi

	def atribuicao_decl(self, node):
		self.exp_decl(node.child[0], node.value) #passa o nome da variável


	def exp_decl(self, node, nomeVariavel) :
		if( node.child[0].type == "exp_decl_compara" ):
			self.simples_exp(node.child[0], nomeVariavel)
			self.compara_op(node.child[1])
			self.simples_exp(node.child[2], nomeVariavel)

		else :
			self.simples_exp(node.child[0])

	def simples_exp(self, node, nomeVariavel) :
		if(node.child[0].type == "simples_exp_somasub"):
			self.simples_exp(node.child[0], nomeVariavel)
			self.soma_sub(node.child[1])
			self.termo(node.child[2], nomeVariavel)

		else :
			self.termo(node.child[0], nomeVariavel)

	def soma_sub(self, node):
		if node.value == "SOMA":
			return self.builder.fadd(left, right, 'addtmp')

		elif node.value == "SUB":
			return self.builder.fsub(left, right, 'subtmp')

	def termo(self, node, nomeVariavel) :
		if(node.child[0].type == "termo_multdiv"):
			self.termo(node.child[0], nomeVariavel)
			self.mult_div(node.child[1])
			self.fator(node.child[2], nomeVariavel)

		else:
			self.fator(node.child[0], nomeVariavel)	

	def mult_div(self, node) :
		if node.value == "MULT":
			return self.builder.fmul(left, right, 'multmp')		
		elif node.value == "DIVISAO":
			return self.builder.fdiv(left, right, 'divtmp')

	def fator(self, node, nomeVariavel):

		if node.type == "fator_numero":


			#PAAREEEEIIII AQUIIIIIIIIIIIIIII

			if nomeVariavel != "nada":
				if self.scope + "." + nomeVariavel in self.table.keys():
					valor = builder.store(ir.Constant(ir.IntType(32), 7), a)
					self.table[self.scope + "." + nomeVariavel]["valor"] = 

		#fazer a condição para quando for atribuicao

		else:
			if node.type == "fator_numero":
				self.numero_decl(node.child[0])

			elif node.type == "fator_id":
				return builder.load(node.value) #carrega o valor

			elif node.type == "fator_exp":
				self.exp_decl(node.child[0], "nada")


	def numero_decl(self, node):
		# if node.type == "numero_decl_inteiro":
		return node.value
			# return ir.IntType(32)  #1 inteiro
		# else:
		# 	return node.value
			# return ir.FloatType() #2 float

	def compara_op(self, node):
		if node.type == "compara_op_igual":
			return self.builder.fcmp_unordered('==', left, right, 'cmptmp')

		elif node.type == "compara_op_maior":
			return self.builder.fcmp_unordered('>', left, right, 'cmptmp')

		elif node.type == "compara_op_menor":
			return self.builder.fcmp_unordered('<', left, right, 'cmptmp')

		elif node.type == "compara_op_menorIgual":
			return self.builder.fcmp_unordered('<=', left, right, 'cmptmp')

		elif node.type == "compara_op_maiorIgual":
			return self.builder.fcmp_unordered('>=', left, right, 'cmptmp')


if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	driver = Gen(code)