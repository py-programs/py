"""
Pure Python calculator – no imports, no dependencies.
Supports integers (exact), floats, variables, and built‑in math functions.
"""

# ------------------------------------------------------------
# Math functions implemented without any imports
# ------------------------------------------------------------
def _int_pow(base, exp):
    """Exponentiation by squaring for integer exponent."""
    result = 1
    while exp > 0:
        if exp & 1:
            result *= base
        base *= base
        exp >>= 1
    return result

def _pi():
    """Return a high‑precision approximation of pi (float)."""
    # Machin‑like formula: pi/4 = 4*arctan(1/5) - arctan(1/239)
    def arctan(x, terms=20):
        s = 0.0
        sign = 1.0
        p = x
        for i in range(1, terms*2, 2):
            s += sign * p / i
            p *= x * x
            sign = -sign
        return s
    return (16 * arctan(1/5) - 4 * arctan(1/239))

def _e():
    """Return e via series: sum(1/k!) for k=0..N"""
    s = 0.0
    fact = 1
    for i in range(20):
        s += 1.0 / fact
        fact *= (i + 1)
    return s

PI = _pi()
E  = _e()

def _sqrt(x):
    """Babylonian method for square root."""
    if x < 0:
        raise ValueError("math domain error")
    if x == 0:
        return 0.0
    guess = x / 2.0
    for _ in range(20):          # 20 iterations gives full double precision
        guess = 0.5 * (guess + x / guess)
    return guess

def _exp(x):
    """Taylor series for e^x."""
    # Use range reduction: exp(x) = exp(int + frac) = e^int * exp(frac)
    integer_part = int(x)
    frac = x - integer_part
    # exp(frac) via series
    s = 1.0
    term = 1.0
    for i in range(1, 30):
        term *= frac / i
        s += term
    # e^integer_part by repeated squaring on E
    if integer_part >= 0:
        return s * (E ** integer_part)
    else:
        return s / (E ** (-integer_part))

def _ln(x):
    """Natural logarithm via Newton's method on exp(y)-x=0."""
    if x <= 0:
        raise ValueError("math domain error")
    # initial guess: use log2 and convert
    guess = 0.0
    tmp = x
    while tmp > 2.0:
        tmp /= 2.0
        guess += 0.6931471805599453   # ln(2)
    while tmp < 0.5:
        tmp *= 2.0
        guess -= 0.6931471805599453
    # Newton refinement
    for _ in range(5):
        guess = guess + (x - _exp(guess)) / _exp(guess)
    return guess

def _log10(x):
    return _ln(x) / 2.302585092994046

def _log(x, base=None):
    if base is None:
        return _ln(x)
    return _ln(x) / _ln(base)

def _sin(x):
    """Taylor series for sine (input in radians)."""
    # Normalize to [-pi, pi]
    twopi = 2 * PI
    x = x - twopi * int(x / twopi)
    # Taylor: sin(x) = x - x^3/3! + x^5/5! - ...
    s = 0.0
    term = x
    sign = 1.0
    x2 = x * x
    fact = 1
    for i in range(1, 20, 2):
        s += sign * term / fact
        term *= x2
        sign = -sign
        fact *= (i + 1) * (i + 2)
    return s

def _cos(x):
    return _sin(PI/2 - x)

def _tan(x):
    s = _sin(x)
    c = _cos(x)
    if abs(c) < 1e-15:
        raise ValueError("tan undefined")
    return s / c

def _factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("factorial only defined for non‑negative integers")
    res = 1
    for i in range(1, n+1):
        res *= i
    return res

# ------------------------------------------------------------
# Tokenizer (no regex)
# ------------------------------------------------------------
def tokenize(expr):
    i = 0
    n = len(expr)
    tokens = []
    while i < n:
        c = expr[i]
        if c in ' \t':
            i += 1
            continue
        if c.isdigit() or (c == '.' and i+1 < n and expr[i+1].isdigit()):
            # number
            start = i
            if c == '0' and i+1 < n and expr[i+1] in 'xX':
                i += 2
                while i < n and expr[i] in '0123456789abcdefABCDEF':
                    i += 1
                tokens.append(('NUMBER', int(expr[start:i], 16)))  # hex int
                continue
            while i < n and (expr[i].isdigit() or expr[i] == '.'):
                i += 1
            if i < n and expr[i] in 'eE':
                i += 1
                if i < n and expr[i] in '+-':
                    i += 1
                while i < n and expr[i].isdigit():
                    i += 1
            num_str = expr[start:i]
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                tokens.append(('FLOAT', float(num_str)))
            else:
                tokens.append(('INT', int(num_str)))
            continue
        if c.isalpha() or c == '_':
            start = i
            while i < n and (expr[i].isalnum() or expr[i] == '_'):
                i += 1
            tokens.append(('ID', expr[start:i]))
            continue
        if c in '+-*/%()=,':   # single‑char operators
            if c == '*' and i+1 < n and expr[i+1] == '*':
                tokens.append(('POW', '**'))
                i += 2
                continue
            if c == '/' and i+1 < n and expr[i+1] == '/':
                tokens.append(('FLOORDIV', '//'))
                i += 2
                continue
            tokens.append((c, c))
            i += 1
            continue
        raise SyntaxError(f"Unexpected character: {c!r}")
    tokens.append(('EOF', None))
    return tokens

