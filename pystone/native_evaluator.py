# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from lake.decorator import register_fun as register
from .astree import *
from .closure_evaluator import *


class NativeFunction(object):
	def __init__(self, name, method, args_count):
		self._name = name
		self._method = method
		self._args_count = args_count

	def __str__(self):
		return "<native: " + self._name + ">"

	@property
	def args_count(self):
		return self._args_count

	def invoke(self, args, tree):
		try:
			return self._method(*args)
		except Exception as e:
			raise StoneException("bad native function call: " + self._name, tree)


arguments_old_eval = Arguments.eval
@register(Arguments)
def eval(self, env, func):
	if not isinstance(func, NativeFunction):
		return arguments_old_eval(self, env, func)
	else:
		if self.size() != func.args_count:
			raise StoneException("bad number of arguments", self)
		args = [subtree.eval(env) for subtree in self]
		return func.invoke(args, self)


class Natives(object):
	def environment(self, env):
		self.append_natives(env)
		return env

	def append_natives(self, env):
		self.append_native(env, 'print', Natives, 'print_', 1)
		self.append_native(env, 'len', Natives, 'len_', 1)
		self.append_native(env, 'int', Natives, 'int_', 1)

	def append_native(self, env, name, cls, method_name, args_count):
		try:
			method = getattr(cls, method_name)
		except Exception as e:
			raise StoneException("cannot find a native function: " + methodName)
		env.put_new(name, NativeFunction(method_name, method, args_count))

	@staticmethod
	def print_(obj):
		print(obj)
		return 0

	@staticmethod
	def len_(string):
		return len(string)

	@staticmethod
	def int_(string):
		return int(string)

















