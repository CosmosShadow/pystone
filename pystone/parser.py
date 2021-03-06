# coding: utf-8
# 语法解析
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import copy
from .exception import *
from .astree import ASTree, ASTLeaf, ASTList, NegativeExpr, Arguments, ParameterList, Dot, ArrayRef


class Element(object):
	def parse(self, lexer, astree_list):
		raise NotImplementedError('')

	def match(self, lexer):
		raise NotImplementedError('')


class Tree(Element):
	def __init__(self, parser):
		super(Tree, self).__init__()
		self._parser = parser

	def parse(self, lexer, astree_list):
		astree_list.append(self._parser.parse(lexer))

	def match(self, lexer):
		return self._parser.match(lexer)


class OrTree(Element):
	def __init__(self, parsers):
		super(OrTree, self).__init__()
		self._parsers = parsers

	def parse(self, lexer, astree_list):
		p = self._choose(lexer)
		if p is None:
			raise ParseException(lexer.peek(0))
		else:
			astree_list.append(p.parse(lexer))

	def match(self, lexer):
		return self._choose(lexer) is not None

	def _choose(self, lexer):
		for parser in self._parsers:
			if parser.match(lexer):
				return parser
		return None

	def insert(self, parser):
		self._parsers = [parser] + self._parsers


class Repeat(Element):
	def __init__(self, parser, only_once):
		self._parser = parser
		self._only_once = only_once

	def parse(self, lexer, astree_list):
		while self._parser.match(lexer):
			astree = self._parser.parse(lexer)
			if astree is not None:
				astree_list.append(astree)
			if self._only_once:
				break

	def match(self, lexer):
		return self._parser.match(lexer)


class AToken(Element):
	def __init__(self, astree_class=None):
		self._astree_class = astree_class or ASTLeaf

	def parse(self, lexer, astree_list):
		token = lexer.read()
		if self.test(token):
			leaf = self._astree_class(token)
			astree_list.append(leaf)
		else:
			raise ParseException(token)

	def match(self, lexer):
		return self.test(lexer.peek(0))

	def test(self, token):
		raise NotImplementedError('')


class IdToken(AToken):
	def __init__(self, astree_class=None, reserved_arr=None):
		super(IdToken, self).__init__(astree_class)
		self._reserved_arr = reserved_arr or []		#保留字数组

	def test(self, token):
		if token.is_identifier and token.text not in self._reserved_arr:
			return True
		else:
			return False


class NumToken(AToken):
	def test(self, token):
		return token.is_number


class StrToken(AToken):
	def test(self, token):
		return token.is_string


class Leaf(Element):
	def __init__(self, token_text_arr):
		self._token_text_arr = token_text_arr

	def parse(self, lexer, astree_list):
		token = lexer.read()
		if token.is_identifier:
			for toke_text in self._token_text_arr:
				if token.text == toke_text:
					self.add_token(astree_list, token)
					return
		if len(self._token_text_arr) > 0:
			raise ParseException(token, 'one of [' + ' '.join(self._token_text_arr) + "] expected.")
		else:
			raise ParseException(token)

	def add_token(self, astree_list, token):
		astree_list.append(ASTLeaf(token))

	def match(self, lexer):
		token = lexer.peek(0)
		if token.is_identifier and token.text in self._token_text_arr:
			return True
		else:
			return False


class Skip(Leaf):
	def add_token(self, astree_list, token):
		pass


class Operator(object):
	"""操作符
	value: 优先级
	left_assoc: 同优先级时，是否左优先
	"""
	def __init__(self, value, left_assoc):
		self.value = value
		self.left_assoc = left_assoc


class Operators(object):
	LEFT = True
	RIGHT = False
	def __init__(self):
		self._operaters = {}

	def add(self, name, value, left_assoc):
		"""
		name: 关键字
		value: 优先级
		left_assoc: 同优先级时，左优先
		"""
		self._operaters[name] = Operator(value, left_assoc)

	def __getitem__(self, key):
		return self._operaters.get(key, None)


