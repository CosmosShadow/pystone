# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *
from pystone.lexer import *
from pystone.basic_parser import *




class TestParser(object):
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

		code_arr = codes.split('\n')
		lexer = Lexer(code_arr)
		basic_parser = BasicParser()

		tree_arr = []
		while lexer.peek(0) != Token.EOF:
			tree = basic_parser.parse(lexer)
			tree_arr.append(tree)

		for tree, target in zip(tree_arr, syntax_tree.split('\n')):
			assert_equal(str(tree), target.strip())


if __name__ == '__main__':
	code_arr = ['2 + -1']
	lexer = Lexer(code_arr)
	basic_parser = BasicParser()
	print(basic_parser.parse(lexer))





















