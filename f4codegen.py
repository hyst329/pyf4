from f4type import inferType, getElementType

__author__ = 'hyst329'

_main = ""
_indent = 0

c_types = {
    'INT': 'int',
    'REAL': 'double',
    'CHAR': 'char',
    'STRING': 'char*',
    'STR': 'char*'
}

fspec = {
    'INT': 'd',
    'REAL': 'lf',
    'CHAR': 'c',
    'STRING': 's',
    'STR': 's'
}

varmap = {}
funmap = {}

BLANKOP = ("BLANK", )


def generate_c(res, file):
    global _main, _indent
    _indent = 0
    print("Generating C file...")
    file.write('#include "f4helen.h"\n')
    _main = "int main()\n{\n"
    _indent = 1
    for stat in res:
        traverse(stat, file)
    _main += "}\n"
    file.write(_main)
    file.close()
    print("Generating done")


def traverse(stat, file, cur_fun=None, with_semi=True, with_endline=True):
    global _main, _indent
    in_main = not cur_fun
    if stat == BLANKOP:
        return
    end = ";" if with_semi else ""
    if with_semi:
        _write_indent(file, in_main)
    print(stat)
    cmd = stat[0]
    if cmd == 'NEW':
        _write(c_types[stat[1]] + ' ', file, in_main)
        _write(stat[2] + " = ", file, in_main)
        _write(_expr(stat[3]), file, in_main)
        _write(end, file, in_main)
        varmap[stat[2]] = stat[1]
    elif cmd == 'NEWARR':
        # _write(c_types[stat[1]] + ' ', file, in_main)
        # _write(stat[3] + "[", file, in_main)
        # _write(_expr(stat[2]), file, in_main)
        # _write(']' + end, file, in_main)
        _write("f4_array* " + stat[3] + " = f4_new('", file, in_main)
        _write(fspec[stat[1]] + "', " + _expr(stat[2]) + ")" + end, file, in_main)
        varmap[stat[3]] = stat[1] + '.0'
    elif cmd == "MOV":
        var = stat[1][0]
        if stat[1][0] == 'ELEM':
            # var = stat[1][1] + "->array[" + _expr(stat[1][2]) + " - 1]"
            var = "((" + c_types[getElementType(varmap[stat[1][1]])] + "*)(" + \
                  stat[1][1] + "->array))[" + _expr(stat[1][2]) + " - 1]"
        _write(var + " = ", file, in_main)
        _write(_expr(stat[2]), file, in_main)
        _write(end, file, in_main)
    elif cmd == "OUT":
        _write('f4_out("%' + fspec.get(inferType(stat[1], varmap, funmap), 'a')
               + '\\n", ' + _expr(stat[1]) + ")" + end, file, in_main)
    elif cmd == "IN":
        _write("f4_in('" + fspec[inferType(stat[1], varmap, funmap)] + "', &"
               + _expr(stat[1]) + ")" + end, file, in_main)
    elif cmd == "IF":
        _write("if (", file, in_main)
        _write(_expr(stat[1]) + ")\n", file, in_main)
        _write_indent(file, in_main)
        _write("{\n", file, in_main)
        _indent += 1
        for s in stat[2]:
            traverse(s, file, cur_fun)
        if stat[3] != BLANKOP:
            _indent -= 1
            _write_indent(file, in_main)
            _write("}\n", file, in_main)
            _write_indent(file, in_main)
            _write("else\n", file, in_main)
            _write_indent(file, in_main)
            _write("{\n", file, in_main)
            _indent += 1
            for s in stat[3]:
                traverse(s, file, cur_fun)
        _indent -= 1
        _write_indent(file, in_main)
        _write("}", file, in_main)
    elif cmd == "LOOP":
        _write("for (", file, in_main)
        _old_indent = _indent
        _indent = 0
        traverse(stat[1], file, cur_fun, True, False)
        _indent = _old_indent
        _write(_expr(stat[2]) + "; ", file, in_main)
        traverse(stat[3], file, cur_fun, False, False)
        _write(")\n", file, in_main)
        _write_indent(file, in_main)
        _write("{\n", file, in_main)
        _indent += 1
        for s in stat[4]:
            traverse(s, file, cur_fun)
        _indent -= 1
        _write_indent(file, in_main)
        _write("}", file, in_main)
    elif cmd == "FUN":
        funmap[stat[1]] = stat[3]
        old_in_main = in_main
        old_cur_fun = cur_fun
        cur_fun = stat[1]
        in_main = False
        _write(c_types.get(stat[3], "void") + ' ' + stat[1], file, in_main)
        _write("(", file, in_main)
        for t in stat[2][0:-1]:
            _write(c_types[t[0]] + ' ' + t[1] + ', ', file, in_main)
        if stat[2]:
            _write(c_types[stat[2][-1][0]] + ' ' + stat[2][-1][1], file, in_main)
        _write(")\n", file, in_main)
        _write("{\n", file, in_main)
        for s in stat[4]:
            traverse(s, file, cur_fun)
        _write("}\n\n", file, in_main)
        in_main = old_in_main
        cur_fun = old_cur_fun
    elif cmd == "DECL":
        funmap[stat[1]] = stat[3]
        _write("extern " + c_types.get(stat[3], "void") + ' ' + stat[1], file, in_main)
        _write("(", file, in_main)
        for t in stat[2][0:-1]:
            _write(c_types[t[0]] + ' ' + t[1] + ', ', file, in_main)
        if stat[2]:
            _write(c_types[stat[2][-1][0]] + ' ' + stat[2][-1][1], file, in_main)
        _write(")" + end, file, in_main)
        pass
    elif cmd == "RESIZE":
        _write("f4_resize(" + stat[1][1] + ", " + _expr(stat[2]) + ")" + end, file, in_main)
    elif cmd == 'RET':
        _write("return " + _expr(stat[1]) + end, file, in_main)
    elif cmd == "EXPR":
        _write(_expr(stat[1]) + end, file, in_main)
    if with_endline:
        _write('\n', file, in_main)


