# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .parser import Parser, Operators
from .astree import *
from .token import *
from .lexer import Lexer
from .basic_parser import BasicParser



class FuncParser(BasicParser):
	def __init__(self):
		super(FuncParser, self).__init__()

		self.param = rule().identifier(self.reserved)
		self.params = rule(ParameterList).ast(self.param).repeat(rule().sep(',').ast(self.param))
		self.param_arr = rule().sep('(').maybe(params).sep(')')
		self.def_ = rule(DefStmnt).sep('def').identifier(reserved).ast(param_arr).ast(block)
		self.args = rule(Arguments).ast(expr).repeat(rule().sep(',').ast(expr))
		self.postfix = rule().sep('(').maybe(args).sep(')')

		self.reserved.add(')')
		self.primary.repeat(postfix)
		self.simple.option(args)
		self.program.insertChoice(self._def)