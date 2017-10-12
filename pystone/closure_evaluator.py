# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from lake.decorator import register_fun as register
from .astree import *
from .func_evaluator import *


@register(Fun)
def eval(self, env):
	return Function(self.parameters(), self.body(), env)