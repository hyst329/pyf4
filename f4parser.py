from ply import yacc
from f4error import error

import f4lex
from f4log import log

# Parsing file for F4 programming language
__author__ = 'hyst329'

tokens = f4lex.tokens

precedence = (
    ('nonassoc', 'equals', 'leq', 'geq', 'less', 'greater'),
    ('left', 'plus', 'minus'),
    ('left', 'mult', 'divide'),
)


# Main program
def p_program(p):
    """program : instseq"""
    p[0] = p[1]


# Instruction sequence
def p_instseq(p):
    """instseq : instseq instruction
               | instruction"""
    if len(p) == 2:
        if not p[0]:
            p[0] = []
        p[0].append(p[1])
    else:
        if not p[0]:
            p[0] = []
        p[0] = p[1]
        if p[2]:
            p[0].append(p[2])


# Instruction
def p_instruction(p):
    """instruction : newline
                   | statement newline"""
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = ('BLANK',)


# IF statement forms
def p_instruction_if(p):
    """instruction : if expression newline instseq endif"""
    p[0] = ('IF', p[2], p[4], ('BLANK',))


def p_instruction_if_bad0(p):
    """instruction : if error newline instseq endif"""
    error('IFERR')


def p_instruction_if_bad1(p):
    """instruction : if expression newline instseq error"""
    error('NOENDIF')


def p_instruction_ifelse(p):
    """instruction : if expression newline instseq else newline instseq endif"""
    p[0] = ('IF', p[2], p[4], p[7])


# LOOP statement form
def p_instruction_loop(p):
    """instruction : loop statement comma expression comma statement newline instseq endloop"""
    p[0] = ('LOOP', p[2], p[4], p[6], p[8])


# Functions
def p_instruction_fun(p):
    """instruction : fun ident colon arglist rarrow type newline instseq endfun"""
    p[0] = ('FUN', p[2], p[4], p[6], p[8])


def p_instruction_funvoid(p):
    """instruction : fun ident colon arglist newline instseq endfun"""
    p[0] = ('FUN', p[2], p[4], None, p[6])


def p_instruction_return(p):
    """instruction : return expression"""
    p[0] = ('RET', p[2])


# Statement
def p_statement_decl(p):
    """statement : declaration"""
    p[0] = p[1]


def p_statement_in(p):
    """statement : in ident"""
    p[0] = ('IN', ('ID', p[2]))


def p_statement_inelem(p):
    """statement : in ident point factor"""
    p[0] = ('IN', ('ELEM', p[2], p[4]))


def p_statement_out(p):
    """statement : out expression"""
    p[0] = ('OUT', p[2])


def p_statement_ass(p):
    """statement : assignment"""
    p[0] = p[1]


def p_statement_debugvar(p):
    """statement : debugvar """
    p[0] = ('DEBUGVAR',)


# Argument list
def p_arglist(p):
    """arglist : type ident comma arglist
               | type ident"""
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = [(p[1], p[2])]
        p[0].extend(p[4])


# Expression list
def p_exprlist(p):
    """exprlist : expression comma exprlist
                | expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]]
        p[0].extend(p[3])


# Type
def p_type(p):
    """type : int
            | real"""
    p[0] = p[1].upper()


# Expression
def p_expression_plus(p):
    """expression : expression plus term"""
    p[0] = ('ADD', p[1], p[3])


def p_expression_minus(p):
    """expression : expression minus term"""
    p[0] = ('SUB', p[1], p[3])


def p_expression_eq(p):
    """expression : factor equals factor"""
    p[0] = ('EQL', p[1], p[3])


def p_expression_leq(p):
    """expression : factor leq factor"""
    p[0] = ('LEQ', p[1], p[3])


def p_expression_geq(p):
    """expression : factor geq factor"""
    p[0] = ('GEQ', p[1], p[3])


def p_expression_less(p):
    """expression : factor less factor"""
    p[0] = ('LES', p[1], p[3])


def p_expression_gtr(p):
    """expression : factor greater factor"""
    p[0] = ('GTR', p[1], p[3])


def p_expression_term(p):
    """expression : term"""
    p[0] = p[1]


# Term
def p_term_times(p):
    """term : term mult factor"""
    p[0] = ('MUL', p[1], p[3])


def p_term_div(p):
    """term : term divide factor"""
    p[0] = ('DIV', p[1], p[3])


def p_term_factor(p):
    """term : factor"""
    p[0] = p[1]


# Factor
def p_factor_int(p):
    """factor : intlit"""
    p[0] = ('INT', p[1])


def p_factor_real(p):
    """factor : reallit"""
    p[0] = ('REAL', p[1])


def p_factor_ident(p):
    """factor : ident"""
    p[0] = ('ID', p[1])


def p_factor_expr(p):
    """factor : lparen expression rparen"""
    p[0] = p[2]


def p_factor_arrelem(p):
    """factor : ident point factor"""
    p[0] = ('IND', p[1], p[3])


def p_factor_fun(p):
    """factor : ident lparen exprlist rparen"""
    p[0] = ('CALL', p[1], p[3])


# Declaration
def p_declaration_ident(p):
    """declaration : type ident
                   | type ident assign expression"""
    if len(p) == 3:
        p[0] = ('NEW', p[1], p[2], (p[1], 0))
    else:
        p[0] = ('NEW', p[1], p[2], p[4])


def p_declaration_array(p):
    """declaration : type point factor ident"""
    p[0] = ('NEWARR', p[1], p[3], p[4])


# Assignment
def p_assignment(p):
    """assignment : ident assign expression"""
    p[0] = ('MOV', (p[1],), p[3])


def p_assignment_elem(p):
    """assignment : ident point factor assign expression"""
    p[0] = ('MOV', ('ELEM', p[1], p[3]), p[5])


# Error rule for syntax errors

def p_error(p):
    if not p:
        print("Syntax error, translation terminated")


parser = yacc.yacc(debug=True, debuglog=log)