# coding: utf-8
# 环境: 保存程序上下文
# 存取变量
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import json

from .token import *


class Enviroment(object):
	def __init__(self):
		super(Enviroment, self).__init__()
		self._values = dict()

	def __getitem__(self, key):
		assert isinstance(key, str)
		if key in self._values:
			return self._values[key]
		else:
			raise StoneException('value %s should assign before use' % key)

	def __setitem__(self, key, value):
		assert isinstance(key, str)
		assert value != None
		assert isinstance(value, str) or isinstance(value, int)
		self._values[key] = value

	def __repr__(self):
		return json.dumps(self._values)



















