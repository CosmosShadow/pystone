# coding: utf-8
# 语法解析
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from .astree import ASTree, ASTLeaf, ASTList


import java.util.HashMap;
import java.util.HashSet;
import java.lang.reflect.Method;
import java.lang.reflect.Constructor;


class ParseException(Exception):
	def __init__(self, token, msg=''):
		super(ParseException, self).__init__((token, msg))


class Element(object):
	def parse(self, lexer, astree_list):
		raise NotImplementedError('')

	def match(self, lexer):
		raise NotImplementedError('')


class Tree(Element):
	def __init__(self, parser):
		super(Tree, self).__init__()
		self._parser = parser

	def parse(self, lexer, astree_list):
		astree_list.append(self._parser.parse(lexer))

	def match(self, lexer):
		return self._parser.match(lexer)


class OrTree(Element):
	def __init__(self, parsers):
		super(OrTree, self).__init__()
		self._parsers = parsers

	def parse(self, lexer, astree_list):
		p = self.choose(lexer);
		if p is None:
			raise ParseException(lexer.peek(0))
		else:
			astree_list.append(p.parse(lexer))

	def match(self, lexer):
		return self.choose(lexer) is not None

	def choose(self, lexer):
		for parser in self._parsers:
			if parser.match(lexer):
				return parser
		return None

	def insert(self, parser):
		self._parsers = [parser] + self._parsers


class Repeat(Element):
	def __init__(self, parser, only_once):
		self._parser = parser
		self._only_once = only_once

	def parse(lexer, astree_list):
		while self._parser.match(lexer):
			astree = self._parser.parse(lexer)
			if isinstance(astree, ASTList) or astree.child_count > 0:
				astree_list.append(astree)
			if self._only_once:
				break

	def match(self, lexer):
		return self._parser.match(lexer)


class AToken(Element):
	def __init__(self, astree_class=None):
		self._astree_class = astree_class or ASTLeaf

	def parse(lexer, astree_list):
		token = lexer.read()
		if self.test(token):
			leaf = self._astree_class(token)
			astree_list.append(leaf)
		else:
			raise ParseException(token)

	def match(self, lexer):
		return self.test(lexer.peek(0))

	def test(self, token):
		raise NotImplementedError('')


class IdToken(AToken):
	def __init__(self, astree_class=None, reserved_arr=None):
		super(IdToken, self).__init__(astree_class)
		self._reserved_arr = reserved_arr or []		#保留字数组

	def test(self, token):
		return token.is_identifier and t.text not in self._reserved_arr


class NumToken(AToken):
	def test(self, token):
		return token.is_number

class StrToken(AToken):
	def test(self, token):
		return token.is_string


class Leaf(Element):
	def __init__(self, tokens):
		self._tokens = tokens

	def parse(self, lexer, astree_list):
		token = lexer.read()
		if token.is_identifier:
			for _token in self._tokens:
				if token.text == _token.text:
					astree_list.append(ASTLeaf(token))
		if len(self._tokens) > 0:
			raise ParseException(token, self._tokens[0] + " expected.")
		else:
			raise ParseException(token)

	def find(self, astree_list, token):
		astree_list.append(ASTLeaf(token))

	def match(self, lexer):
		token = lexer.peek(0)
		if token.is_identifier:
			for _token in self._tokens:
				if token.text == _token.text:
					return True
		return False


class Skip(Leaf):
	def find(self, astree_list, token):
		pass


class Operator(object):
	def __init__(self, value, left_assoc):
		self.value = value
		self.left_assoc = left_assoc


class Operators(object):
	def __init__(self):
		self._operaters = {}

	def add(self, name, value, leftAssoc):
		self._operaters[name] = Operator(value, leftAssoc)

	def __getitem__(self, key):
		return self._operaters[key]


