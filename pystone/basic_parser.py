# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from . import parser
from .parser import Parser
from .astree import *


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


class BasicParser(object):
	def __init__(self, arg):
		super(BasicParser, self).__init__()
		reserved_arr = [";", "}", Token.EOL]

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
		primary = rule(PrimaryExpr).or_(
				rule().sep('(').ast(expr0).sep(')'),
				rule().number(NumberLiteral),
				rule().identifier(Name, reserved_arr),
				rule().string(StringLiteral)
				)
		factor = rule().or_(
				rule(NegativeExpr).sep('-').ast(primary), 
				primary)
		expr = expr0.expression(BinaryExpr, factor, operators)
		statement0 = rule()
		block = rule(BlockStmnt)
				.sep('{')
				.option(statement0)
				.repeat(rule().sep(';', Token.EOL).option(statement0))
				.sep('}')
		simple = rule(PrimaryExpr).ast(expr)
		statement = statement0.or_(
				rule(IfStmnt).sep('if').ast(expr).ast(block).option(rule().sep('else').ast(block)),
				rule(WhileStmnt).sep('while').ast(expr).ast(block),
				simple
				)
		self._program = rule().or_(statement, rule(NullStmnt)).sep(';', Token.EOL)

	def parse(self, lexer):
		return self._program.parse(lexer)