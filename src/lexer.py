# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import collections
from .token import *


class Lexer(object):
	"""词法解析器"""
	regex_pat = "\\s*((//.*)|([0-9]+)|(\"(\\\\\"|\\\\\\\\|\\\\n|[^\"])*\")|[A-Za-z][A-Za-z0-9]*|==|<=|>=|&&|\\|\\||\\p{Punct})?"

	def __init__(self, reader):
		super(Lexer, self).__init__()
		self._reader = reader
		self._has_more = True
		self._queue = collections.deque()

	def read(self):
		if len(self._queue) > 0:
			return self._queue.popleft()
		else:
			return Token.EOF

	def peek(self, index):
		if len(self._queue) > 0:
			return self._queue[index]
		else:
			return Token.EOF

	def fill_queue(self, count):
		while count >= len(self._queue):
			if self._has_more:
				self.read_line()
			else:
				return False
		return True

	def read_line(self):
		line = self._reader.next()
		if line is None:
			self._has_more = False
			return

        int lineNo = self._reader.getLineNumber();

        Matcher matcher = pattern.matcher(line);
        matcher.useTransparentBounds(true).useAnchoringBounds(false);
        int pos = 0;
        int endPos = line.length();
        while (pos < endPos) {
            matcher.region(pos, endPos);
            if (matcher.lookingAt()) {
                addToken(lineNo, matcher);
                pos = matcher.end();
            }
            else
            throw new ParseException("bad token at line " + lineNo);
        }
        queue.add(new IdToken(lineNo, Token.EOL));
    }




package stone;

import java.io.IOException;
import java.io.LineNumberReader;
import java.io.Reader;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Lexer {
    private boolean fillQueue(int i) throws ParseException {
        while (i >= queue.size())
            if (hasMore)
                readLine();
            else
                return false;
        return true;
    }
    
    protected void addToken(int lineNo, Matcher matcher) {
        String m = matcher.group(1);
        if (m != null) // if not a space
            if (matcher.group(2) == null) { // if not a comment
                Token token;
                if (matcher.group(3) != null)
                    token = new NumToken(lineNo, Integer.parseInt(m));
                else if (matcher.group(4) != null)
                    token = new StrToken(lineNo, toStringLiteral(m));
                else
                    token = new IdToken(lineNo, m);
                queue.add(token);
            }
    }
    protected String toStringLiteral(String s) {
        StringBuilder sb = new StringBuilder();
        int len = s.length() - 1;
        for (int i = 1; i < len; i++) {
            char c = s.charAt(i);
            if (c == '\\' && i + 1 < len) {
                int c2 = s.charAt(i + 1);
                if (c2 == '"' || c2 == '\\')
                    c = s.charAt(++i);
                else if (c2 == 'n') {
                    ++i;
                    c = '\n';
                }
            }
            sb.append(c);
        }
        return sb.toString();
    }

    protected static class NumToken extends Token {
        private int value;

        protected NumToken(int line, int v) {
            super(line);
            value = v;
        }
        public boolean isNumber() { return true; }
        public String getText() { return Integer.toString(value); }
        public int getNumber() { return value; }
    }

    protected static class IdToken extends Token {
        private String text;
        protected IdToken(int line, String id) {
            super(line);
            text = id;
        }
        public boolean isIdentifier() { return true; }
        public String getText() { return text; }
    }

    protected static class StrToken extends Token {
        private String literal;
        StrToken(int line, String str) {
            super(line);
            literal = str;
        }
        public boolean isString() { return true; }
        public String getText() { return literal; }
    }
}


public class ParseException extends Exception {
    public ParseException(Token t) {
        this("", t);
    }
    public ParseException(String msg, Token t) {
        super("syntax error around " + location(t) + ". " + msg);
    }
    private static String location(Token t) {
        if (t == Token.EOF)
            return "the last line";
        else
            return "\"" + t.getText() + "\" at line " + t.getLineNumber();
    }
    public ParseException(IOException e) {
        super(e);
    }
    public ParseException(String msg) {
        super(msg);
    }
}