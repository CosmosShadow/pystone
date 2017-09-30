# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from .lexer import Lexer
from .basic_parser import BasicParser


class Interpreter(object):
	"""解释执行: 词法分析、语法分析、执行"""
	def __init__(self, lexer_cls=Lexer, parser_cls=BasicParser, evaluator_file='.basic_evaluator'):
		super(BasicInterpreter, self).__init__()
		self._lexer_cls = lexer_cls 				#词法器
		self._parser_cls = parser_cls 			#语法器
		# 执行器绑定到语法树中
		__import__(evaluator_file)

	def run(self, code):
		code_arr = code.split('\n')
		lexer = self._lexer_cls(code_arr)
		parser = self._parser_cls()
		results = []
		while not lexer.is_end:
			tree = parser.parse(lexer)
			value = tree.eval()
			results.append(value)
			print(value)
		return results


def default_run(code):
	return Interpreter().run(code)








