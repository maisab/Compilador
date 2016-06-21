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
		self.func = None
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
		self.func = ir.Function(self.modulo, ir.FunctionType(ir.VoidType(), ()), name='main')
		bb = self.func.append_basic_block('entry')
		self.builder = ir.IRBuilder(bb)

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

		elif(node.type == "declaracao_atribuicao"):
			self.atribuicao_decl(node.child[0])

		# elif(node.type == "declaracao_leia"):
		# 	self.leia_decl(node.child[0])

		# elif(node.type == "declaracao_escreva"):
		# 	self.escreva_decl(node.child[0])

		elif(node.type == "declaracao_declaravar"):
			self.declara_var(node.child[0])

		# elif(node.type == "declaracao_retorna"):
		# 	self.retorna_decl(node.child[0])

	def declara_var(self, node):
		if(self.scope == "global"):
			if self.table["global." + node.value]["tipo"] == "INTEIRO":
				self.table["global." + node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.IntType(32), "global." + node.value)

			elif self.table["global." + node.value]["tipo"] == "FLUTUANTE":
				self.table["global." + node.value]["valor"] = ir.GlobalVariable(self.modulo, ir.FloatType(), "global." + node.value)
		else:
			if self.table[self.scope + "." + node.value]["tipo"] == "INTEIRO":
				self.table[self.scope + "." + node.value]["valor"] = self.builder.alloca(ir.IntType(32), self.scope + "." + node.value)

			else:
				self.table[self.scope + "." + node.value]["valor"] = self.builder.alloca(ir.FloatType(), self.scope + "." + node.value)
	
	def se_decl(self, node):
		# formula a condição
		condicao = self.exp_decl(node.child[0])

		# adiciona os blocos básicos
		then_block = self.func.append_basic_block('then')

		if(len(node.child) == 3):
			else_block = self.func.append_basic_block('else')

		merge_block = self.func.append_basic_block('ifcont')

		if(len(node.child) == 3):
			self.builder.cbranch(condicao, then_block, else_block)
		else:
			self.builder.cbranch(condicao, then_block, merge_block)
		
		# emite o valor 'then'
		self.builder.position_at_end(then_block)
		then_value = self.exp_decl(node.child[0])

		self.builder.branch(merge_block)
		then_block = self.builder.basic_block

		# emite o valor 'else'
		if(len(node.child) == 3):
			self.builder.position_at_end(else_block)
			else_value = self.exp_decl(node.child[0])
			self.builder.branch(merge_block)
			else_block = self.builder.basic_block

		# finalizando o código e acionando os nós PHI
		self.builder.position_at_end(merge_block)

		phi = self.builder.phi(ir.DoubleType(), 'iftmp')
		phi.add_incoming(then_value, then_block)

		if(len(node.child) == 3):
			phi.add_incoming(else_value, else_block)

		return phi

	def atribuicao_decl(self, node):
		
		resultado = self.exp_decl(node.child[0])

		if self.scope + "." + node.value in self.table.keys(): 
			if self.table[self.scope + "." + node.value]["tipo"] == "INTEIRO":	
				self.builder.store(ir.Constant(ir.IntType(32), self.float_to_int(resultado)), self.table[self.scope + "." + node.value]["valor"])

			elif self.table[self.scope + "." + node.value]["tipo"] == "FLUTUANTE":											
				self.builder.store(resultado, self.table[self.scope + "." + node.value]["valor"])

		else :
			if self.table["global." + node.value]["tipo"] == "INTEIRO":
				self.builder.store(ir.Constant(ir.IntType(32), self.float_to_int(resultado)), self.table["global." + node.value]["valor"])
				
			elif self.table["global." + node.value]["tipo"] == "FLUTUANTE":
				self.builder.store(resultado, self.table["global." + node.value]["valor"])

	def float_to_int(self, num):
		return self.builder.fptosi(num, ir.IntType(32))

	def int_to_float(self, num):
		return self.builder.sitofp(num, ir.FloatType())

	def exp_decl(self, node):
		if( node.type == "exp_decl_compara" ):
			left = self.simples_exp(node.child[0])
			op = self.compara_op(node.child[1])
			right = self.simples_exp(node.child[2])

			if op == '=':
				return self.builder.fcmp_unordered('==', left, right, 'cmptmp')
			elif op == '>':
				return self.builder.fcmp_unordered('>', left, right, 'cmptmp')
			elif op == '>=':
				return self.builder.fcmp_unordered('>=', left, right, 'cmptmp')
			elif op == '<':
				return self.builder.fcmp_unordered('<', left, right, 'cmptmp')
			elif op == '<=':
				return self.builder.fcmp_unordered('<=', left, right, 'cmptmp')

		else :
			return self.simples_exp(node.child[0])

	def simples_exp(self, node) :
		if(node.type == "simples_exp_somasub"):
			print("entrou soma")
			left = self.simples_exp(node.child[0])
			op = self.soma_sub(node.child[1])
			right = self.termo(node.child[2])

			if op == "+": 
				return self.builder.fadd(left, right, 'addtmp')

			elif op == "-":
				return self.builder.fsub(left, right, 'subtmp')

		else :
			return self.termo(node.child[0])

	def soma_sub(self, node):
		return node.value

	def termo(self, node):
		if(node.type == "termo_multdiv"):
			left = self.termo(node.child[0])
			op = self.mult_div(node.child[1])
			right = self.fator(node.child[2])

			if op == "*": 
				return self.builder.fmul(left, right, 'multmp')

			elif op == "/":
				return self.builder.fdiv(left, right, 'divtmp')

		else:
			return self.fator(node.child[0])	

	def mult_div(self, node) :
		return node.value

	def fator(self, node):
		if node.type == "fator_numero":
			return self.numero_decl(node.child[0])

		elif node.type == "fator_id":
			if self.scope + "." + node.value in self.table.keys():
				if self.table[self.scope + "." + node.value]["tipo"] == "INTEIRO":
					return self.int_to_float(self.builder.load(self.table[self.scope + "." + node.value]["valor"])) #carrega o valor
				else: 
					return self.builder.load(self.table[self.scope + "." + node.value]["valor"])

			else: 
				if self.table["global." + node.value]["tipo"] == "INTEIRO":
					return self.int_to_float(self.builder.load(self.table["global." + node.value]["valor"])) #carrega o valor
				else:
					return self.builder.load(self.table["global." + node.value]["valor"])


		elif node.type == "fator_exp":
			return self.exp_decl(node.child[0])


	def numero_decl(self, node):
		return ir.Constant(ir.FloatType(), node.value)

	def compara_op(self, node):
		return node.value


if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	driver = Gen(code)