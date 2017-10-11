# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *

from pystone.exception import *
from pystone.interpreter import *


class TestInterpreter(object):
	def setup(self):
		pass

	def test_basic(self):
		code = '''sum = 0
		i = 1
		while i < 10 {
		    sum = sum + i
		    i = i + 1
		}
		sum'''
		results = default_run(code)
		assert_equal(results, [0, 1, 10, 45])

	def test_func_1(self):
		code = '''sum = 0
		i = 1
		while i < 10 {
		    sum = sum + i
		    i = i + 1
		}
		sum'''
		interperter = Interpreter(kind='func')
		results = interperter.run(code)
		assert_equal(results, [0, 1, 10, 45])


if __name__ == '__main__':
	interperter = Interpreter(kind='func')
	code = '''
	def fib (n) {
		if n < 2 {
			n
		} else {
			fib(n - 1) + fib(n - 2)
		}
	}
	a = fib(10)
	'''
	# code = """
	# def foo(a) {
	# 	b = a + 10
	# }
	# c = foo(5)
	# """
	results = interperter.run(code)
	# print(results)
