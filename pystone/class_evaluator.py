# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from lake.decorator import register_fun as register
from .astree import *
from .native_evaluator import *


class ClassInfo(object):
	def __init__(self, class_stmnt, env):
		self._class_stmnt = class_stmnt
		self._env = env
		super_class_name = self._class_stmnt.super_class()
		if super_class_name is None:
			self._super_class = None
		else:
			self._super_class = self._env[super_class_name]
		if self._super_class is not None and not isinstance(ClassInfo):
			raise StoneException("unknown super class: " + self._super_class, self._class_stmnt)

	def name(self):
		return self._class_stmnt.name()

	def super_class(self):
		return self._super_class

	def body(self):
		return self._class_stmnt.body()

	def enviroment(self):
		return self._env

	def __str__(self):
		return '<class ' + self.name() + '>'


class StoneObject(object):
	def __init__(self, env):
		self._env = env

	def __str__(self):
		return '<object:' + '' + '>'

	def read(self, member):
		env = self.get_env(member)
		return env[member]

	def write(self, member, value):
		env = self.get_env(member)
		env[member] = value

	def get_env(self, member):
		env = self._env.where(member)
		if env is not None and env == self._env:
			return env
		else:
			raise AccessException()


@register(ClassStmnt)
def eval(self, env):
	class_info = ClassInfo(self, env)
	name = self.name()
	env[name] = class_info
	return name


@register(ClassBody)
def eval(self, env):
	for sub_tree in self:
		sub_tree.eval(env)
	return None


@register(Dot)
def eval(self, env, value):
	member = self.name()
	if isinstance(value, ClassInfo):
		if member == 'new':
			class_info = value
			local_env = class_info.enviroment()
			new_env = local_env.__class__(local_env)
			stone_object = StoneObject(new_env)
			new_env.put_new("this", stone_object)
			self.init_object(class_info, new_env)
			return stone_object
	if isinstance(value, StoneObject):
		stone_object = value
		return stone_object.read(member)
	raise StoneException("bad member access: " + member, this)

@register(Dot)
def init_object(self, class_info, env):
	super_class = class_info.super_class()
	if super_class is not None:
		self.init_object(super_class, env)
	class_info.body().eval(env)


binary_expr_old_compute_assign = BinaryExpr.compute_assign

@register(BinaryExpr)
def compute_assign(self, env, right_value):
	left = self.left()
	if isinstance(left, PrimaryExpr):
		primary_expr = left
		if primary_expr.has_postfix(0) and isinstance(primary_expr.postfix(0), Dot):
			obj = primary_expr.eval_sub_expr(env, 1)
			if isinstance(obj, StoneObject):
				stone_object = obj
				dot = primary_expr.postfix(0)
				return self.set_field(stone_object, dot, right_value)
	return binary_expr_old_compute_assign(self, env, right_value)

@register(BinaryExpr)
def set_field(self, stone_object, dot, right_value):
	name = dot.name()
	try:
		stone_object.write(name, right_value)
		return right_value
	except Exception as e:
		StoneException("bad member access " + self.location() + ": " + name)















