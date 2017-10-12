# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .parser import Parser, Operators
from .astree import *
from .token import *
from .lexer import Lexer
from .func_parser import FuncParser

# 闭包(函数作为参数)语法解析

# primary  ：primary | " fun " paramlist block


class ClosureParser(FuncParser):
	def __init__(self):
		super(ClosureParser, self).__init__()
		rule = Parser.rule

		self.fun = rule(Fun).sep("fun").ast(self.param_arr).ast(self.block)
		self.primary.insert_choice(self.fun)








