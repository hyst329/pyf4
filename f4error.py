__author__ = 'hyst329'

errors = {
    # Placeholder for code 1
    # Placeholder for code 2
    'NOENDIF': (3, 'No endif specified'),
    'IFERR': (4, 'Error in IF conditional expression'),
    # Placeholder for code 5
    # Placeholder for code 6
    # Placeholder for code 7
    # Placeholder for code 8
    'NOVAR': (9, 'No such variable')
}


def error(code):
    e = errors.get(code, (0, 'Unknown error'))
    print('Error: %s (code: %03d)' % (e[1], e[0]))
    raise RuntimeError()