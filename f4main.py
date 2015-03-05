import os
import sys
import pickle
import subprocess
from termcolor import cprint
from f4codegen import generate_c
from f4error import error

from f4interp import interpret
import f4parser
from f4ppc import preprocess, to_string
from f4ver import verstr, vername

__author__ = 'hyst329'


def main():
    if len(sys.argv) == 1:
        print("PyF4 --- F4PL implementation in Python\n")
        print("Version %s '%s'" % (verstr, vername))
        print("Usage: f4main infile.f4 [options]\n")
        return 0
    try:
        if len(sys.argv) == 2 or sys.argv[2] == '-i':
            mode = 'int'
        elif sys.argv[2] == '-c':
            mode = 'ast'
        elif sys.argv[2] == '-b':
            mode = 'from_ast'
        elif sys.argv[2] == '-g':
            mode = 'gen_c'
        elif sys.argv[2] == '-gc':
            mode = 'gen_c_gcc'
        else:
            print("Unknown format specified: '%s'" % sys.argv[2])
            return
        if mode in ('int', 'ast', 'gen_c', 'gen_c_gcc'):
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
        elif mode == 'from_ast':
            print("Experimental AST interpreting mode. May be unsafe")
            res = pickle.load(open(sys.argv[1], 'rb'))
            print(res)
            interpret(res)
        elif mode in ('gen_c', 'gen_c_gcc'):
            if mode == 'gen_c_gcc':
                p = subprocess.Popen("gcc --version", stdout=open(os.devnull, "w"))
                p.communicate()
                if p.returncode:
                    print("GCC not found or works incorrectly,"
                          " but required to compile generated C code... Sorry :(")
                    return
            generate_c(res, open(sys.argv[1] + ".c", 'w'))
            fsize = os.stat(sys.argv[1] + ".c").st_size
            print("%s bytes of C code generated" % fsize)
            if mode == 'gen_c_gcc':
                print("Compiling with GCC...")
                p = subprocess.Popen('gcc ' + sys.argv[1] + ".c" + " -o " + sys.argv[1] + ".exe --std=c99",
                                     stdout=open(os.devnull, "w"))
                p.communicate()
                if p.returncode:
                    print("GCC cannot compile the generated code..."
                          " This maybe was an error, either in your Helen code or"
                          " in the codegen... Sorry :(")
                    return
                print("Executable written to %s with size of %s bytes,"
                      " you can run it and test!" % (sys.argv[1] + ".exe",
                                                     os.stat(sys.argv[1] + ".exe").st_size))
        return 0
    except IOError as e:
        error('NOFILE', e.filename, e.strerror, e.errno, exc=0)
    except RuntimeError:
        cprint('Fatal errors, translation terminated', 'grey', 'on_red')
        return 1


if __name__ == "__main__":
    main()