class Expr(Element):
	def __init__(self, factor, operators):
		self._factor = factor
		self._operaters = operators

	def parse(lexer, astree_list):
		astree_right = self._factor.parse(lexer)
		operator_next = self.next_operator(lexer)	#Precedence
		while operator_next is not None:
			astree_right = self.do_shift(lexer, astree_right, operator_next.value)
			operator_next = self.next_operator(lexer)
		astree_list.append(astree_right)

	def do_shift(self, lexer, astree_left, operator_value):
		astree_right = self._factor.parse(lexer)
		operator_next = self.next_operator(lexer)	#Precedence
		while operator_next is not None and self.right_is_expr(operator_value, operator_next):
			astree_right = do_shift(lexer, astree_right, operator_next.value);
			operator_next = self.next_operator(lexer)
		return [astree_left, ASTLeaf(lexer.read()), astree_right]

	def next_operator(self, lexer):
		token = lexer.peek(0)
		return self._operaters[token.text] if token.is_identifier else None

	def right_is_expr(operator_value, operator_next):
		if operator_next.left_assoc:
			return operator_value < operator_next.value
		else:
			return operator_value <= operator_next.value

	def match(self, lexer):
		return self._factor.match(lexer)



class Parser(object):
	
    protected List<Element> elements;
    protected Factory factory;
    public Parser(Class<? extends ASTree> clazz) {
        reset(clazz);
    }
    protected Parser(Parser p) {
        elements = p.elements;
        factory = p.factory;
    }
    public ASTree parse(Lexer lexer) throws ParseException {
        ArrayList<ASTree> results = new ArrayList<ASTree>();
        for (Element e: elements)
            e.parse(lexer, results);

        return factory.make(results);
    }
    protected boolean match(Lexer lexer) throws ParseException {
        if (elements.size() == 0)
            return true;
        else {
            Element e = elements.get(0);
            return e.match(lexer);
        }
    }
    public static Parser rule() { return rule(null); }
    public static Parser rule(Class<? extends ASTree> clazz) {
        return new Parser(clazz);
    }
    public Parser reset() {
        elements = new ArrayList<Element>();
        return this;
    }
    public Parser reset(Class<? extends ASTree> clazz) {
        elements = new ArrayList<Element>();
        factory = Factory.getForASTList(clazz);
        return this;
    }
    public Parser number() {
        return number(null);
    }
    public Parser number(Class<? extends ASTLeaf> clazz) {
        elements.add(new NumToken(clazz));
        return this;
    }
    public Parser identifier(HashSet<String> reserved) {
        return identifier(null, reserved);
    }
    public Parser identifier(Class<? extends ASTLeaf> clazz, HashSet<String> reserved)
    {
        elements.add(new IdToken(clazz, reserved));
        return this;
    }
    public Parser string() {
        return string(null);
    }
    public Parser string(Class<? extends ASTLeaf> clazz) {
        elements.add(new StrToken(clazz));
        return this;
    }
    public Parser token(String... pat) {
        elements.add(new Leaf(pat));
        return this;
    }
    public Parser sep(String... pat) {
        elements.add(new Skip(pat));
        return this;
    }
    public Parser ast(Parser p) {
        elements.add(new Tree(p));
        return this;
    }
    public Parser or(Parser... p) {
        elements.add(new OrTree(p));
        return this;
    }
    public Parser maybe(Parser p) {
        Parser p2 = new Parser(p);
        p2.reset();
        elements.add(new OrTree(new Parser[] { p, p2 }));
        return this;
    }
    public Parser option(Parser p) {
        elements.add(new Repeat(p, true));
        return this;
    }
    public Parser repeat(Parser p) {
        elements.add(new Repeat(p, false));
        return this;
    }
    public Parser expression(Parser subexp, Operators operators) {
        elements.add(new Expr(null, subexp, operators));
        return this;
    }
    public Parser expression(Class<? extends ASTree> clazz, Parser subexp, Operators operators) {
        elements.add(new Expr(clazz, subexp, operators));
        return this;
    }
    public Parser insertChoice(Parser p) {
        Element e = elements.get(0);
        if (e instanceof OrTree)
            ((OrTree)e).insert(p);
        else {
            Parser otherwise = new Parser(this);
            reset(null);
            or(p, otherwise);
        }
        return this;
    }
}













