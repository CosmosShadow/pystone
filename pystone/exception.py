# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division


class StoneException(Exception):
	pass


class ParseException(StoneException):
	def __init__(self, token, msg=''):
		super(ParseException, self).__init__('语法树解析错误: ' + str(token) + ', ' + msg)


class EvalException(StoneException):
	def __init__(self, msg):
		super(EvalException, self).__init__('执行错误: ' + msg)