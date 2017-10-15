# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import collections

# 手工分词器: 有限状态机实现

class ManualLexer(object):
	EMPTY = -1

	def __init__(self, string):
		self._last_char = self.EMPTY
		self._queue = collections.deque(list(string))

	def next_char(self):
		if len(self._queue) > 0:
			return self._queue.popleft()
		else:
			return None

	def get_char(self):
		if self._last_char == self.EMPTY:
			return self.next_char()
		else:
			c = self._last_char
			self._last_char = self.EMPTY
			return c

	def un_get_char(self, char):
		self._last_char = char

	def read(self):
		paths = []

		tmp_char = ' '
		while tmp_char is not None and self.is_space(tmp_char):
			tmp_char = self.get_char()

		char = tmp_char

		if char < 0:
			return None
		else:
			if self.is_digit(char):
				while self.is_digit(char):
					paths.append(char)
					char = self.get_char()
			elif self.is_letter(char):
				while self.is_letter(char) or self.is_digit(char):
					paths.append(char)
					char = self.get_char()
			elif char == '=':
				char = self.get_char()
				if char == '=':
					return '=='
				else:
					self.un_get_char(char)
					return '='
			else:
				raise ValueError(char)

		if char > 0:
			self.un_get_char(char)

		return ''.join(paths)


	def is_letter(self, char):
		return ('A' <= char and char <= 'Z') or ('a' <= char and char <= 'z')

	def is_digit(self, char):
		return '0' <= char and char <= '9'

	def is_space(self, char):
		return 0 <= char and char <= ' '


def tokenize(string):
	lexer = ManualLexer(string)
	token = lexer.read()
	results = []
	while token is not None:
		results.append(token)
		token = lexer.read()
	return results
