# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *

from pystone.exception import *
from pystone.enviroment import *


class TestEnviroment(object):
	def setup(self):
		self._env = Enviroment()

	def test_normal(self):
		self._env['name1'] = 1
		assert_equal(self._env['name1'], 1)

		self._env['name1'] = 2
		assert_equal(self._env['name1'], 2)

		self._env['name2'] = 'value2'
		assert_equal(self._env['name2'], 'value2')


	def test_token(self):
		line = 1
		key = 'token_name'
		str_value = 'this is a string'
		num_value = 2

		token_key = IdToken(line, 'token_name')
		token_str = StrToken(line, str_value)
		token_num = NumToken(line, num_value)

		self._env[token_key] = token_str
		assert_equal(self._env[token_key], str_value)

		self._env[token_key] = token_num
		assert_equal(self._env[token_key], num_value)


	@raises(StoneException)
	def test_not_in(self):
		self._env['not_in_key']

	@raises(AssertionError)
	def test_none_key(self):
		self._env[None]

	@raises(StoneException)
	def test_wrong_token_value(self):
		self._env['key'] = IdToken(1, 'id')

	@raises(StoneException)
	def test_wrong_token_key(self):
		token_num = NumToken(1, 1)
		self._env[token_num]


if __name__ == '__main__':
	pass


















