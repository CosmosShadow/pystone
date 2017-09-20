# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


class Token(object):
	def __init__(self, line):
		super(Token, self).__init__()
		self._line_number = line

	@property
	def line_number(self):
		return self._line_number

	@property
	def is_identifier(self):
		return False

	@property
	def is_number(self):
		return False

	@property
	def is_string(self):
		return False

	@property
	def number(self):
		raise StoneException("not number token")

	@property
	def text(self):
		return ""


class StoneException(Exception):
	pass










