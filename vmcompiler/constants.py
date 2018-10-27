POINTER_MAPS = {
    'local': 'LCL',
    'argument': 'ARG',
    'this': 'THIS',
    'that': 'THAT'
}

# Memory Access Command Constants
PUSH_CONSTANT = (
    '// {0}\n'
    '@{1}\n'
    'D=A\n'
    '@SP\n'
    'A=M\n'
    'M=D\n'
    '@SP\n'
    'M=M+1\n'
)

PUSH_TEMP = (
    '// {0}\n'
    '@5\n'
    'D=A\n'
    '@{1}\n'
    'D=D+A\n'
    'A=D\n'
    'D=M\n'
    '@SP\n'
    'A=M\n'
    'M=D\n'
    '@SP\n'
    'M=M+1\n'
)

POP_TEMP = (
    '// {0}\n'
    '@5\n'
    'D=A\n'
    '@{1}\n'
    'D=D+A\n'
    '@addr\n'
    'M=D\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M\n'
    '@addr\n'
    'A=M\n'
    'M=D\n'
)

PUSH_REG_SEGMENT = (
    '// {0}\n'
    '@{1}\n'
    'D=A\n'
    '@{2}\n'
    'D=D+M\n'
    'A=D\n'
    'D=M\n'
    '@SP\n'
    'A=M\n'
    'M=D\n'
    '@SP\n'
    'M=M+1\n'
)

POP_REG_SEGMENT = (
    '// {0}\n'
    '@{1}\n'
    'D=A\n'
    '@{2}\n'
    'D=D+M\n'
    '@addr\n'
    'M=D\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M\n'
    '@addr\n'
    'A=M\n'
    'M=D\n'
)

PUSH_STATIC = (
    '// {0}\n'
    '@{1}.{2}\n'
    'D=M\n'
    '@SP\n'
    'A=M\n'
    'M=D\n'
    '@SP\n'
    'M=M+1\n'
)

POP_STATIC = (
    '// {0}\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M\n'
    '@{1}.{2}\n'
    'M=D\n'
)

POINTER_MAPPING = {
    '0': 'THIS',
    '1': 'THAT'
}

PUSH_POINTER = (
    '// {0}\n'
    '@{1}\n'
    'D=M\n'
    '@SP\n'
    'A=M\n'
    'M=D\n'
    '@SP\n'
    'M=M+1\n'
)

POP_POINTER = (
    '// {0}\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M\n'
    '@{1}\n'
    'M=D\n'
)

# Arithmetic/Logic Command constants
# add, sub, and, or
OPS_MAPS = {
    'add': '+',
    'sub': '-',
    'and': '&',
    'or': '|'
}

OPS = (
    '// {0}\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M{1}D\n'
    '@SP\n'
    'A=M\n'
    'M=D\n'
    '@SP\n'
    'M=M+1\n'
)

# neg, not
NEG_MAPS = {
    'neg': '-',
    'not': '!'
}

NEG = (
    '// {0}\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'M={1}M\n'
    '@SP\n'
    'M=M+1\n'
)

COMP_MAPS = {
    'eq': 'JEQ',
    'gt': 'JGT',
    'lt': 'JLT'
}

COMP = (
    '// {0}\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M\n'
    '@SP\n'
    'M=M-1\n'
    'A=M\n'
    'D=M-D\n'
    '@TRUE{1}\n'
    'D;{2}\n'
    '@SP\n'
    'A=M\n'
    'M=0\n'
    '@FALSE{1}\n'
    '0;JMP\n'
    '(TRUE{1})\n'
    '@SP\n'
    'A=M\n'
    'M=-1\n'
    '(FALSE{1})\n'
    '@SP\n'
    'M=M+1\n'
)
