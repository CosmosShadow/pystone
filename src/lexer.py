# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import re
import string
import collections
from token import *


class Lexer(object):
	"""词法解析器"""
	punctuation = string.punctuation
	punctuation = punctuation.replace('"', '')
	punctuation = punctuation.replace('/', '')
	re_number = "[0-9]+"
	re_identifier = "[A-Za-z][A-Za-z0-9]*|==|<=|>=|&&|\\|\\||[%s]" % punctuation
	re_string = '\"[\\\\"|\\\\\\\\|\\\\n|[^\"]]*\"'
	re_comment = "//.*"
	regex_pat = "\\s*((%s)|(%s)|(%s)|(%s))?" % (re_number, re_string, re_identifier, re_comment)

	def __init__(self, source_codes):
		super(Lexer, self).__init__()
		self._source_codes = source_codes
		self._current_line = 0
		self._has_more = True
		self._queue = collections.deque()

	def next_line(self):
		if self._current_line < len(self._source_codes):
			self._current_line += 1
			return self._source_codes[self._current_line-1]
		else:
			return None

	def read(self):
		if self.fill_queue(0):
			return self._queue.popleft()
		else:
			return Token.EOF

	def peek(self, index):
		if self.fill_queue(index):
			return self._queue[index]
		else:
			return Token.EOF

	def fill_queue(self, index):
		while index + 1 > len(self._queue):
			if self._has_more:
				self.read_line()
			else:
				return False
		return True

	def read_line(self):
		line = self.next_line()
		if line is None:
			self._has_more = False
			return
		line_no = self._current_line
		for matcher in re.findall(self.regex_pat, line):
			self.add_token(line_no, matcher)
		self._queue.append(IdToken(line_no, Token.EOL));

	def add_token(self, line_no, matcher):
		match, number, string, identifier, comment = matcher
		if len(match) > 0 and len(comment) == 0:
			if len(number) > 0:
				token = NumToken(line_no, int(number))
			if len(identifier) > 0:
				token = IdToken(line_no, identifier)
			if len(string) > 0:
				token = StrToken(line_no, string)
			self._queue.append(token)



class NumToken(Token):
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
	def __init__(self, line_no, string):
		super(StrToken, self).__init__(line_no)
		self._string = string

	@property
	def is_string(self):
		return True

	@property
	def text(self):
		return self._string


class ParseException(Exception):
	def __init__(self, msg, token=None):
		if token is None:
			super(ParseException, self)(msg)
		else:
			location = "the last line" if token == Token.EOF else "\"" + t.getText() + "\" at line " + str(token.line_number)
			"syntax error around " + location + ". " + msg
			super(ParseException, self)(msg)


if __name__ == '__main__':
	source_codes = ['hello world //comment', 'a == "string"', 'b=12']
	lexer = Lexer(source_codes)
	token = lexer.read()
	while token != Token.EOF:
		print('==> ' + token.__class__.__name__ + ': ' + token.text)
		token = lexer.read()






		