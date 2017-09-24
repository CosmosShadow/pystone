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

def flat(arr):
	result = []
	for item in arr:
		if isinstance(item, list):
			result += item
		else:
			result.append(item)
	return result

def flat_all(arr):
	while any([isinstance(item, list) for item in arr]):
		arr = flat(arr)
	return arr

def print_astree_list(astree_list):
	flatten = flat_all(astree_list)
	print('==> ' + ''.join(map(str, flatten)))

while lexer.peek(0) != Token.EOF:
	astree_list = parser.parse(lexer)
	# print_astree_list(astree_list)
	print('==>', astree_list)
