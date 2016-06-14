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
			self.programa(self.tree.child[1])
			self.declara_var(self.tree.child[0])

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
		# if(node.type == "declaracao_se"):
		# 	self.se_decl(node.child[0])

		# elif(node.type == "declaracao_repita"):
		# 	self.repita_decl(node.child[0])

		# elif(node.type == "declaracao_atribuicao"):
		# 	self.atribuicao_decl(node.child[0])

		# elif(node.type == "declaracao_leia"):
		# 	self.leia_decl(node.child[0])

		# elif(node.type == "declaracao_escreva"):
		# 	self.escreva_decl(node.child[0])

		if(node.type == "declaracao_declaravar"):
			self.declara_var(node.child[0])

		# elif(node.type == "declaracao_retorna"):
		# 	self.retorna_decl(node.child[0])

	def declara_var(self, node):
		if(self.scope == "global"):
			if self.table["global." + node.value]["tipo"] == "INTEIRO":
				ir.GlobalVariable(self.modulo, ir.IntType(32), node.value)

			elif self.table["global." + node.value]["tipo"] == "FLUTUANTE":
				ir.GlobalVariable(self.modulo, ir.FloatType(), node.value)

if __name__ == '__main__':
	import sys
	code = open(sys.argv[1])
	driver = Gen(code)