# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .parser import Parser, Operators
from .astree import *
from .token import *
from .lexer import Lexer
from .basic_parser import BasicParser


# param   : IDENTIFIER
# params  : param { "," param }
# param_list : "(" [ params ] ")"
# def     : "def" IDENTIFIER paramlist block
# args    : expr { "," expr }
# postfix : "(" [ args ] ")"
# primary : ( "(" expr ")" | NUMBER | IDENTIFIER | STRING ) { postfix }
# simple  : expr [ args ]
# program : [ def | statement ] (";" | EOL)

class FuncParser(BasicParser):
	def __init__(self):
		super(FuncParser, self).__init__()

		rule = Parser.rule

		self.param = rule().identifier(self.reserved_arr)
		self.params = rule(ParameterList).ast(self.param).repeat(rule().sep(',').ast(self.param))
		self.param_arr = rule().sep('(').maybe(self.params).sep(')')
		self.def_ = rule(DefStmnt).sep('def').identifier(self.reserved_arr).ast(self.param_arr).ast(self.block)
		self.args = rule(Arguments).ast(self.expr).repeat(rule().sep(',').ast(self.expr))
		self.postfix = rule().sep('(').maybe(self.args).sep(')')

		self.reserved_arr.append(')')
		self.primary.repeat(self.postfix)
		self.simple.option(self.args)
		self.program.insert_choice(self.def_)








