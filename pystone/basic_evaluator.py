# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from .parser import Parser, Operators
from .astree import *
from .token import *
from .lexer import Lexer
import lake.decorator.register_fun as register


@register
