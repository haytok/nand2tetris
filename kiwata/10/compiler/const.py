import re

# トークンタイプ
KEYWORD_TYPE = 0
SYMBOL_TYPE = 1
INTEGER_TYPE = 2
STRING_TYPE = 3
IDENTIFIER_TYPE = 4


def get_element(type):
    if type == KEYWORD_TYPE:
        return 'keyword'
    elif type == SYMBOL_TYPE:
        return 'symbol'
    elif type == INTEGER_TYPE:
        return 'integerConstant'
    elif type == STRING_TYPE:
        return 'stringConstant'
    elif type == IDENTIFIER_TYPE:
        return 'identifier'
    else:
        raise ValueError('Invalid type.')


# 終端記号のパターン
KEYWORD_PATTERN = [
  'class',
  'constructor',
  'function',
  'method',
  'field',
  'static',
  'var',
  'int',
  'char',
  'boolean',
  'void',
  'true',
  'false',
  'null',
  'this',
  'let',
  'do',
  'if',
  'else',
  'while',
  'return',
]
SYMBOL_PATTERN = [
  '{',
  '}',
  '(',
  ')',
  '[',
  ']',
  '.',
  ',',
  ';',
  '+',
  '-',
  '*',
  '/',
  '&',
  '|',
  '<',
  '>',
  '=',
  '~',
]
INTEGER_PATTERN = re.compile(r'^(0|[1-9][0-9]{,4})$')
STRING_PATTERN = re.compile(r'^"[^"]*"$')
IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
