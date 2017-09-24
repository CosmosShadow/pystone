# coding: utf-8
# Abstract Syntax Tree: 抽象语法树
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


class ASTree(object):
	"""抽象语法树，作语法树元素的基类"""
	def __init__(self):
		super(ASTree, self).__init__()
		self._children = []
	
	def child(self, index):
		return self._children[index]

	@property
	def child_count(self):
		return len(self._children)

	def children(self):
		return iter(self._children)

	def location(self):
		raise NotImplementedError('')

	def __iter__(self):
		return self.children()


class ASTLeaf(ASTree):
	"""抽象语法树列表: 就是叶子节点"""
	def __init__(self, token):
		super(ASTLeaf, self).__init__()
		self._token = token

	def __str__(self):
		return self._token.text

	def location(self):
		return 'at line ' + str(token.line_number)

	def token(self):
		return self._token



class ASTList(ASTree):
	"""抽象语法树列表: 就是中间结节"""
	def __init__(self, children):
		super(ASTList, self).__init__()
		self._children = children

	def __str__(self):
		return '(' + ' '.join([str(t) for t in self._children]) +  ')'

	def location(self):
		for t in self._children:
			if t.location():
				return t.location()
		return None


class NumberLiteral(ASTLeaf):
	"""数字字面量"""
	def value(self):
		return self._token.number


class Name(ASTLeaf):
	"""变量名"""
	def name(self):
		return self._token.text


class BinaryExpr(ASTList):
	"""二元表达式"""
	def left(self):
		return self.child(0)

	def operator(self):
		return self.child(0).token().text

	def right(self):
		return self.child(2)


class PrimaryExpr(ASTList):
	@staticmethod
	def create(self, astree_list):
		if len(astree_list) == 1:
			return astree_list[0]
		else:
			return PrimaryExpr(astree_list)


class NegativeExpr(ASTList):
	def operand(self):
		return self.child(0)

	def __str__(self):
		return '-' + self.operand()


class BlockStmnt(ASTList):
	pass


class IfStmnt(ASTList):
	def condition(self):
		return self.child(0)

	def then_block(self):
		return child(1)

	def else_block(self):
		return self.child(2) if self.child_count > 2 else None

	def __str__(self):
		else_block_str = self.else_block() or 'None'
		return "(if " + self.condition() + " " + self.then_block() + " else " + else_block_str + ")"


class WhileStmnt(ASTList):
	def condition(self):
		return self.child(0)

	def body(self):
		return self.child(1)

	def __str__(self):
		return "(while " + self.condition() + " " + body() + ")"


class NullStmnt(ASTList):
	pass


class StringLiteral(ASTLeaf):
	def value(self):
		return self.token().text









