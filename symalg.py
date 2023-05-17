"""
basic symbolic calc lib for epxression evaluation and building derivatives
"""
from lexer import tokenize, build_expr


class Expr:
    def __init__(self, var=None, const=None, op1=None, op2=None, op=None):
        self.var = var
        self.const = const
        self.op1 = op1 # operand 1
        self.op2 = op2 #operand 2
        self.op = op # operator

    def __str__(self):
        if self.const is not None:
            return str(self.const)
        elif self.var is not None:
            return self.var
        # binary
        elif self.op1 is not None and self.op2 is not None:
            return f"{str(self.op1)} {self.op} {str(self.op2)}"
        # unary
        else:
            return f"{self.op}{str(self.op1)}"


    def __add__(self, other):
        return Expr(None, None, self, other, '+')

    def __sub__(self, other):
        return Expr(None, None, self, other, '-')

    def __mul__(self, other):
        return Expr(None, None, self, other, '*')

    def __truediv__(self, other):
        return Expr(None, None, self, other, '/')

    def __pow__(self, other):
        return Expr(None, None, self, other, '**')
    


class Var(Expr):
    def __init__(self, var):
        super().__init__(var, None)

class Const(Expr):
    def __init__(self, const):
        super().__init__(None, const)

# sampleExpr =  -Const(3) + Var('x') ** Const(2) + Var('y')
# print(sampleExpr.const)
# print(sampleExpr.var)
# print(sampleExpr.op1)
# print(sampleExpr.op2)
# print(sampleExpr.op)


def simplify(a):
    

    if a.op1 and a.op1.const and a.op2 and a.op2.const and a.op == '+':
        return Const(a.op1.const + a.op2.const)
    if a.op1 and a.op2 and a.op2.const == 0 and a.op == '+':
        return simplify(a.op1)
    if a.op1 and a.op1.const == 0 and a.op2 and a.op == '+':
        return simplify(a.op2)
    
    if a.op1 and a.op1.const and a.op2 and a.op2.const and a.op == '-':
        return Const(a.op1.const - a.op2.const)
    if a.op1 and a.op2 and a.op2.const == 0 and a.op == '-':
        return simplify(a.op1)
    if a.op1 and a.op1.const == 0 and a.op2 and a.op == '-':
        return simplify(negate(a.op2))
    
    
    if a.op1 and a.op1.const and a.op2 and a.op2.const and a.op == '*':
        return Const(a.op1.const * a.op2.const)
    if a.op1 and a.op2 and a.op2.const == 1 and a.op == '*':
        return simplify(a.op1)
    if a.op1 and a.op1.const == 1 and a.op2 and a.op == '*':
        return simplify(a.op2)
    if a.op1 and a.op2 and a.op2.const == 0 and a.op == '*':
        return Const(0)
    if a.op1 and a.op1.const == 0 and a.op2 and a.op == '*':
        return Const(0)
    
    
    
    if a.op1 and a.op1.const and a.op2 and a.op2.const and a.op == '**':
        return Const(a.op1.const ** a.op2.const)
    if a.op1 and a.op2 and a.op2.const == 1 and a.op == '**':
        return simplify(a.op1)
    if a.op1 and a.op2 and a.op2.const == 0 and a.op == '**':
        return Const(1)
    if a.op2 and a.op2.op == '**' and a.op1 and a.op2.op1 and a.op2.op1.const and a.op2.op2 and a.op2.op2.const:
        return a.op1 ** Const(a.op2.op1.const * a.op2.op2.const)
    
    
    
    if a.op == '*' and a.op2 and a.op2.const and a.op1.op1 and a.op1.op1.const and a.op1 and a.op1.op2:
        return Const(a.op2.const * a.op1.op1.const) * simplify(a.op1.op2)
    if a.op == '*' and a.op2 and a.op2.const and a.op1.op2 and a.op1.op2.const and a.op1.op1:
        return Const(a.op2.const * a.op1.op2.const) * simplify(a.op1.op1)
    if a.op == '*' and a.op1 and a.op1.const and a.op2.op1 and a.op2.op1.const and a.op2.op2:
        return Const(a.op1.const * a.op2.op1.const) * simplify(a.op2.op2)
    # dist law
    if a.op1 and a.op1.const and a.op2 and a.op2.op1 and a.op2.op2 and a.op2.op == '+' and a.op == '*':
        return (Const(a.op1.const) * simplify(a.op2.op1)) + (Const(a.op1.const) * simplify(a.op2.op2))
    
    
    
    if a.op1 and a.op1.const == 0 and a.op2 and a.op == '/':
        return Const(0)
    if a.op1 and a.op1.const and a.op2 and a.op2.const == 0 and a.op == '/':
        raise ZeroDivisionError
    if a.op1 and a.op1.const and a.op2 and a.op2.const and a.op1.const == a.op2.const and a.op == '/':
        return Const(1)
    if a.op1 and a.op2 and a.op2.const == 1 and a.op == '/':
        return simplify(a.op1)
    
    
    if a.op1 and a.op2 and a.op == '/':
        return simplify(a.op1) / simplify(a.op2)
    if a.op1 and a.op2 and a.op == '**':
        return simplify(a.op1) ** simplify(a.op2)
    if a.op1 and a.op2 and a.op == '*':
        return simplify(a.op1) * simplify(a.op2)
    if a.op1 and a.op2 and a.op == '+':
        return simplify(a.op1) + simplify(a.op2)
    if a.op1 and a.op2 and a.op == '-':
        return simplify(a.op1) - simplify(a.op2)
    
    else:
        return a
    