def _write(str, file, to_main=True):
    global _main
    if to_main:
        _main += str
    else:
        file.write(str)


def _write_indent(file, to_main=True):
    _write(" " * 4 * _indent, file, to_main)


def _expr(expr):
    op = expr[0]
    if op == 'ADD':
        return "(" + _expr(expr[1]) + " + " + _expr(expr[2]) + ")"
    elif op == 'SUB':
        return "(" + _expr(expr[1]) + " - " + _expr(expr[2]) + ")"
    elif op == 'MUL':
        return "(" + _expr(expr[1]) + " * " + _expr(expr[2]) + ")"
    elif op == 'DIV':
        return "(" + _expr(expr[1]) + " / " + _expr(expr[2]) + ")"
    elif op == 'EQL':
        return "(" + _expr(expr[1]) + " == " + _expr(expr[2]) + ")"
    elif op == 'LEQ':
        return "(" + _expr(expr[1]) + " <= " + _expr(expr[2]) + ")"
    elif op == 'GEQ':
        return "(" + _expr(expr[1]) + " >= " + _expr(expr[2]) + ")"
    elif op == 'LES':
        return "(" + _expr(expr[1]) + " < " + _expr(expr[2]) + ")"
    elif op == 'GTR':
        return "(" + _expr(expr[1]) + " > " + _expr(expr[2]) + ")"
    elif op in ('IND', 'ELEM'):
        return "((" + c_types[getElementType(varmap[expr[1]])] + "*)(" + expr[1] + "->array))[" + _expr(
            expr[2]) + "- 1]"
    elif op == 'NEG':
        return "-" + _expr(expr[1])
    elif op in ('INT', 'REAL', 'CHAR', 'STR'):
        return "(" + c_types[op] + ")(" + _literal(op, expr[1]) + ")"
    elif op == 'ID':
        return expr[1]
    elif op == 'SIZE':
        return expr[1] + "->size"
    elif op == 'CALL':
        ret = expr[1] + "("
        for e in expr[2][0:-1]:
            ret += _expr(e) + ", "
        if expr[2]:
            ret += _expr(expr[2][-1])
        ret += ")"
        return ret


def _literal(type, lit):
    r = str(lit)
    if type == "CHAR":
        r = "'" + r + "'"
    elif type in ("STR", "STRING"):
        r = '"' + r + '"'
    return r