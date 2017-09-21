# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *
from pystone.lexer import *

class TestLexer(object):
	@classmethod
	def setup_class(klass):
		pass

	@classmethod
	def teardown_class(klass):
		pass

	def setup(self):
		pass

	def teardown(self):
		pass

	def test_comment(self):
		source_codes = ['hello world //comment']
		lexer = Lexer(source_codes)
		tokens = [lexer.read() for _ in range(4)]
		for i, (cls, text) in enumerate([(IdToken, 'hello'), (IdToken, 'world'), (IdToken, '\\n')]):
			assert_is_instance(tokens[i], cls)
			assert_equal(tokens[i].text, text)
		assert_is_instance(tokens[-1], Token)
		assert_equal(tokens[-1].line_number, -1)

	def test_string(self):
		source_codes = ['a == "string"']
		lexer = Lexer(source_codes)
		tokens = [lexer.read() for _ in range(5)]
		for i, (cls, text) in enumerate([(IdToken, 'a'), (IdToken, '=='), (StrToken, 'string'), (IdToken, '\\n')]):
			assert_equal(tokens[i].text, text)
			assert_is_instance(tokens[i], cls)
		assert_is_instance(tokens[-1], Token)
		assert_equal(tokens[-1].line_number, -1)

	def test_number(self):
		source_codes = ['b=12']
		lexer = Lexer(source_codes)
		tokens = [lexer.read() for _ in range(5)]

		assert_is_instance(tokens[0], IdToken)
		assert_equal(tokens[0].text, 'b')

		assert_is_instance(tokens[1], IdToken)
		assert_equal(tokens[1].text, '=')

		assert_is_instance(tokens[2], NumToken)
		assert_equal(tokens[2].text, '12')
		assert_equal(tokens[2].number, 12)

		assert_is_instance(tokens[3], IdToken)
		assert_equal(tokens[3].text, '\\n')

		assert_is_instance(tokens[4], Token)
		assert_equal(tokens[4].line_number, -1)
