def negate(a):
    if isinstance(a, Var):
        return Const(-1) * a
    if isinstance(a, Const):
        return Const(-a.const)
    
    if a.op1 is not None and a.op2 is not None and a.op == '+':
        return negate(a.op1) + negate(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '*':
        return negate(a.op1) * a.op2
    if a.op1 is not None and a.op2 is not None and a.op == '/':
        return negate(a.op1) / a.op2
    if a.op1 is not None and a.op2 is not None and a.op == '**':
        return Const(-1) * a.op1 ** a.op2
    

def mapVar(f, a):
    # f is a function, a is an expr
    
    if isinstance(a, Var):
        return f(a)
    if isinstance(a, Const):
        return a
    if a.op1 is not None and a.op2 is not None and a.op == '+':
        return mapVar(f, a.op1) + mapVar(f, a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '-':
        return mapVar(f, a.op1) - mapVar(f, a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '*':
        return mapVar(f, a.op1) * mapVar(f, a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '/':
        return mapVar(f, a.op1) / mapVar(f, a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '**':
        return mapVar(f, a.op1) ** mapVar(f, a.op2)
    
def plugIn(c, val, a):
    # replace Var('c') with Const(val) in Expr a
    def f(x):
        if isinstance(x, Var) and x.var == c:
            return Const(val)
        return Var(x)
            
    return mapVar(f, a)


def evalExprC(a):
    # evalExpr'
    # evaluate Expr a, return Const
    if isinstance(a, Var):
        raise ValueError('still Vars in formula. Plug in a value')
    if isinstance(a, Const):
        return a.const
    if a.op1 is not None and a.op2 is not None and a.op == '+':
        return evalExprC(a.op1) + evalExprC(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '-':
        return evalExprC(a.op1) - evalExprC(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '*':
        return evalExprC(a.op1) * evalExprC(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '/':
        return evalExprC(a.op1) / evalExprC(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '**':
        return evalExprC(a.op1) ** evalExprC(a.op2)
    

def evalExpr(c, val, a):
    # plug in val for c in a
    a_c = plugIn(c, val, a)
    return evalExprC(a_c)


def derivative(a):
    # derivative of Expr a
    if isinstance(a, Var):
        return Const(1)
    if isinstance(a, Const):
        return Const(0)
    if a.op1 is not None and a.op2 is not None and a.op == '*':
        return (a.op1 * derivative(a.op2)) + (a.op2 * derivative(a.op1))
    if a.op1 is not None and a.op2.const is not None and a.op == '**':
        return Const(a.op2.const) * (a.op1 ** (Const(a.op2.const-1))) * derivative(a.op1)
    if a.op1 is not None and a.op2 is not None and a.op == '+':
        return derivative(a.op1) + derivative(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '-':
        return derivative(a.op1) - derivative(a.op2)
    if a.op1 is not None and a.op2 is not None and a.op == '/':
        return ((derivative(a.op1) * a.op2) + (negate(derivative(a.op2) * a.op1))) / (a.op2 ** Const(2))
    else:
        raise NotImplementedError('cant diff that expr not implemented')
    
def ddx(a):
    return fullSimplify(derivative(a))

def ddxs(a, n):
    l = [a]
    for _ in range(n):
        l.append(ddx(l[-1]))
            
    return l

def nthDerivative(a, n):
    """
    def nthDerivative(n, expr):
    return reduce(lambda f, g: lambda x: g(f(x)), [ddx] * n)(expr)
    """
    
    
    return ddxs(a,n)[-1]
        

def equal(a, b):
    # return True if a and b are equivalent    
    if isinstance(a, Const) and isinstance(b, Const):
        return a.const == b.const
    elif isinstance(a, Var) and isinstance(b, Var):
        return a.var == b.var
    elif a.op == b.op:
        return equal(a.op1,b.op1) and equal(a.op2,b.op2)
    else:
        return False

    
    
def print_expr(a):
    print('-----')
    print(a.const, a.var)
    print(a.op1, type(a.op1))
    print(a.op)
    print(a.op2, type(a.op2)) 
    print('-----')      

    

def fullSimplify(expr):
    last = Const(0)
    
    while not equal(expr,last):
        last = expr
        expr = simplify(expr)
    return expr



def run(fn, expr):
    
    tokens, keyword, eva = tokenize(expr)
    expr_str = build_expr(tokens)
    kw = {}
    exec(expr_str) in kw
    
    # derive
    if keyword == 'der':
        return ddx(kw['e']), None
    elif keyword == 'eval':
        c = eva[0]
        val = eva[1]
        return evalExpr(c, val, kw['e']), None
    elif keyword == 'simp':
        return fullSimplify(kw['e']), None
    else:
        raise AttributeError
    

        
if __name__ == "__main__":
    a = Const(3) * Var('x') ** Const(2)
    print(evalExpr('x', 3, a))
    
    
    # add later: multivariate evaluation
    #http://5outh.blogspot.com/2013/05/symbolic-calculus-in-haskell.html
    
    # d = Const(4) * (Var('x') + Var('y'))
    # e = Var('x') * Const(3) * Const(5)
    # sampleExpr =  Const(3) * (Var('x') + Const(7)) ** Const(4) / Const(1) * Var('y')
    
    
    
    # a = Const(3) * Var('x') + Const(1)
    # b = Const(3) * Var('x') + Const(1)
    # print(equal(a,b))
    
    
    
    # a = Const(2)
    # print_expr(a)
    # print_expr(negate(a))
    
    # a = Const(3) * Var('x') ** Const(2)
    # print(a)
    # ap = fullSimplify(derivative(a))
    # print(ap)
    # print_expr(ap)
    
    
    # # b = Const(3) * (Const(2) * Var('x') ** Const(1))
    # # print_expr(b)
    # # print_expr(b.op2)
    # # print(fullSimplify(b))
    
    # print_expr(Var('x')**Const(1))
    
    
    # a = Var('x') ** Const(1)
    # print(a)
    # print_expr(a)
    # print(simplify(a))
    # print(fullSimplify(a))
    
    
    # a = Const(2) * (Const(3) * Var('x'))
    # print_expr(a)
    # print(a)
    # print(simplify(a))
    
    
    # 3 * x ** 2
    # a = Const(3) * Var('x') ** Const(2)
    
    # ders = ddxs(a, 2)
    
    # for d in ders:
    #     print(d)
    
    
    
    
    # print(sampleExpr)
    # print_expr(sampleExpr)
    # b = simplify(sampleExpr)
    # print(b)
    # print_expr(b)