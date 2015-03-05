from f4error import error

__author__ = 'hyst329'

INT = "INT"
REAL = "REAL"
CHAR = "CHAR"
STRING = "STRING"


def inferType(expr, varmap, funmap):
    op = expr[0]
    if op in ('ADD', 'SUB', 'MUL'):
        return widestType(inferType(expr[1], varmap, funmap), inferType(expr[2], varmap, funmap))
    elif op == 'DIV':
        return REAL if inferType(expr[1], varmap, funmap) == inferType(expr[2], varmap, funmap) == INT else widestType()
    elif op in ('EQL', 'LES', 'GTR', 'LEQ', 'GEQ'):
        return INT
    elif op == 'IND' or op == 'ELEM':
        return getElementType(varmap[expr[1]])
    elif op == 'NEG':
        return inferType(expr[1])
    elif op == 'INT':
        return INT
    elif op == 'REAL':
        return REAL
    elif op == 'CHAR':
        return CHAR
    elif op == 'STR':
        return STRING
    elif op == 'ID':
        return varmap[expr[1]]
    elif op == 'CALL':
        return funmap[expr[1]]


def getElementType(arrayType):
    return arrayType[0:arrayType.rfind('.')]


def widestType(type1, type2):
    if type1 == type2:
        return type1
    elif (type1 == INT and type2 == REAL) or (type1 == REAL and type2 == INT):
        return REAL
    else:
        error('TPEREX')
