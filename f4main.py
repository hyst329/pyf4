import sys
import pickle
from termcolor import cprint
from f4error import error

from f4interp import interpret
import f4parser
from f4ppc import preprocess, to_string
from f4ver import verstr

__author__ = 'hyst329'


def main():
    if len(sys.argv) == 1:
        print("PyF4 --- F4PL implementation in Python\n")
        print("Version %s" % verstr)
        print("Usage: PyF4 infile.f4 [options]\n")
        return 0
    try:
        if len(sys.argv) == 2 or sys.argv[2] == '-i':
            mode = 'int'
        elif sys.argv[2] == '-c':
            mode = 'ast'
        elif sys.argv[2] == '-b':
            mode = 'bytecode'
        else:
            print("Unknown format specified: '%s'" % sys.argv[2])
            return
        if mode in ('int', 'ast'):
            cont = open(sys.argv[1], 'r').read()
            if cont[-1] != '\n':
                cont += '\n'
            cont = to_string(preprocess(cont))
            parser = f4parser.parser
            res = parser.parse(cont)
            # if parser.error:
            # print "Error"
        if mode == 'int':
            print('Interpreting...')
            interpret(res)
        elif mode == 'ast':
            print("AST:\n", res)
            pickle.dump(res, open(sys.argv[1] + ".ast", 'wb'), 2)
        elif mode == 'bytecode':
            print("Experimental bytecode mode")
            res = pickle.load(open(sys.argv[1], 'rb'))
            print(res)
            interpret(res)
        return 0
    except IOError as e:
        error('NOFILE', e.filename, e.strerror, e.errno, exc=0)
    except RuntimeError:
        cprint('Fatal errors, translation terminated', 'grey', 'on_red')
        return 1


if __name__ == "__main__":
    main()