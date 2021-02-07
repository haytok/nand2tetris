import re

# トークンタイプ
class TokenType:
    KEYWORD_TYPE = 0
    SYMBOL_TYPE = 1
    INTEGER_TYPE = 2
    STRING_TYPE = 3
    IDENTIFIER_TYPE = 4


# シンボルタイプ
class SymbolKind:
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3


def get_element(type):
    if type == TokenType.KEYWORD_TYPE:
        return 'keyword'
    elif type == TokenType.SYMBOL_TYPE:
        return 'symbol'
    elif type == TokenType.INTEGER_TYPE:
        return 'integerConstant'
    elif type == TokenType.STRING_TYPE:
        return 'stringConstant'
    elif type == TokenType.IDENTIFIER_TYPE:
        return 'identifier'
    else:
        raise ValueError('Invalid type.')


class BaseToken:
    def __init__(self, token, token_displayed=None):
        self.token = token
        if token_displayed:
            self.token_displayed = token_displayed
        else:
            self.token_displayed = token

    def __str__(self):
        return str(self.token_displayed)


class KeywordToken(BaseToken):
    def __init__(self, token, token_displayed=None):
        super().__init__(token, token_displayed)
        self.type = TokenType.KEYWORD_TYPE


class SymbolToken(BaseToken):
    def __init__(self, token, token_displayed=None):
        super().__init__(token, token_displayed)
        self.type = TokenType.SYMBOL_TYPE


class IntegerToken(BaseToken):
    def __init__(self, token, token_displayed=None):
        super().__init__(int(token), token_displayed)
        self.type = TokenType.INTEGER_TYPE
        if self.token > 32767:
            raise ValueError('Invalid integer.')


class StringToken(BaseToken):
    def __init__(self, token, token_displayed=None):
        super().__init__(token[1:-1], token_displayed)
        self.type = TokenType.STRING_TYPE


class IdentifierToken(BaseToken):
    def __init__(self, token, token_displayed=None):
        super().__init__(token, token_displayed)
        self.type = TokenType.IDENTIFIER_TYPE


class Tokens:
    # Keyword
    CLASS = KeywordToken('class')
    CONSTRUCTOR = KeywordToken('constructor')
    FUNCTION = KeywordToken('function')
    METHOD = KeywordToken('method')
    FIELD = KeywordToken('field')
    STATIC = KeywordToken('static')
    VAR = KeywordToken('var')
    INT = KeywordToken('int')
    CHAR = KeywordToken('char')
    BOOLEAN = KeywordToken('boolean')
    VOID = KeywordToken('void')
    TRUE = KeywordToken('true')
    FALSE = KeywordToken('false')
    NULL = KeywordToken('null')
    THIS = KeywordToken('this')
    LET = KeywordToken('let')
    DO = KeywordToken('do')
    IF = KeywordToken('if')
    ELSE = KeywordToken('else')
    WHILE = KeywordToken('while')
    RETURN = KeywordToken('return')
    # Symbol
    LEFT_CURLY_BRACKET = SymbolToken('{')
    RIGHT_CURLY_BRACKET = SymbolToken('}')
    LEFT_ROUND_BRACKET = SymbolToken('(')
    RIGHT_ROUND_BRACKET = SymbolToken(')')
    LEFT_SQUARE_BRACKET = SymbolToken('[')
    RIGHT_SQUARE_BRACKET = SymbolToken(']')
    DOT = SymbolToken('.')
    COMMA = SymbolToken(',')
    SEMICOLON = SymbolToken(';')
    PLUS = SymbolToken('+')
    MINUS = SymbolToken('-')
    MULTI = SymbolToken('*')
    DIV = SymbolToken('/')
    AND = SymbolToken('&', token_displayed='&amp;')
    OR = SymbolToken('|')
    LESS_THAN = SymbolToken('<', token_displayed='&lt;')
    GREATER_THAN = SymbolToken('>', token_displayed='&gt;')
    EQUAL = SymbolToken('=')
    TILDE = SymbolToken('~')


# 終端記号のパターン
KEYWORD_PATTERN = {
  'class': Tokens.CLASS,
  'constructor': Tokens.CONSTRUCTOR,
  'function': Tokens.FUNCTION,
  'method': Tokens.METHOD,
  'field': Tokens.FIELD,
  'static': Tokens.STATIC,
  'var': Tokens.VAR,
  'int': Tokens.INT,
  'char': Tokens.CHAR,
  'boolean': Tokens.BOOLEAN,
  'void': Tokens.VOID,
  'true': Tokens.TRUE,
  'false': Tokens.FALSE,
  'null': Tokens.NULL,
  'this': Tokens.THIS,
  'let': Tokens.LET,
  'do': Tokens.DO,
  'if': Tokens.IF,
  'else': Tokens.ELSE,
  'while': Tokens.WHILE,
  'return': Tokens.RETURN,
}
SYMBOL_PATTERN = {
  '{': Tokens.LEFT_CURLY_BRACKET,
  '}': Tokens.RIGHT_CURLY_BRACKET,
  '(': Tokens.LEFT_ROUND_BRACKET,
  ')': Tokens.RIGHT_ROUND_BRACKET,
  '[': Tokens.LEFT_SQUARE_BRACKET,
  ']': Tokens.RIGHT_SQUARE_BRACKET,
  '.': Tokens.DOT,
  ',': Tokens.COMMA,
  ';': Tokens.SEMICOLON,
  '+': Tokens.PLUS,
  '-': Tokens.MINUS,
  '*': Tokens.MULTI,
  '/': Tokens.DIV,
  '&': Tokens.AND,
  '|': Tokens.OR,
  '<': Tokens.LESS_THAN,
  '>': Tokens.GREATER_THAN,
  '=': Tokens.EQUAL,
  '~': Tokens.TILDE,
}
INTEGER_PATTERN = re.compile(r'^(0|[1-9][0-9]{,4})$')
STRING_PATTERN = re.compile(r'^"[^"]*"$')
IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

if __name__ == '__main__':
    instance = KEYWORD_PATTERN['class']
    print(instance.type, instance.token)
    instance = SYMBOL_PATTERN['<']
    print(instance.type, instance.token, instance.token_displayed)
    instance = IntegerToken('999999')
    print(instance.type, instance.token)
