import os
from f4error import error

__author__ = 'hyst329'

used_modules = set()
ppc_path = ['library']


def preprocess(raw):
    global used_modules
    lines = raw.split('\n')
    i = 0
    try:
        while 1:
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
                        for p in ppc_path:
                            path = p + "/" + mod.replace('.', '/') + '.f4'
                            if os.path.exists(path):
                                break
                        cont = open(path, 'r').read()
                        l = preprocess(cont)
                else:
                    error('INVDIR', d[0])
                    l = ''
            if isinstance(l, list):
                lines[i:i + 1] = l
            elif isinstance(l, str):
                lines[i] = l
            i += 1
    except IndexError:
        return lines


def to_string(lines):
    return '\n'.join(lines)