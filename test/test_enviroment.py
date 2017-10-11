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


if __name__ == '__main__':
	pass


















