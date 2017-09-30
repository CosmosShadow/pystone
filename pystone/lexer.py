# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import re
import string
import collections
from .token import *


class Lexer(object):
	"""词法解析器
	使用正则来进行词法解析
	主要元素有: 数字、标识符、字符串字面量、注释
	每行有多个元素，所以需要re.findall
	"""
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

	@property
	def is_end(self):
		return self.peek(0) == Token.EOF:

	def read(self):
		"""读取下一个token，内容游标会往前走一步，直到文件末尾"""
		if self._fill_queue(0):
			return self._queue.popleft()
		else:
			return Token.EOF

	def peek(self, index):
		"""读取当前游标前index(0-base)位置的token，游标不变化，主要用于语法分析"""
		if self._fill_queue(index):
			return self._queue[index]
		else:
			return Token.EOF

	def _fill_queue(self, index):
		"""解析出来的token，填满index+1长度"""
		while index + 1 > len(self._queue):
			if self._has_more:
				self._read_line()
			else:
				return False
		return True

	def _read_line(self):
		line = self._next_line()
		if line is None:
			self._has_more = False
			return
		line_no = self._current_line
		for matcher in re.findall(self.regex_pat, line):
			self._add_token(line_no, matcher)
		self._queue.append(IdToken(line_no, Token.EOL));

	def _next_line(self):
		if self._current_line < len(self._source_codes):
			self._current_line += 1
			return self._source_codes[self._current_line-1]
		else:
			return None

	def _add_token(self, line_no, matcher):
		match, number, identifier, comment, string, sting_las_char = matcher
		if len(match) > 0 and len(comment) == 0:
			if len(number) > 0:
				token = NumToken(line_no, int(number))
			if len(identifier) > 0:
				token = IdToken(line_no, identifier)
			if len(string) > 0:
				token = StrToken(line_no, string)
			self._queue.append(token)


def tokenize(code):
	code_arr = code.split('\n')
	lexer = Lexer(code_arr)
	tokens = []
	while lexer.peek(0) != Token.EOF:
		tokens.append(lexer.read())
	tokens.append(Token.EOF)
	return tokens









		