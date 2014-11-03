__author__ = 'hyst329'

errors = {
    'NOFILE': (1, 'File %s cannot be opened'),
    'INVTOK': (2, 'Invalid token %s'),
    'NOENDIF': (3, 'No endif specified'),
    'IFERR': (4, 'Error in IF conditional expression'),
    # Placeholder for code 5
    # Placeholder for code 6
    # Placeholder for code 7
    # Placeholder for code 8
    'NOVAR': (9, 'No such variable "%s"')
}


def error(code, *args):
    e = errors.get(code, (0, 'Unknown error'))
    print('Error: %s (code: %03d)' % (e[1] % args, e[0]))
    raise RuntimeError()