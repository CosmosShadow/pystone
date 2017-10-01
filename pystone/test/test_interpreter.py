# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from nose.tools import *

from pystone.exception import *
from pystone.interpreter import *


class TestInterpreter(object):
	def setup(self):
		pass


if __name__ == '__main__':
	code = '''sum = 0
	i = 1
	while i < 10 {
	    sum = sum + i
	    i = i + 1
	}
	sum'''

	default_run(code)
