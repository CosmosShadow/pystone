# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import sys
import importlib

from .lexer import Lexer

from .basic_parser import BasicParser
from .func_parser import FuncParser
from .closure_parser import ClosureParser
from .class_parser import ClassParser

from .enviroment import Enviroment
from .nested_enviroment import NestedEnv



class Interpreter(object):
	"""解释执行: 词法分析、语法分析、执行"""
	def __init__(self, lexer_cls=Lexer, kind='basic'):
		super(Interpreter, self).__init__()
		assert kind in ['basic', 'func', 'closure', 'native', 'class']
		self._kind = kind

		#词法器
		self._lexer_cls = lexer_cls

		#语法器
		parsers = {'basic': BasicParser, 'func': FuncParser, 'closure': ClosureParser, 'native': ClosureParser, 'class': ClassParser}
		self._parser_cls = parsers[kind]

		# 上下文环境
		envs = {'basic': Enviroment, 'func': NestedEnv, 'closure': NestedEnv, 'native': NestedEnv, 'class': NestedEnv}
		self._env_cls = envs[kind]

		# 执行器
		evaluators = {
		'basic': 'pystone.basic_evaluator',
		'func': 'pystone.func_evaluator',
		'closure': 'pystone.closure_evaluator',
		'native': 'pystone.native_evaluator',
		'class': 'pystone.class_evaluator'}
		self._evaluator = importlib.import_module(evaluators[kind], 'pystone')

	def run(self, code):
		code_arr = code.split('\n')
		lexer = self._lexer_cls(code_arr)
		parser = self._parser_cls()
		env = self._env_cls()
		if self._kind == 'native':
			env = self._evaluator.Natives().environment(env)
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








