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
		return '(' + ' '.join(map(str, self._children)) +  ')'

	def location(self):
		for t in self._children:
			loc = t.location()
			if loc is not None:
				return loc
		return None


class NumberLiteral(ASTLeaf):
	"""数字字面量"""
	def value(self):
		return self._token.number


class Name(ASTLeaf):
	"""变量名"""
	def name(self):
		return self._token.text


class StringLiteral(ASTLeaf):
	def value(self):
		return self.token().text


class PrimaryExpr(ASTList):
	pass


class NegativeExpr(ASTList):
	def operand(self):
		return self.child(0)

	def __str__(self):
		return '(-' + str(self.operand()) + ')'


class BinaryExpr(ASTList):
	"""二元表达式"""
	def left(self):
		return self.child(0)

	def operator(self):
		return self.child(1).token().text

	def right(self):
		return self.child(2)


class BlockStmnt(ASTList):
	pass


class IfStmnt(ASTList):
	def condition(self):
		return self.child(0)

	def then_block(self):
		return self.child(1)

	def else_block(self):
		return self.child(2) if self.child_count > 2 else None

	def __str__(self):
		else_block_str = str(self.else_block()) or 'None'
		return "(if " + str(self.condition()) + " " + str(self.then_block()) + " else " + else_block_str + ")"


class WhileStmnt(ASTList):
	def condition(self):
		return self.child(0)

	def body(self):
		return self.child(1)

	def __str__(self):
		return "(while " + str(self.condition()) + " " + str(self.body()) + ")"


class NullStmnt(ASTList):
	pass


class ParameterList(ASTList):
	def name(self, index):
		return self.child(index).token().text

	def size(self):
		return self.child_count


class DefStmnt(ASTList):
	def name(self):
		return self.child(0).token().text

	def parameters(self):
		return self.child(1)

	def body(self):
		return self.child(2)

	def __str__(self):
		return '(def ' + str(self.name()) + ' ' + str(self.parameters()) + ' ' + str(self.body()) + ')'


class Postfix(ASTList):
	pass


class Arguments(Postfix):
	def size(self):
		return self.child_count


class Fun(ASTList):
	def parameters(self):
		return self.child(0)

	def body(self):
		return self.child(1)

	def __str__(self):
		return '(fun ' + str(self.parameters()) + ' ' + str(self.body()) + ')'


class ClassBody(ASTList):
	pass


class ClassStmnt(ASTList):
	def name(self):
		return self.child(0).token().text

	def super_class(self):
		if self.child_count < 3:
			return None
		else:
			return self.child(1).token().text

	def body(self):
		return self.child(self.child_count - 1)

	def __str__(self):
		parent = self.super_class()
		parent = parent or '*'
		return "(class " + self.name() + " " + parent + " " + str(self.body()) + ")"


class Dot(Postfix):
	"""类中的点运算抽象语法树"""
	def name(self):
		return self.child(0).token().text

	def __str__(self):
		return "." + self.name()


class ArrayLiteral(ASTList):
	"""数组抽象语法树"""
	def size(self):
		return self.child_count

	def __str__(self):
		return '[' + ' '.join(map(str, self._children)) +  ']'


class ArrayRef(Postfix):
	"""数组访问抽象语法树"""
	def index(self):
		return self.child(0)

	def __str__(self):
		return '[' + str(self.index()) + ']'



















