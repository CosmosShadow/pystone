# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .parser import Parser, Operators
from .astree import *
from .token import *
from .lexer import Lexer
from .closure_parser import ClosureParser

# 类语法解析

# member   : def | simple
# class_body : "{" [ member ] {(";" | EOL) [ member ]} "}"
# defclass : "class" IDENTIFIER [ "extends" IDENTIFIER ] classbody
# postfix : "." IDENTIFIER | "(" [ args ] ")"
# program : [ defclass | def | statement ] (";" | EOL)


class ClassParser(ClosureParser):
	def __init__(self):
		super(ClassParser, self).__init__()
		rule = Parser.rule

		self.member = rule().or_(self.def_, self.simple)
		self.classbody = rule(ClassBody).sep("{").option(self.member).repeat(rule().sep(";", Token.EOL).option(self.member)).sep("}")
		self.defclass = rule(ClassStmnt).sep("class").identifier(self.reserved_arr).option(rule().sep("extends").identifier(self.reserved_arr)).ast(self.classbody)

		self.postfix.insert_choice(rule(Dot).sep(".").identifier(self.reserved_arr))
		self.program.insert_choice(self.defclass)








