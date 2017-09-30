# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import lake.decorator.register_fun as register

from .astree import *

TRUE = 1
FALSE = 0


@register(ASTree)
def eval(self, env):
	raise NotImplementedError('')


@register(ASTList)
def eval(self, env):
	return EvalException("cannot eval: " + str(self))


@register(ASTLeaf)
def eval(self, env):
	return EvalException("cannot eval: " + str(self))


@register(NumberLiteral)
def eval(self, env):
	return self.value()


@register(StringLiteral)
def eval(self, env):
	return self.value()


@register(Name)
def eval(self, env):
	return env[self.name()]


@register(NegativeExpr)
def eval(self, env):
	value = self.operand().eval(env)
	if isinstance(value, int):
		return value
	else:
		raise EvalException('bad type for -' + str(self))


@register(BinaryExpr)
def eval(self, env):
	op = self.operator()
	if op == '=':
		right_value = self.right().eval(env)
		return self.compute_assign(env, right_value)
	else:
		right_value = self.right().eval(env)
		left_value = self.left().eval(env)
		return self.compute_op(left_value, op, right_value)

@register(BinaryExpr)
def compute_assign(self, env, right_value):
	left = self.left()
	if isinstance(left, Name):
		env[left] = right_value
		return right_value
	else:
		raise EvalException('bad assignment ' + str(self))

@register(BinaryExpr)
def compute_op(self, left_value, op, right_value):
	if isinstance(left_value, int) and isinstance(right_value, int):
		return self.compute_number(left_value, op, right_value)
	else:
		if op == '+':
			return str(left_value) + str(right_value)
		elif op == '==':
			if left_value == right_value:
				return TRUE
			else:
				return FALSE
		else:
			EvalException('bad type ' + str(self))

@register(BinaryExpr)
def compute_number(self, left_value, op, right_value):
	if op == '+':
		return left_value + right_value
	elif: op == '-':
		return left_value - right_value
	elif op == '*':
		return a * b
	elif op == '/':
		return a / b
	elif op == '%':
		return a % b
	elif op == '==':
		return TRUE if a == b else FALSE
	elif op == '>':
		return TRUE if a > b else FALSE
	elif op == '<':
		return TRUE if a < b else FALSE
	else:
		EvalException('bad operator ' + str(self))


@register(BlockStmnt)
def eval(self, env):
	result = 0
	for sub_astree in self:
		if not isinstance(sub_astree, NullStmnt):
			result = sub_astree.eval(env)
	return result


@register(IfStmnt)
def eval(self, env):
	cond = self.condition().eval(env)
	if isinstance(cond, int) and cond != FALSE:
		return self.then_block().eval(env)
	else:
		else_block = self.else_block()
		if else_block is not None:
			return else_block.eval(env)
		else:
			return 0


@register(WhileStmnt)
def eval(self, env):
	result = 0
	while True:
		cond = self.condition().eval(env)
		if isinstance(cond, int) and cond == FALSE:
			return result
		else:
			result = self.body().eval(env)
	return result


















