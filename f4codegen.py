__author__ = 'hyst329'

_main = ""

c_types = {
    'INT': 'int',
    'REAL': 'double',
    'CHAR': 'char',
    'STRING': 'char*',
    'STR': 'char*'
}

def generate_c(res, file):
    global _main
    print("Generating C file...")
    file.write("#include <stdio.h>\n")
    _main = "int main() {\n"
    for stat in res:
        traverse(stat, file)
    _main += "}\n"
    file.write(_main)

def traverse(stat, file, in_main=True):
    global _main
    print(stat)
    cmd = stat[0]
    if cmd == 'NEW':
        _write(c_types[stat[1]] + ' ', file, in_main)
        _write(stat[2] + " = ", file, in_main)
        _write(_expr(stat[3]), file, in_main)
        _write(';', file, in_main)
    elif cmd == 'NEWARR':
        _write(c_types[stat[1]] + ' ', file, in_main)
        _write(stat[3] + "[", file, in_main)
        _write(_expr(stat[2]), file, in_main)
        _write('];', file, in_main)
    elif cmd == "MOV":
        var = stat[1][0]
        if stat[1][0] == 'ELEM':
            var = stat[1][1] + "[" + _expr(stat[1][2]) + "]"
        _write(var + " = ", file, in_main)
        _write(_expr(stat[2]), file, in_main)
        _write(';', file, in_main)
    elif cmd == "OUT":
        _write('printf("%s", ' + _expr(stat[1]) + ");", file, in_main)
    elif cmd == "IN":
        _write('scanf("%s", &' + _expr(stat[1]) + ");", file, in_main)
    _write('\n', file, in_main)

def _write(str, file, to_main=True):
    global _main
    if to_main:
        _main += str
    else:
        file.write(str)

def _expr(expr):
    op = expr[0]
    if op == 'ADD':
        return "(" + _expr(expr[1]) + " + " + _expr(expr[2]) + ")"
    elif op == 'SUB':
        return "(" + _expr(expr[1]) + " - " + _expr(expr[2]) + ")"
    elif op == 'MUL':
        return "(" + _expr(expr[1]) + " * " + _expr(expr[2]) + ")"
    elif op == 'DIV':
        return "(" +_expr(expr[1]) + " / " + _expr(expr[2]) + ")"
    elif op == 'EQL':
        return "(" +_expr(expr[1]) + " == " + _expr(expr[2]) + ")"
    elif op == 'LEQ':
        return "(" +_expr(expr[1]) + " <= " + _expr(expr[2]) + ")"
    elif op == 'GEQ':
        return "(" +_expr(expr[1]) + " >= " + _expr(expr[2]) + ")"
    elif op == 'LES':
        return "(" +_expr(expr[1]) + " < " + _expr(expr[2]) + ")"
    elif op == 'GTR':
        return "(" +_expr(expr[1]) + " > " + _expr(expr[2]) + ")"
    elif op == 'IND' or op == 'ELEM':
        return expr[1] + "[" + _expr(expr[2]) + "- 1]"
    elif op == 'NEG':
        return "-" + _expr(expr[1])
    elif op in ('INT', 'REAL', 'CHAR', 'STR'):
        return "(" + c_types[op] + ")(" + _literal(op, expr[1]) + ")"
    elif op == 'ID':
        return expr[1]
    elif op == 'CALL':
        return expr[1] + "(" + _expr(expr[2]) + ")"


def _literal(type, lit):
    r = str(lit)
    if type == "CHAR":
        r = "'" + r + "'"
    elif type in ("STR", "STRING"):
        r = '"' + r + '"'
    return r