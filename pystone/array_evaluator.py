# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from lake.decorator import register_fun as register
from .astree import *
from .class_evaluator import *


@register(ArrayLiteral)
def eval(self, env):
	return [sub_tree.eval(env) for sub_tree in self]


@register(ArrayRef)
def eval(self, env, value):
	if isinstance(value, list):
		index = self.index().eval(env)
		if isinstance(index, int):
			return value[index]
	raise StoneException("bad array access " + str(self))


array_super_compute_assign = BinaryExpr.compute_assign

@register(BinaryExpr)
def compute_assign(self, env, right_value):
	left = self.left()
	if isinstance(left, PrimaryExpr):
		primary_expr = left
		if primary_expr.has_postfix(0) and isinstance(primary_expr.postfix(0), ArrayRef):
			obj = primary_expr.eval_sub_expr(env, 1)
			if isinstance(obj, list):
				arr = obj
				aref = primary_expr.postfix(0)
				index = aref.index().eval(env)
				if isinstance(index, int):
					arr[index] = right_value
					return right_value
			raise StoneException("bad array access " + str(this))
	return array_super_compute_assign(self, env, right_value)















