# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *
from ..token import *

class TestSome(object):
	@classmethod
	def setup_class(klass):
		pass

	@classmethod
	def teardown_class(klass):
		pass

	def setup(self):
		self._token = Token(1)

	def teardown(self):
		pass

	def test_line_number(self):
		assert_equal(self._token.line_number, 1)

	def test_is(self):
		assert_false(self._token.is_identifier)
		assert_false(self._token.is_number)
		assert_false(self._token.is_string)

	def test_text(self):
		assert_equal(self._token.text, '')

	@raises(StoneException)
	def test_number(self):
		self._token.number