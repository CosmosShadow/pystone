# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *

from pystone.manual_lexer import *


class TestManualLexer(object):
	def test_number(self):
		assert_equal(tokenize(' 123 456 '), ['123', '456'])

	def test_literal(self):
		assert_equal(tokenize('abc4abc abc'), ['abc4abc', 'abc'])

	def test_assign_equal(self):
		assert_equal(tokenize('====='), ['==', '==', '='])

	def test_mixed(self):
		codes = "123 abc4abc abc====="
		assert_equal(tokenize('123 abc4abc abc====='), ['123', 'abc4abc', 'abc', '==', '==', '='])


if __name__ == '__main__':
	codes = "123 abc4abc abc====="
	print(tokenize(codes))


















