# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import re
import string
import collections
from .token import *


class Lexer(object):
	"""词法解析器"""
	punctuation = string.punctuation
	punctuation = punctuation.replace('"', '')
	punctuation = punctuation.replace('/', '')
	re_number = "[0-9]+"
	re_identifier = "[A-Za-z][A-Za-z0-9]*|==|<=|>=|&&|\\|\\||[%s]" % punctuation
	re_string = '"((\\"|\\\\|\\n|[^"])*)"'
	re_comment = "//.*"
	regex_pat = "\\s*((%s)|(%s)|(%s)|%s)?" % (re_number, re_identifier, re_comment, re_string)

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
		match, number, identifier, comment, string, sting_las_char = matcher
		if len(match) > 0 and len(comment) == 0:
			if len(number) > 0:
				token = NumToken(line_no, int(number))
			if len(identifier) > 0:
				token = IdToken(line_no, identifier)
			if len(string) > 0:
				token = StrToken(line_no, string)
			self._queue.append(token)



class ParseException(Exception):
	def __init__(self, msg, token=None):
		if token is None:
			super(ParseException, self)(msg)
		else:
			location = "the last line" if token == Token.EOF else "\"" + t.getText() + "\" at line " + str(token.line_number)
			"syntax error around " + location + ". " + msg
			super(ParseException, self)(msg)









		