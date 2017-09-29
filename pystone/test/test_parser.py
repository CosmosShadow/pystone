# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *

from pystone.lexer import Lexer
from pystone.lexer import tokenize
from pystone.parser import *
from pystone.astree import *
from pystone.token import *


class TestParser(object):
	def test_parser_single_number(self):
		rule = Parser.rule
		num = rule().number(NumberLiteral)
		lexer = Lexer(['1;2;3'])
		tree = num.parse(lexer)
		assert_equal(str(tree), '1')

	def test_parse_two_number(self):
		rule = Parser.rule
		num = rule().number(NumberLiteral).number(NumberLiteral)
		lexer = Lexer(['1 2'])
		tree = num.parse(lexer)
		assert_equal(str(tree), '(1 2)')

	def test_parse_repeat_number(self):
		rule = Parser.rule
		num = rule().number(NumberLiteral)
		repeat_num = rule().repeat(num)
		lexer = Lexer(['1 2 3'])
		tree = repeat_num.parse(lexer)
		assert_equal(str(tree), '(1 2 3)')


if __name__ == '__main__':
	pass





