class Expr(Element):
	"""递归二元表达式"""
	def __init__(self, astree_class, parser, operators):
		super(Expr, self).__init__()
		self._astree_class = astree_class
		self._parser = parser
		self._operaters = operators

	def parse(self, lexer, astree_list):
		astree_left = self._parser.parse(lexer)
		operator_next = self.next_operator(lexer)	#Precedence
		while operator_next is not None:
			astree_left = self.do_shift(lexer, astree_left, operator_next.value)
			operator_next = self.next_operator(lexer)
		astree_list.append(astree_left)

	def do_shift(self, lexer, astree_left, operator_value):
		arr = [astree_left, ASTLeaf(lexer.read())]
		astree_right = self._parser.parse(lexer)
		operator_next = self.next_operator(lexer)	#Precedence
		while operator_next is not None and self.right_is_expr(operator_value, operator_next):
			astree_right = self.do_shift(lexer, astree_right, operator_next.value)
			operator_next = self.next_operator(lexer)
		arr.append(astree_right)
		return self._astree_class(arr)

	def next_operator(self, lexer):
		token = lexer.peek(0)
		return self._operaters[token.text] if token.is_identifier else None

	def right_is_expr(self, operator_value, operator_next):
		if operator_next.left_assoc:
			return operator_value < operator_next.value
		else:
			return operator_value <= operator_next.value

	def match(self, lexer):
		return self._parser.match(lexer)


class Parser(object):
	def __init__(self, astree_class):
		self._elements = []
		self._astree_class = astree_class or ASTList

	def parse(self, lexer):
		astree_list = []
		for element in self._elements:
			element.parse(lexer, astree_list)
		# 以下几种树结构不能化解
		if self._astree_class in [NegativeExpr, Arguments, ParameterList, Dot, ArrayRef]:
			return self._astree_class(astree_list)
		else:
			if len(astree_list) == 0:
				return None
			elif len(astree_list) == 1:
				return astree_list[0]
			else:
				return self._astree_class(astree_list)

	def match(self, lexer):
		if len(self._elements) == 0:
			return True
		else:
			return self._elements[0].match(lexer)		#是否应该所有elements都match？

	@staticmethod
	def rule(astree_class=None):
		return Parser(astree_class)

	def reset(self):
		self._elements = []
		return self

	def number(self, astree_class=None):
		self._elements.append(NumToken(astree_class))
		return self

	def identifier(self, reserved_arr=None, astree_class=None):
		self._elements.append(IdToken(astree_class, reserved_arr))
		return self

	def string(self, astree_class=None):
		self._elements.append(StrToken(astree_class))
		return self

	def token(self, *token_text_arr):
		self._elements.append(Leaf(list(token_text_arr)))
		return self

	def sep(self, *token_text_arr):
		self._elements.append(Skip(list(token_text_arr)))
		return self

	def ast(self, parser):
		self._elements.append(Tree(parser))
		return self

	def or_(self, *parser_arr):
		self._elements.append(OrTree(list(parser_arr)))
		return self

	def maybe(self, parser):
		new_parser = copy.deepcopy(parser)
		new_parser.reset()
		self._elements.append(OrTree([parser, new_parser]))
		return self

	def option(self, parser):
		self._elements.append(Repeat(parser, only_once=True))
		return self

	def repeat(self, parser):
		self._elements.append(Repeat(parser, only_once=False))
		return self

	def expression(self, astree_class, subexp_parser, operators):
		self._elements.append(Expr(astree_class, subexp_parser, operators))
		return self

	def insert_choice(self, parser):
		element = self._elements[0]
		if isinstance(element, OrTree):
			element.insert(parser)
		else:
			other_parser = copy.deepcopy(self)
			self.reset()
			self.or_(parser, other_parser)
		return self



















