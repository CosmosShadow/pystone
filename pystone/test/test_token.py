# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *
from pystone.token import *

class TestToken(object):
	def setup(self):
		self._token = Token(1)

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


class TestNumToken(object):
	def setup(self):
		self._token = NumToken(1, 20)

	def test_number(self):
		assert_equal(self._token.line_number, 1)
		assert_true(self._token.is_number)
		assert_false(self._token.is_identifier)
		assert_false(self._token.is_string)
		assert_equal(self._token.number, 20)
		assert_equal(self._token.text, '20')


class TestIdToken(object):
	def setup(self):
		self._token = IdToken(1, 'hello')

	def test_number(self):
		assert_equal(self._token.line_number, 1)
		assert_false(self._token.is_number)
		assert_true(self._token.is_identifier)
		assert_false(self._token.is_string)
		assert_equal(self._token.text, 'hello')

	@raises(StoneException)
	def test_number(self):
		self._token.number


class TestStrToken(object):
	def setup(self):
		self._token = StrToken(1, 'hello')

	def test_number(self):
		assert_equal(self._token.line_number, 1)
		assert_false(self._token.is_number)
		assert_false(self._token.is_identifier)
		assert_true(self._token.is_string)
		assert_equal(self._token.text, 'hello')

	@raises(StoneException)
	def test_number(self):
		self._token.number
