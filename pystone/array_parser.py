# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .parser import Parser
from .astree import *
from .token import *
from .lexer import Lexer
from .class_parser import ClassParser

# 数组语法解析

# elements: expr { "," expr }
# primary : ( "[" [ elements ] "]" | "(" expr ")" | NUMBER | IDENTIFIER | STRING ) { postfix }
# postfix : "(" [ args ] ")" | "[" expr "]"

class ArrayParser(ClassParser):
	def __init__(self):
		super(ArrayParser, self).__init__()
		rule = Parser.rule

		self.elements = rule(ArrayLiteral).ast(self.expr).repeat( rule().sep( ',' ).ast(self.expr) )
		self.reserved_arr.append( ']' )
		self.primary.insert_choice( rule().sep( '[' ).maybe(self.elements).sep( ']' ) )
		self.postfix.insert_choice( rule(ArrayRef).sep( '[' ).ast(self.expr).sep( ']' ) )








