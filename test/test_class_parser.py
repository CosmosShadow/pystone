# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *
from pystone.lexer import *
from pystone.class_parser import *



class TestClassParser(object):
	def _check(self, codes, syntax_tree):
		tree_arr = ClassParser.parse_code(codes)
		for tree, target in zip(tree_arr, syntax_tree.split('\n')):
			assert_equal(str(tree), target.strip())

	def test_basic_parser(self):
		codes = """even = 0
		odd = 0
		i = 1
		while i < 10 {
		   if i % 2 == 0 {       // even number?
		      even = even + i
		   } else {
		      odd = odd + i
		   }
		   i = i + 1
		}
		even + odd"""

		syntax_tree = """(even = 0)
		(odd = 0)
		(i = 1)
		(while (i < 10) ((if ((i % 2) == 0) (even = (even + i)) else (odd = (odd + i))) (i = (i + 1))))
		(even + odd)"""
		self._check(codes, syntax_tree)

	def test_func_parser(self):
		codes = """d = 10
		def foo(a) {
			b = a + 10
		}
		c = foo(5)"""

		syntax_tree = """(d = 10)
		(def foo (a) (b = (a + 10)))
		(c = (foo (5)))"""
		self._check(codes, syntax_tree)


	def test_parse_negative(self):
		trees = ClassParser.parse_code('2+-1')
		assert_equal(len(trees), 1)
		assert_equal(str(trees[0]), '(2 + (-1))')


	def test_parse_null(self):
		trees = ClassParser.parse_code('\n')
		assert_equal(trees[0], None)


	def test_parse_class(self):
		codes = """class Position {
			x = y = 0
			def move (nx, ny) {
				x = nx; y = ny
			}
		}
		p = Position.new
		p.move(3, 4)
		p.x = 10
		print p.x + p.y"""

		syntax_tree = """(class Position * ((x = (y = 0)) (def move (nx ny) ((x = nx) (y = ny)))))
		(p = (Position .new))
		(p .move (3 4))
		((p .x) = 10)
		(print (((p .x) + (p .y))))"""

		self._check(codes, syntax_tree)


if __name__ == '__main__':
	codes = """class Position {
		x = y = 0
		def move (nx, ny) {
			x = nx; y = ny
		}
	}
	p = Position.new
	p.move(3, 4)
	p.x = 10
	print p.x + p.y"""
	trees = ClassParser.parse_code(codes)
	for tree in trees:
		print(tree)




















