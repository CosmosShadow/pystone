# coding: utf-8
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import lake.decorator.register_fun as register

from .astree import *

TRUE = 1
FALSE = 0


@register(ASTree)
def eval(self, env):
	raise NotImplementedError('')


@register(ASTList)
def eval(self, env):
	return EvalException("cannot eval: " + str(self))


@register(ASTLeaf)
def eval(self, env):
	return EvalException("cannot eval: " + str(self))


@register(NumberLiteral)
def eval(self, env):
	return self.value()


@register(StringLiteral)
def eval(self, env):
	return self.value()


@register(Name)
def eval(self, env):
	return env[self.name()]


@register(NegativeExpr)
def eval(self, env):
	value = self.operand().eval(env)
	if isinstance(value, int):
		return value
	else:
		raise EvalException(
	Object v = ((ASTreeEx)operand()).eval(env);
            if (v instanceof Integer)
                return new Integer(-((Integer)v).intValue());
            else
                throw new StoneException("bad type for -", this);



    @Reviser public static class NegativeEx extends NegativeExpr {
        public NegativeEx(List<ASTree> c) { super(c); }
        public Object eval(Environment env) {
            Object v = ((ASTreeEx)operand()).eval(env);
            if (v instanceof Integer)
                return new Integer(-((Integer)v).intValue());
            else
                throw new StoneException("bad type for -", this);
        }
    }
    @Reviser public static class BinaryEx extends BinaryExpr {
        public BinaryEx(List<ASTree> c) { super(c); }
        public Object eval(Environment env) {
            String op = operator();
            if ("=".equals(op)) {
                Object right = ((ASTreeEx)right()).eval(env);
                return computeAssign(env, right);
            }
            else {
                Object left = ((ASTreeEx)left()).eval(env);
                Object right = ((ASTreeEx)right()).eval(env);
                return computeOp(left, op, right);
            }
        }
        protected Object computeAssign(Environment env, Object rvalue) {
            ASTree l = left();
            if (l instanceof Name) {
                env.put(((Name)l).name(), rvalue);
                return rvalue;
            }
            else
                throw new StoneException("bad assignment", this);
        }
        protected Object computeOp(Object left, String op, Object right) {
            if (left instanceof Integer && right instanceof Integer) {
                return computeNumber((Integer)left, op, (Integer)right);
            }
            else
                if (op.equals("+"))
                    return String.valueOf(left) + String.valueOf(right);
                else if (op.equals("==")) {
                    if (left == null)
                        return right == null ? TRUE : FALSE;
                    else
                        return left.equals(right) ? TRUE : FALSE;
                }
                else
                    throw new StoneException("bad type", this);
        }
        protected Object computeNumber(Integer left, String op, Integer right) {
            int a = left.intValue();
            int b = right.intValue();
            if (op.equals("+"))
                return a + b;
            else if (op.equals("-"))
                return a - b;
            else if (op.equals("*"))
                return a * b;
            else if (op.equals("/"))
                return a / b;
            else if (op.equals("%"))
                return a % b;
            else if (op.equals("=="))
                return a == b ? TRUE : FALSE;
            else if (op.equals(">"))
                return a > b ? TRUE : FALSE;
            else if (op.equals("<"))
                return a < b ? TRUE : FALSE;
            else
                throw new StoneException("bad operator", this);
        }
    }
    @Reviser public static class BlockEx extends BlockStmnt {
        public BlockEx(List<ASTree> c) { super(c); }
        public Object eval(Environment env) {
            Object result = 0;
            for (ASTree t: this) {
                if (!(t instanceof NullStmnt))
                    result = ((ASTreeEx)t).eval(env);
            }
            return result;
        }
    }
    @Reviser public static class IfEx extends IfStmnt {
        public IfEx(List<ASTree> c) { super(c); }
        public Object eval(Environment env) {
            Object c = ((ASTreeEx)condition()).eval(env);
            if (c instanceof Integer && ((Integer)c).intValue() != FALSE)
                return ((ASTreeEx)thenBlock()).eval(env);
            else {
                ASTree b = elseBlock();
                if (b == null)
                    return 0;
            else
                return ((ASTreeEx)b).eval(env);
            }
        }
    }
    @Reviser public static class WhileEx extends WhileStmnt {
        public WhileEx(List<ASTree> c) { super(c); }
        public Object eval(Environment env) {
            Object result = 0;
            for (;;) {
                Object c = ((ASTreeEx)condition()).eval(env);
                if (c instanceof Integer && ((Integer)c).intValue() == FALSE)
                    return result;
                else
                    result = ((ASTreeEx)body()).eval(env);
            }
        }
    }