__author__ = 'tram'

# The command structure:
# byte 0 - operator code,
# bytes 1-2 - 1st operand address
# bytes 3-4 - 2nd operand address if present

commands = {
    'ADD': 0x01,
    'SUB': 0x02,
    'MUL': 0x03,
    'DIV': 0x04,
    'EQL': 0x10,
    'LEQ': 0x11,
    'GEQ': 0x12,
    'LES': 0x13,
    'GTR': 0x14,
    'NEG': 0x05,
    'IND': 0x40,
}

def bytecode(res):
    pass