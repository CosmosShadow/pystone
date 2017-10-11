# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *
from pystone.lexer import *
from pystone.basic_parser import *



class TestBasicParser(object):
	def test_parser(self):
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

		tree_arr = BasicParser.parse_code(codes)
		for tree, target in zip(tree_arr, syntax_tree.split('\n')):
			assert_equal(str(tree), target.strip())


	def test_parse_negative(self):
		trees = BasicParser.parse_code('2+-1')
		assert_equal(len(trees), 1)
		assert_equal(str(trees[0]), '(2 + (-1))')


	def test_parse_null(self):
		trees = BasicParser.parse_code('\n')
		assert_equal(trees[0], None)


if __name__ == '__main__':
	trees = BasicParser.parse_code('\n')
	print(trees[0])





















