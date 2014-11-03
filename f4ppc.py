__author__ = 'hyst329'

used_modules = set()
path = 'library/'


def preprocess(raw):
    global used_modules
    lines = raw.split('\n')
    for i in range(len(lines)):
        l = lines[i]
        p = l.find('#')
        if p >= 0:
            l = l[0:p]
        if len(l) and l[0] == '@':
            d = l[1:]
            d = d.split(' ')
            if d[0] == 'use':
                mod = d[1]
                if mod not in used_modules:
                    used_modules.add(mod)
                    cont = open(path + mod + '.f4', 'r').read()
                    l = preprocess(cont)
            else:
                l = ''
        if isinstance(l, list):
            lines[i:i + 1] = l
        elif isinstance(l, str):
            lines[i] = l

    return lines


def to_string(lines):
    return '\n'.join(lines)