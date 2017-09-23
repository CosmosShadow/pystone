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
	def __init__(self, msg):
		super(ParseException, self).__init__(str(msg))


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


class Parser(object):
    
    

    protected static class Leaf extends Element {
        protected String[] tokens;
        protected Leaf(String[] pat) { tokens = pat; }
        protected void parse(Lexer lexer, List<ASTree> res)
            throws ParseException
        {
            Token t = lexer.read();
            if (t.isIdentifier())
                for (String token: tokens)
                    if (token.equals(t.getText())) {
                        find(res, t);
                        return;
                    }

            if (tokens.length > 0)
                throw new ParseException(tokens[0] + " expected.", t);
            else
                throw new ParseException(t);
        }
        protected void find(List<ASTree> res, Token t) {
            res.add(new ASTLeaf(t));
        }
        protected boolean match(Lexer lexer) throws ParseException {
            Token t = lexer.peek(0);
            if (t.isIdentifier())
                for (String token: tokens)
                    if (token.equals(t.getText()))
                        return true;

            return false;
        }
    }

    protected static class Skip extends Leaf {
        protected Skip(String[] t) { super(t); }
        protected void find(List<ASTree> res, Token t) {}
    }

    public static class Precedence {
        int value;
        boolean leftAssoc; // left associative
        public Precedence(int v, boolean a) {
           value = v; leftAssoc = a;
        }
    }

    public static class Operators extends HashMap<String,Precedence> {
        public static boolean LEFT = true;
        public static boolean RIGHT = false;
        public void add(String name, int prec, boolean leftAssoc) {
            put(name, new Precedence(prec, leftAssoc));
        }
    }

    protected static class Expr extends Element {
        protected Factory factory;
        protected Operators ops;
        protected Parser factor;
        protected Expr(Class<? extends ASTree> clazz, Parser exp, Operators map)
        {
            factory = Factory.getForASTList(clazz);
            ops = map;
            factor = exp;
        }
        public void parse(Lexer lexer, List<ASTree> res) throws ParseException {
            ASTree right = factor.parse(lexer);
            Precedence prec;
            while ((prec = nextOperator(lexer)) != null)
                right = doShift(lexer, right, prec.value);

            res.add(right);
        }
        private ASTree doShift(Lexer lexer, ASTree left, int prec)
            throws ParseException
        {
            ArrayList<ASTree> list = new ArrayList<ASTree>();
            list.add(left);
            list.add(new ASTLeaf(lexer.read()));
            ASTree right = factor.parse(lexer);
            Precedence next;
            while ((next = nextOperator(lexer)) != null
                    && rightIsExpr(prec, next))
                right = doShift(lexer, right, next.value);

            list.add(right);
            return factory.make(list);
        }
        private Precedence nextOperator(Lexer lexer) throws ParseException {
            Token t = lexer.peek(0);
            if (t.isIdentifier())
                return ops.get(t.getText());
            else
                return null;
        }
        private static boolean rightIsExpr(int prec, Precedence nextPrec) {
            if (nextPrec.leftAssoc)
                return prec < nextPrec.value;
            else
                return prec <= nextPrec.value;
        }
        protected boolean match(Lexer lexer) throws ParseException {
            return factor.match(lexer);
        }
    }

    public static final String factoryName = "create";
    protected static abstract class Factory {
        protected abstract ASTree make0(Object arg) throws Exception;
        protected ASTree make(Object arg) {
            try {
                return make0(arg);
            } catch (IllegalArgumentException e1) {
                throw e1;
            } catch (Exception e2) {
                throw new RuntimeException(e2); // this compiler is broken.
            }
        }
        protected static Factory getForASTList(Class<? extends ASTree> clazz) {
            Factory f = get(clazz, List.class);
            if (f == null)
                f = new Factory() {
                    protected ASTree make0(Object arg) throws Exception {
                        List<ASTree> results = (List<ASTree>)arg;
                        if (results.size() == 1)
                            return results.get(0);
                        else
                            return new ASTList(results);
                    }
                };
            return f;
        }
        protected static Factory get(Class<? extends ASTree> clazz, Class<?> argType)
        {
            if (clazz == null)
                return null;
            try {
                final Method m = clazz.getMethod(factoryName, new Class<?>[] { argType });
                return new Factory() {
                    protected ASTree make0(Object arg) throws Exception {
                        return (ASTree)m.invoke(null, arg);
                    }
                };
            } catch (NoSuchMethodException e) {}
            try {
                final Constructor<? extends ASTree> c = clazz.getConstructor(argType);
                return new Factory() {
                    protected ASTree make0(Object arg) throws Exception {
                        return c.newInstance(arg);
                    }
                };
            } catch (NoSuchMethodException e) {
                throw new RuntimeException(e);
            }
        }
    }

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













