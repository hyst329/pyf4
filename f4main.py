import sys

from f4interp import interpret
import f4parser


__author__ = 'hyst329'


def main():
    if len(sys.argv) == 1:
        print "PyF4 --- F4PL implementation in Python\n"
        print "Usage: PyF4 infile.f4 [options]\n"
        return 0
    try:
        cont = open(sys.argv[1], 'r').read()
        if cont[-1] != '\n':
            cont += '\n'
        # f4lex.lexer.input(cont)
        # for tok in f4lex.lexer:
        # print tok
        parser = f4parser.parser
        if len(sys.argv) == 2 or sys.argv[2] == '-i':
            mode = 'int'
        elif sys.argv[2] == '-c':
            mode = 'ast'
        else:
            print "Unknown format specified"
            return
        res = parser.parse(cont)
        # if parser.error:
        # print "Error"
        if mode == 'int':
            print 'Interpreting...'
            interpret(res)
        elif mode == 'ast':
            print res

        return 0
    except IOError:
        print "\033[91m File cannot be read"
        return 1


if __name__ == "__main__":
    main()