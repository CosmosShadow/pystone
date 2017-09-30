# coding: utf-8
# 环境: 保存程序上下文
# 存取变量
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from .token import *


class Enviroment(object):
	def __init__(self):
		super(Enviroment, self).__init__()
		self._values = dict()

	def _check_key(self, key):
		assert key != None
		if not isinstance(key, str):
			assert isinstance(key, Token)
			if not isinstance(key, IdToken):
				raise StoneException('only variable can store a value')
			key = key.text
		assert len(key) > 0
		return key

	def _check_value(self, value):
		assert value != None
		if not any([isinstance(value, str), isinstance(value, int)]):
			if not any([isinstance(value, NumToken), isinstance(value, StrToken)]):
				raise StoneException('only number or string can be used for assign')
			if isinstance(value, NumToken):
				value = value.number
			if isinstance(value, StrToken):
				value = value.text
		return value

	def __getitem__(self, key):
		key = self._check_key(key)
		if key in self._values:
			return self._values[key]
		else:
			raise StoneException('value %s should assign before use' % key)

	def __setitem__(self, key, value):
		key = self._check_key(key)
		value = self._check_value(value)
		self._values[key] = value


















