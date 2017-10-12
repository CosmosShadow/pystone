# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from lake.decorator import register_fun as register
from .astree import *
from .func_evaluator import *


class NativeFunction(object):
	def __init__(self, name, method):
		self._name = name
		self._method = method

	def __str__(self):
		return "<native:" + ' ' + ">"

	def num_of_parameters(self):
		return len(self._method)

	def invoke(self, args, tree):
		try:
			self._method.invoke(None, args)
		except Exception as e:
			raise StoneException("bad native function call: " + name, tree)


@register(Arguments)
def eval(self, env, func):
	if not isinstance(func, NativeFunction):
		# 把原先注册的代码抽出来，有点丑
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

	int nparams = func.num_of_parameters()
	if self.size() != nparams:
		throw new StoneException("bad number of arguments", self)
	args = [subtree.eval(env) for subtree in self]
	return func.invoke(args, self)



















