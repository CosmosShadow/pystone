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

	def test_func_run_basic(self):
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

	def test_func_run_func(self):
		code = """
		def foo(a) {
			b = a + 10
		}
		c = foo(5)
		"""
		interperter = Interpreter(kind='func')
		results = interperter.run(code)
		assert_equal(results, ['foo', 15])

	def test_func_iterator_call(self):
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
		interperter = Interpreter(kind='func')
		results = interperter.run(code)
		assert_equal(results, ['fib', 55])

	def test_func_local_variable(self):
		code = """
		a = 40
		def foo(a) {
			b = a + 10
		}
		c = foo(5)
		"""
		interperter = Interpreter(kind='func')
		results = interperter.run(code)
		assert_equal(results, [40, 'foo', 15])

	def test_func_global_variable(self):
		code = """
		a = 40
		def foo() {
			b = a + 10
		}
		c = foo()
		"""
		interperter = Interpreter(kind='func')
		results = interperter.run(code)
		assert_equal(results, [40, 'foo', 50])

	def test_func_namesapce(self):
		code = """
		a = 40
		def foo() {
			a = 50
		}
		foo()
		a
		"""
		interperter = Interpreter(kind='func')
		results = interperter.run(code)
		# foo()函数影响了外部参数
		assert_equal(results, [40, 'foo', 50, 50])

	def test_closure(self):
		code = """
		def counter (c) {
			fun () { c = c + 1 }
		}
		c1 = counter(0)
		c2 = counter(0)
		c1()
		c1()
		c2()
		"""
		interperter = Interpreter(kind='closure')
		results = interperter.run(code)

		assert_equal(results[-3:], [1, 2, 1])

	def test_native_int(self):
		code = """
		a = "12"
		b = 5 + int(a)
		"""
		interperter = Interpreter(kind='native')
		results = interperter.run(code)
		assert_equal(results, ['12', 17])

	def test_native_len(self):
		code = """
		a = "12"
		b = len(a)
		"""
		interperter = Interpreter(kind='native')
		results = interperter.run(code)
		assert_equal(results, ['12', 2])

	def test_native_len(self):
		code = """
		a = "12"
		print(a)
		"""
		interperter = Interpreter(kind='native')
		results = interperter.run(code)
		assert_equal(results, ['12', 0])




if __name__ == '__main__':
	interperter = Interpreter(kind='native')
	code = """
	a = "12"
	print(a)
	"""
	# ['12', 17]
	results = interperter.run(code)
	print(results)
















