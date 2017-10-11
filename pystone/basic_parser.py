# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from .parser import Parser, Operators
from .astree import *
from .token import *
from .lexer import Lexer

# 语法规则
# primary    : "(" expr ")" | NUMBER | NAME | STRING
# factor     : "-" primary | primary
# expr       : factor { OP factor }
# block      : "{" [ statement ] {(";" | EOL) [ statement ]} "}"
# simple     : expr
# statement  : "if" expr block [ "else" block ]
#            | "while" expr block
#            | simple
# program    : [ statement ] (";" | EOL)


class BasicParser(object):
	def __init__(self):
		super(BasicParser, self).__init__()
		self.reserved_arr = [";", "}", Token.EOL]

		operators = Operators()
		operators.add("=", 1, Operators.RIGHT)
		operators.add("==", 2, Operators.LEFT)
		operators.add(">", 2, Operators.LEFT)
		operators.add("<", 2, Operators.LEFT)
		operators.add("+", 3, Operators.LEFT)
		operators.add("-", 3, Operators.LEFT)
		operators.add("*", 4, Operators.LEFT)
		operators.add("/", 4, Operators.LEFT)
		operators.add("%", 4, Operators.LEFT)

		rule = Parser.rule

		expr0 = rule()
		self.primary = rule(PrimaryExpr).or_(
				rule().sep('(').ast(expr0).sep(')'),
				rule().number(NumberLiteral),
				rule().identifier(Name, self.reserved_arr),
				rule().string(StringLiteral)
				)
		factor = rule().or_(
				rule(NegativeExpr).sep('-').ast(self.primary), 
				self.primary)
		expr = expr0.expression(BinaryExpr, factor, operators)
		statement0 = rule()
		block = rule(BlockStmnt).sep('{').option(statement0).repeat(
						rule().sep(';', Token.EOL).option(statement0)
						).sep('}')
		simple = rule(PrimaryExpr).ast(expr)
		statement = statement0.or_(
				rule(IfStmnt).sep('if').ast(expr).ast(block).option(rule().sep('else').ast(block)),
				rule(WhileStmnt).sep('while').ast(expr).ast(block),
				simple
				)
		self.program = rule().or_(statement, rule(NullStmnt)).sep(';', Token.EOL)


	def parse(self, lexer):
		return self.program.parse(lexer)

	@classmethod
	def parse_lexer(cls, lexer):
		basic_parser = cls()
		tree_arr = []
		while lexer.peek(0) != Token.EOF:
			tree = basic_parser.parse(lexer)
			tree_arr.append(tree)
		return tree_arr

	@classmethod
	def parse_code(cls, code):
		code_arr = code.split('\n')
		lexer = Lexer(code_arr)
		return cls.parse_lexer(lexer)












