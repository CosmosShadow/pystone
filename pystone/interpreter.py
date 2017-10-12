# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import sys

from .lexer import Lexer
from .basic_parser import BasicParser
from .func_parser import FuncParser
from .closure_parser import ClosureParser
from .enviroment import Enviroment
from .nested_enviroment import NestedEnv



class Interpreter(object):
	"""解释执行: 词法分析、语法分析、执行"""
	def __init__(self, lexer_cls=Lexer, kind='basic'):
		super(Interpreter, self).__init__()
		assert kind in ['basic', 'func', 'closure']

		#词法器
		self._lexer_cls = lexer_cls

		#语法器
		parsers = {'basic': BasicParser, 'func': FuncParser, 'closure': ClosureParser}
		self._parser_cls = parsers[kind]

		# 上下文环境
		envs = {'basic': Enviroment, 'func': NestedEnv, 'closure': NestedEnv}
		self._env_cls = envs[kind]

		# 执行器
		evaluators = {'basic': 'pystone.basic_evaluator','func': 'pystone.func_evaluator', 'closure': 'pystone.closure_evaluator'}
		__import__(evaluators[kind])

	def run(self, code):
		code_arr = code.split('\n')
		lexer = self._lexer_cls(code_arr)
		parser = self._parser_cls()
		env = self._env_cls()
		results = []
		while not lexer.is_end:
			tree = parser.parse(lexer)
			if tree is not None:
				value = tree.eval(env)
				print(value)
				results.append(value)
		return results


def default_run(code):
	return Interpreter().run(code)








