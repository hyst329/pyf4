import sys
import pickle
from f4error import error

from f4interp import interpret
import f4parser
from f4ppc import preprocess, to_string
from f4ver import version

__author__ = 'hyst329'


def main():
    if len(sys.argv) == 1:
        print("PyF4 --- F4PL implementation in Python\n")
        print("Version %d.%d.%d" % (version["major"], version["minor"], version["patch"]))
        print("Usage: PyF4 infile.f4 [options]\n")
        return 0
    try:
        cont = open(sys.argv[1], 'r').read()
        if cont[-1] != '\n':
            cont += '\n'
        cont = to_string(preprocess(cont))
        parser = f4parser.parser
        if len(sys.argv) == 2 or sys.argv[2] == '-i':
            mode = 'int'
        elif sys.argv[2] == '-c':
            mode = 'ast'
        else:
            print("Unknown format specified")
            return
        res = parser.parse(cont)
        # if parser.error:
        # print "Error"
        if mode == 'int':
            print('Interpreting...')
            interpret(res)
        elif mode == 'ast':
            print(res)
            # pickle.dump(res, open(sys.argv[1] + ".ast", 'w'), 2)

        return 0
    except IOError:
        error('NOFILE', sys.argv[1])
        return 1
    except RuntimeError:
        print('Fatal errors, translation terminated')


if __name__ == "__main__":
    main()