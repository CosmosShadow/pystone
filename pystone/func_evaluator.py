# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from lake.decorator import register_fun as register
from .astree import *
from .basic_evaluator import *


class Function(object):
	def __init__(self, parameters, body, env):
		super(Function, self).__init__()
		self._parameters = parameters
		self._body = body
		self._env = env

	def parameters(self):
		return self._parameters

	def body(self):
		return self._body

	def make_env(self):
		return self._env.__class__(self._env)

	def __str__(self):
		return '<fun:' + '' + '>'


@register(DefStmnt)
def eval(self, env):
	func = Function(self.parameters(), self.body(), env)
	env.put_new(self.name(), func)
	return self.name()


@register(PrimaryExpr)
def operand(self):
	return self.child(0)

@register(PrimaryExpr)
def postfix(self, nest):
	return self.child(self.child_count - nest - 1)

@register(PrimaryExpr)
def has_postfix(self, nest):
	return self.child_count - nest > 1

@register(PrimaryExpr)
def eval(self, env):
	return self.eval_sub_expr(env, 0)

@register(PrimaryExpr)
def eval_sub_expr(self, env, nest):
	if self.has_postfix(nest):
		obj = self.eval_sub_expr(env, nest + 1)
		return self.postfix(nest).eval(env, obj)
	else:
		return self.operand().eval(env)


@register(Postfix)
def eval(self, env):
	raise NotImplementedError('Postfix no eval')


@register(Arguments)
def eval(self, env, func):
	if not isinstance(func, Function):
		raise StoneException('bad function', self)
	params = func.parameters()
	if self.size() != params.size():
		raise StoneException('bad number of arguments', self)
	new_env = func.make_env()
	# 实参传递到形参
	for index, sub_tree in enumerate(self):
		params.eval(new_env, index, sub_tree.eval(env))
	return func.body().eval(new_env)


@register(ParameterList)
def eval(self, env, index, value):
	env.put_new(self.name(index), value)

















