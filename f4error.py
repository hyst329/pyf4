__author__ = 'hyst329'
from termcolor import cprint

errors = {
    'NOFILE': (1, 'File "%s" cannot be opened : %s (ERRNO code %s)'),
    'INVTOK': (2, 'Invalid token %s'),
    'NOENDIF': (3, 'No endif specified'),
    'IFERR': (4, 'Error in IF conditional expression'),
    'ELSEERR': (5, 'Error in ELSE part of the conditional expression'),
    'INVDIR': (6, 'Invalid preprocessor directive: %s'),
    'INVSIZE': (7, 'Invalid size of the array %s : %s (must be > 0)'),
    'MPELSE': (8, 'Misplaced ELSE'),
    'NOVAR': (9, 'No such variable "%s"'),
    'INVIND': (10, "Invalid index: must be an integer expression"),
    'RETERR': (11, 'Return error: must be expression'),
    'ASERR': (12, 'Assignment error: assigned value must be an expression'),
    'DECLERR': (13, 'Declaration error: assigned value must be an expression'),
    'INVELI': (14, 'Error in expression list'),
    'INVALI': (15, 'Error in argument list'),
    'INVID': (16, 'Invalid identifier'),
    'INERR': (17, 'Input error: must be identifier'),
    'OUTERR': (18, 'Output error: must be expression'),
}


def error(code, *args, **kwargs):
    e = errors.get(code, (0, 'Unknown error'))
    cprint('Error: %s (code: %03d)' % (e[1] % args, e[0]), 'red')
    if kwargs.get('exc', 1):
        raise RuntimeError()