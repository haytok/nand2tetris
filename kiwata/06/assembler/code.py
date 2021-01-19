DEST_TABLE = {
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}

COMP_TABLE = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110111',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

JUMP_TABLE = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

"""
input: memonic
output: 3 bit
ex) D が入力されたら 010 を返す
"""
def get_dest_binary(memonic):
    if memonic is None:
        return '000'
    elif memonic not in DEST_TABLE:
        raise ValueError('Memonic is invalid.')
    return DEST_TABLE[memonic]


"""
input: memonic
output: 7 bit
ex) A が入力されたら 0110000 を返す
"""
def get_comp_binary(memonic):
    if memonic is None or memonic not in COMP_TABLE:
        raise ValueError('Memonic is invalid.')
    return COMP_TABLE[memonic]


"""
input: memonic
output: 3 bit
ex) JGT が入力されたら 001 を返す
"""
def get_jump_binary(memonic):
    if memonic is None:
        return '000'
    elif memonic not in JUMP_TABLE:
        raise ValueError('Memonic is invalid.')
    return JUMP_TABLE[memonic]