# ------------------------------------------------------------
# Parser + Evaluator
# ------------------------------------------------------------
FUNCTIONS = {'sqrt', 'exp', 'ln', 'log', 'log10', 'sin', 'cos', 'tan', 'factorial'}

class Calculator:
    def __init__(self):
        self.vars = {'ans': 0.0, 'pi': PI, 'e': E}
        self.tokens = []
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def peek(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return ('EOF', None)

    def advance(self):
        self.pos += 1

    def eat(self, kind):
        if self.current()[0] == kind:
            val = self.current()[1]
            self.advance()
            return val
        raise SyntaxError(f"Expected {kind}, got {self.current()}")

    # --------------------------------------------------------
    # Grammar
    # --------------------------------------------------------
    def parse_assignment(self):
        if self.current()[0] == 'ID' and self.peek()[0] == '=':
            var = self.current()[1]
            self.advance()         # skip ID
            self.eat('=')         # skip =
            value = self.expr()
            self.vars[var] = value
            return value
        return self.expr()

    def expr(self):
        left = self.term()
        while self.current()[0] in ('+', '-'):
            op = self.current()[0]
            self.advance()
            right = self.term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        return left

    def term(self):
        left = self.power()
        while self.current()[0] in ('*', '/', 'FLOORDIV', '%'):
            op = self.current()[0]
            self.advance()
            right = self.power()
            if op == '*':
                left = left * right
            elif op == '/':
                left = left / right
            elif op == 'FLOORDIV':
                left = left // right
            elif op == '%':
                left = left % right
        return left

    def power(self):
        left = self.unary()
        if self.current()[0] == 'POW':
            self.advance()
            right = self.power()   # right‑associative
            # Use built‑in exponentiation; int**int remains exact
            return left ** right
        return left

    def unary(self):
        if self.current()[0] == '-':
            self.advance()
            return -self.unary()
        if self.current()[0] == '+':
            self.advance()
            return self.unary()
        return self.primary()

    def primary(self):
        tok = self.current()
        if tok[0] == 'INT':
            self.advance()
            return tok[1]        # exact integer
        if tok[0] == 'FLOAT':
            self.advance()
            return tok[1]        # float
        if tok[0] == 'ID':
            name = tok[1]
            self.advance()
            if name in FUNCTIONS:
                return self.call_function(name)
            if name in self.vars:
                return self.vars[name]
            raise NameError(f"name '{name}' is not defined")
        if tok[0] == '(':
            self.advance()
            val = self.expr()
            self.eat(')')
            return val
        raise SyntaxError(f"Unexpected token {tok}")

    def call_function(self, name):
        self.eat('(')
        args = []
        args.append(self.expr())
        while self.current()[0] == ',':
            self.advance()
            args.append(self.expr())
        self.eat(')')
        # Dispatch
        if name == 'sqrt':
            return _sqrt(args[0])
        if name == 'exp':
            return _exp(args[0])
        if name == 'ln':
            return _ln(args[0])
        if name == 'log10':
            return _log10(args[0])
        if name == 'log':
            if len(args) == 1:
                return _ln(args[0])
            else:
                return _log(args[0], args[1])
        if name == 'sin':
            return _sin(args[0])
        if name == 'cos':
            return _cos(args[0])
        if name == 'tan':
            return _tan(args[0])
        if name == 'factorial':
            return _factorial(args[0])
        raise RuntimeError(f"Unknown function {name}")

    def evaluate(self, expr):
        self.tokens = tokenize(expr)
        self.pos = 0
        result = self.parse_assignment()
        if self.current()[0] != 'EOF':
            raise SyntaxError("Extra tokens after expression")
        self.vars['ans'] = result
        return result

# ------------------------------------------------------------
# REPL
# ------------------------------------------------------------
def repl():
    calc = Calculator()
    print("No‑import Python calculator")
    print("Type 'help' for help, 'quit' to exit.\n")
    while True:
        try:
            line = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line in ('quit', 'exit'):
            break
        if line == 'help':
            print("""Built‑in functions (no imports):
  sqrt, exp, ln, log(x,[base]), log10
  sin, cos, tan (radians), factorial
Constants: pi, e
Operators: + - * / // % **
Assignment: x = expression
Memory: ans
Example: 2**100, sqrt(2), log(100,10), x = sin(pi/2)""")
            continue
        try:
            result = calc.evaluate(line)
            # Pretty‑print: show ints as ints, floats normally
            if isinstance(result, float) and result == int(result):
                print(int(result))
            else:
                print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    repl()
