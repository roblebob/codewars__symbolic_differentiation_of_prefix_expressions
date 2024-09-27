const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);

const parse = (expr) => {
  let index = 0;
  const tokens = expr.match(/\(|\)|[^\s()]+/g).map((token) => (isNaN(token) ? token : Number(token)));

  const _parse = () => {
    const token = tokens[index++];
    if (token !== "(") return token;
    const result = [];
    while (tokens[index] !== ")") result.push(_parse());
    index++;
    return result;
  };

  return _parse();
};

const differentiate = (expr) => {
  /* Chainrule is applied to every case implicitly */

  if (!Array.isArray(expr)) return typeof expr === "number" ? 0 : 1;

  const [op, a, b] = expr;

  // Sum rule: (f ± g)' = f' ± g'
  if (op === "+" || op === "-") return [op, differentiate(a), differentiate(b)];
  // Product rule: (f * g)' = f' * g + f * g'
  if (op === "*") return ["+", ["*", a, differentiate(b)], ["*", differentiate(a), b]];
  // Quotient rule: (f / g)' = (f' * g - f * g') / (g^2)
  if (op === "/") return ["/", ["-", ["*", differentiate(a), b], ["*", a, differentiate(b)]], ["^", b, 2]];
  // Power rule: (f ^ n)' = n * f ^ (n - 1) * f'
  if (op === "^") return ["*", ["*", b, ["^", a, ["-", b, 1]]], differentiate(a)];

  // cases for sin, cos, tan, exp, ln, .... where b === undefined
  if (op === "sin") return ["*", differentiate(a), ["cos", a]];
  if (op === "cos") return ["*", differentiate(a), ["*", -1, ["sin", a]]];
  if (op === "tan") return ["/", differentiate(a), ["^", ["cos", a], 2]];
  if (op === "exp") return ["*", differentiate(a), ["exp", a]];
  if (op === "ln") return ["/", differentiate(a), a];

  throw new Error(`Invalid operator: ${op}`);
};

const simplify = (expr) => {
  if (!Array.isArray(expr)) return expr;

  let [op, a, b] = expr;
  [a, b] = [simplify(a), simplify(b)];

  if (op === "+" || op === "-") {
    if (a === 0) return op === "-" ? simplify(["*", -1, b]) : b;
    if (b === 0) return a;
    if (typeof a === "number" && typeof b === "number") return op === "-" ? a - b : a + b;
  }

  if (op === "*") {
    if (a === 0 || b === 0) return 0;
    if (a === 1) return b;
    if (b === 1) return a;
    if (typeof a === "number" && typeof b === "number") return a * b;
    if (equal(a, b)) return ["^", a, 2];
  }

  if (op === "/") {
    if (b === 0) throw new Error("Division by zero");
    if (b === 1) return a;
    if (typeof a === "number" && typeof b === "number") return a / b;
    if (equal(a, b)) return 1;
  }

  if (op === "^") {
    if (b === 0) return 1;
    if (b === 1) return a;
    if (typeof a === "number" && typeof b === "number") return a ** b;
  }

  return b === undefined ? [op, a] : [op, a, b];
};

const stringify = (expr) => {
  if (typeof expr === "number") return expr.toString();
  if (Array.isArray(expr)) return `(${expr.map(stringify).join(" ")})`;
  return expr;
};

const diff = (expr) => stringify(simplify(differentiate(parse(expr))));

console.log(diff("(/ 2 (+ 1 x))"));
