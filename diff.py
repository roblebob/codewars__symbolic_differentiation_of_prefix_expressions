import re

def as_float_if_possible(s):
    try:
        return float(s)
    except ValueError:
        return s


def parse(expr):
    index = 0
    tokens = re.findall(r"\(|\)|[^\s()]+", expr) 

    def parse_expr():
        nonlocal index
        nonlocal tokens
        token = tokens[index]
        index += 1
        if token == "(":
            result = []
            while tokens[index] != ")":
                result.append(parse_expr())
            index += 1
            return result
        else:
            return as_float_if_possible(token)

    return parse_expr()


def differentiate(expr):

    if not isinstance(expr, list):
        return 1 if expr == "x" else 0
    
    [op, a, b] = expr if len(expr) == 3 else [expr[0], expr[1], None]
  
    if op == "+" or op == "-":
        return [op, differentiate(a), differentiate(b)]
    
    if op == "*":
        return ["+", ["*", a, differentiate(b)], ["*", differentiate(a), b]]

    if op == "/":
        return ["/", ["-", ["*", differentiate(a), b], ["*", a, differentiate(b)]], ["*", b, b]]

    if op == "^":
        return ["*", b, ["*", ["^", a, ["-", b, 1.0]], differentiate(a)]]
    
    # cases for sin, cos, tan, exp, ln, .... where b === None
    if op == "sin":
        return ["*", differentiate(a), ["cos", a]]
    
    if op == "cos":
        return ["*", differentiate(a), ["*", -1.0, ["sin", a]]]
    
    if op == "tan":
        return ["/", differentiate(a), ["^", ["cos", a], 2.0]]
    
    if op == "exp":
        return ["*", differentiate(a), ["exp", a]]
    
    if op == "ln":
        return ["/", differentiate(a), a]

    raise ValueError(f"Unknown operator: {op}")


def simplify(expr):
    if not isinstance(expr, list):
        return expr
    
    [op, a, b] = expr if len(expr) == 3 else [expr[0], expr[1], None]

    [a, b] = [simplify(a), simplify(b)]

    if op == "+" or op == "-":
        if a == b:
            return 0 if op == "-" else simplify(["*", 2.0, a])
        if a == 0.0:
            return simplify(["*", -1.0, b]) if op == "-" else b
        if b == 0.0:
            return a
        if (isinstance(a, float) or isinstance(a, int)) and (isinstance(b, float) or isinstance(b, int)):
            return a - b if op == "-" else a + b
        
    if op == "*":
        if a == 0 or b == 0:
            return 0.0
        if a == 1.0:
            return b
        if b == 1.0:
            return a
        if isinstance(a, float) and isinstance(b, float):
            return a * b
        if a == b:
            return simplify(["^", a, 2.0])

    if op == "/":
        if b == 0.0:
            raise ValueError("Division by zero")
        if b == 1.0:
            return a
        if isinstance(a, float) and isinstance(b, float):
            return a / b
        if a == b:
            return 1.0
        
    if op == "^":
        if b == 0.0:
            return 1.0
        if b == 1.0:
            return a
        if isinstance(a, float) and isinstance(b, float):
            return a ** b

    return [op, a, b] if b is not None else [op, a]


def stringify(expr):
    if isinstance(expr, float) or isinstance(expr, int):
        return re.sub(r".0+$", "", str(expr))
    
    if isinstance(expr, list):
        return f"({' '.join(map(stringify, expr))})"
    
    return expr


def diff(expr):
    return stringify(simplify(differentiate(parse(expr)))) 





print(diff("(+ x (+ x x))")) 