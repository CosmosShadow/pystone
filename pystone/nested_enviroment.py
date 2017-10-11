# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from .enviroment import Enviroment


class NestedEnv(Enviroment):
	def __init__(self, outer=None):
		super(NestedEnv, self).__init__()
		self._outer = outer

	def set_outer(self, outer):
		self._outer = outer

	def __getitem__(self, key):
		assert isinstance(key, str)
		if key in self._values:
			return self._values[key]
		else:
			if self._outer is not None:
				return self._outer[key]
			else:
				raise StoneException('value %s should assign before use' % key)

	def put_new(self, key, value):
		self._values[key] = value

	def __setitem__(self, key, value):
		assert isinstance(key, str)
		assert isinstance(value, str) or isinstance(value, int)
		obj = self._where(key)
		obj = obj or self
		obj.put_new(key, value)

	def _where(self, key):
		if key in self._values:
			return self
		elif self._outer is None:
			return None
		else:
			return self._outer._where(key)
