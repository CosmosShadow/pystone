# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from pystone.lexer import *
from pystone.basic_parser import *

codes = """even = 0
odd = 0
i = 1
while i < 10 {
   if i % 2 == 0 {       // even number?
      even = even + i
   } else {
      odd = odd + i
   }
   i = i + 1
}
even + odd"""

code_arr = codes.split('\n')

lexer = Lexer(code_arr)
parser = BasicParser()

# token = lexer.read()
# while token != Token.EOF:
# 	print(token)
# 	token = lexer.read()
# exit()

while lexer.peek(0) != Token.EOF:
	ast = parser.parse(lexer)
	print('==> ', ast)
