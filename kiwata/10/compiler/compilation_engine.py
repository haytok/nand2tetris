from jack_tokenizer import Tokenizer
from const import *


class CompilationEngine:
    def __init__(self, input_texts, output_file_path):
        self.tokenizer = Tokenizer(input_texts)
        self.wf = open(output_file_path, 'w')
        self.elements = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.wf.close()
    
    def compile(self):
        self.compile_class()

    def compile_class(self):
        self.write_element_start('class')

        self.compile_keyword([Tokens.CLASS])
        self.compile_class_name()
        self.compile_keyword([Tokens.LEFT_CURLY_BRACKET])
        # classVarDec*
        while self.tokenizer.next_is([Tokens.STATIC, Tokens.FIELD]):
            self.compile_class_var_dec()
        # subroutineDec*

        # self.compile_keyword([Tokens.RIGHT_CURLY_BRACKET])

        self.write_element_end('class')

    def compile_keyword(self, keyword_tokens):
        self.tokenizer.advance()
        if self.tokenizer.current_token in keyword_tokens:
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_class_name(self):
        self.compile_identifier()

    def compile_class_var_dec(self):
        self.write_element_start('classVarDec')

        # static or field
        self.compile_keyword([Tokens.STATIC, Tokens.FIELD])

        # type
        self.compile_type()

        # varName
        self.compile_var_name()

        # (, varName)*
        while self.tokenizer.next_is([Tokens.COMMA]):
            self.compile_symbol([Tokens.COMMA])
            self.compile_var_name()

        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('classVarDec')

    def compile_type(self):
        self.tokenizer.advance()
        if self.tokenizer.current_token in [Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN] \
        or isinstance(self.tokenizer.current_token, StringToken):
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_symbol(self, keyword_tokens):
        self.tokenizer.advance()
        if self.tokenizer.current_token in keyword_tokens:
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_var_name(self):
        self.compile_identifier()

    def compile_identifier(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, IdentifierToken):
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def write_element_start(self, element_name):
        self.wf.write('<{}> \n'.format(element_name))

    def write_element(self, token):
        element_name = get_element(token.type)
        self.wf.write(
            '<{}> {} </{}>\n'.format(element_name, token, element_name)
        )

    def write_element_end(self, element_name):
        self.wf.write('</{}> \n'.format(element_name))

    def raise_syntax_error(self, token):
        raise ValueError('Invalid syntax of {}'.format(token))
