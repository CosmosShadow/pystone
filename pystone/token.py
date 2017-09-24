# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


class Token(object):
	"""token(词)，区别于单词
	定义三种类型: 标识符、整型字面量、字符串字面量
	"""

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

	def __str__(self):
		return self.text


# end of file
Token.EOF = Token(-1)
# end of line
Token.EOL = '\n'

class NumToken(Token):
	"""整型字面量"""
	def __init__(self, line_no, value):
		super(NumToken, self).__init__(line_no)
		self._value = value

	@property
	def is_number(self):
		return True

	@property
	def number(self):
		return self._value

	@property
	def text(self):
		return str(self._value)


class IdToken(Token):
	"""标识符"""
	def __init__(self, line_no, text):
		super(IdToken, self).__init__(line_no)
		self._text = text

	@property
	def is_identifier(self):
		return True

	@property
	def text(self):
		return self._text

class StrToken(Token):
	"""字符串字面量"""
	def __init__(self, line_no, string):
		super(StrToken, self).__init__(line_no)
		self._string = string

	@property
	def is_string(self):
		return True

	@property
	def text(self):
		return self._string


class StoneException(Exception):
	pass





