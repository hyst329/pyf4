from f4error import error

__author__ = 'hyst329'

from ply import *

# Lexing file for F4 programming language

tokens = [
    # Some literals
    'intlit',
    'reallit',
    'chrlit',
    'strlit',
    'ident',
    # 2 char operators
    'equals',
    'leq',
    'geq',
    'aplus',
    'aminus',
    'larrow',
    'rarrow',
    # 1 char operators
    'plus',
    'minus',
    'mult',
    'divide',
    'less',
    'greater',
    'assign',
    'lparen',
    'rparen',
    'colon',
    'semi',
    'comma',
    'point',
    # New line
    'newline'
]

keywords = (
    'if',
    'else',
    'endif',
    'fun',
    'endfun',
    'declare',
    'loop',
    'endloop',
    'return',
    'use',
    'resize',
    'size',
    # Basic types
    'int',
    'real',
    'logical',
    'char',
    'string',
    # Basic operations
    'in',
    'out',
    'debugvar'
)

tokens += keywords

t_ignore = ' \t'

t_equals = r'=='
t_leq = r'\<='
t_geq = r'\>='
t_less = r'\<'
t_greater = r'\>'
t_aplus = r'\+='
t_aminus = r'\-='
t_larrow = r'\<\-'
t_rarrow = r'\-\>'

t_plus = r'\+'
t_minus = r'\-'
t_mult = r'\*'
t_divide = r'\/'
t_assign = r'='
t_lparen = r'\('
t_rparen = r'\)'
t_colon = r'\:'
t_semi = r'\;'
t_comma = r'\,'
t_point = r'\.'


def t_ident(t):
    r"""[a-zA-Z][a-zA-Z0-9]*"""
    if t.value in keywords:
        t.type = t.value
    return t


def t_newline(t):
    r"""\n"""
    t.lexer.lineno += 1
    return t


def t_reallit(t):
    r"""\d+[\.\,]\d+"""
    t.value = float(t.value)
    return t


def t_intlit(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_chrlit(t):
    r"""'[^(')]'"""
    t.value = t.value[1:-1]
    return t


def t_strlit(t):
    r""" "[^(")]+" """
    t.value = t.value[1:-1]
    return t


def t_error(t):
    error('INVTOK', t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()