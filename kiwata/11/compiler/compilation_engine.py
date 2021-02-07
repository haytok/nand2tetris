from jack_tokenizer import Tokenizer
from const import *

from symbol_table import SymbolTable


class CompilationEngine:
    def __init__(self, input_texts, output_file_path):
        self.tokenizer = Tokenizer(input_texts)
        self.wf = open(output_file_path, 'w')
        self.elements = []

        self.symbol_table = SymbolTable()
        self.symbol_table.show_tables()

        # tokens
        self.op_tokens = [
            Tokens.PLUS,
            Tokens.MINUS,
            Tokens.MULTI,
            Tokens.DIV,
            Tokens.AND,
            Tokens.OR,
            Tokens.LESS_THAN,
            Tokens.GREATER_THAN,
            Tokens.EQUAL,
        ]
        self.unary_op_tokens = [
            Tokens.MINUS,
            Tokens.TILDE,
        ]
        self.statement_tokens = [
            Tokens.LET,
            Tokens.IF,
            Tokens.WHILE,
            Tokens.DO,
            Tokens.RETURN,
        ]
        self.keyword_constant_tokens = [
            Tokens.TRUE,
            Tokens.FALSE,
            Tokens.NULL,
            Tokens.THIS,
        ]

        # SymbolTable を作成するのに必要な変数
        self.class_name = None
        self.kind = None
        self.var_type = None
        self.var_name = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.wf.close()
    
    def compile(self):
        self.compile_class()

    def compile_class(self):
        self.write_element_start('class')

        # class
        self.compile_keyword([Tokens.CLASS])
        #
        self.class_name = self.tokenizer.see_next()
        # className
        self.compile_class_name()
        # {
        self.compile_keyword([Tokens.LEFT_CURLY_BRACKET])
        # classVarDec*
        while self.tokenizer.next_is([Tokens.STATIC, Tokens.FIELD]):
            self.compile_class_var_dec()
        # subroutineDec*
        while self.tokenizer.next_is(
            [Tokens.CONSTRUCTOR, Tokens.FUNCTION, Tokens.METHOD, Tokens.VOID]
        ):
            self.compile_subroutine_dec()
        # }
        self.compile_keyword([Tokens.RIGHT_CURLY_BRACKET])

        self.write_element_end('class')

    def compile_keyword(self, keyword_tokens):
        self.tokenizer.advance()
        if self.tokenizer.current_token in keyword_tokens:
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_class_name(self):
        self.compile_identifier()

    def compile_var_dec(self):
        self.write_element_start('varDec')

        self.kind = SymbolKind.VAR
        # var
        self.compile_keyword([Tokens.VAR])
        # type
        self.compile_type()
        self.var_type = self.tokenizer.current_token
        # varName
        self.compile_var_name()
        self.var_name = self.tokenizer.current_token
        self.symbol_table.define(self.var_name, self.var_type, self.kind)
        # (',' varName)*
        while self.tokenizer.next_is([Tokens.COMMA]):
            self.compile_symbol([Tokens.COMMA])
            self.compile_var_name()
            self.var_name = self.tokenizer.current_token
            self.symbol_table.define(self.var_name, self.var_type, self.kind)
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('varDec')

    def get_kind(self, token):
        if token == Tokens.STATIC:
            return SymbolKind.STATIC
        elif token == Tokens.FIELD:
            return SymbolKind.FIELD
        else:
            return ValueError('Invalid token in get_kind.')

    def compile_class_var_dec(self):
        self.write_element_start('classVarDec')

        # static or field
        self.compile_keyword([Tokens.STATIC, Tokens.FIELD])
        self.kind = self.get_kind(self.tokenizer.current_token)
        # type
        self.compile_type()
        self.var_type = self.tokenizer.current_token
        # varName
        self.compile_var_name()
        self.var_name = self.tokenizer.current_token
        self.symbol_table.define(self.var_name, self.var_type, self.kind)

        # (, varName)*
        while self.tokenizer.next_is([Tokens.COMMA]):
            self.compile_symbol([Tokens.COMMA])
            self.compile_var_name()
            self.var_name = self.tokenizer.current_token
            self.symbol_table.define(self.var_name, self.var_type, self.kind)

        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('classVarDec')

    def compile_subroutine_dec(self):
        # Symbol Table の初期化
        self.symbol_table.start_subroutine()

        self.write_element_start('subroutineDec')

        # constructor or function or method or void
        self.compile_keyword(
            [Tokens.CONSTRUCTOR, Tokens.FUNCTION, Tokens.METHOD, Tokens.VOID]
        )

        # Symbol Table の作成
        if self.tokenizer.current_token == Tokens.METHOD:
            self.symbol_table.define('$this', self.class_name, SymbolKind.ARG)

        # void or type
        if self.tokenizer.next_is([Tokens.VOID]):
            self.compile_keyword([Tokens.VOID])
        else:
            self.compile_type()
        # subroutineName
        self.compile_subroutine_name()
        # (
        self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
        # parameterList
        self.compile_parameter_list()
        # )
        self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        # subroutineBody
        self.compile_subroutine_body()

        self.write_element_end('subroutineDec')

    def compile_subroutine_body(self):
        self.write_element_start('subroutineBody')
        # {
        self.compile_keyword([Tokens.LEFT_CURLY_BRACKET])
        # varDec*
        while not self.tokenizer.next_is(self.statement_tokens):
            self.compile_var_dec()
        # statements
        self.compile_statements()
        # }
        self.compile_keyword([Tokens.RIGHT_CURLY_BRACKET])
        self.write_element_end('subroutineBody')

    def compile_integer_constant(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, IntegerToken):
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_string_constant(self):
        self.tokenizer.advance()
        if isinstance(self.tokenizer.current_token, StringToken):
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_op(self):
        self.compile_symbol(self.op_tokens)

    def compile_term(self):
        self.write_element_start('term')

        if isinstance(self.tokenizer.see_next(), IntegerToken):
            self.compile_integer_constant()
        elif isinstance(self.tokenizer.see_next(), StringToken):
            self.compile_string_constant()
        elif isinstance(self.tokenizer.see_next(), KeywordToken):
            self.compile_keyword(self.keyword_constant_tokens)
        elif isinstance(self.tokenizer.see_next(), IdentifierToken):
            # varName[expression]
            if self.tokenizer.next_is([Tokens.LEFT_SQUARE_BRACKET], index=1):
                # varName
                self.compile_var_name()
                # [
                self.compile_symbol([Tokens.LEFT_SQUARE_BRACKET])
                # expression
                self.compile_expression()
                # ]
                self.compile_symbol([Tokens.RIGHT_SQUARE_BRACKET])
            # subroutineCall
            elif self.tokenizer.next_is([Tokens.LEFT_ROUND_BRACKET, Tokens.DOT], index=1):
                self.compile_subroutine_call()
            # varName
            else:
                self.compile_var_name()
        elif self.tokenizer.next_is([Tokens.LEFT_ROUND_BRACKET]):
            # (
            self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
            # expression
            self.compile_expression()
            # )
            self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        elif self.tokenizer.next_is(self.unary_op_tokens):
            # unaryOp
            self.compile_symbol(self.unary_op_tokens)
            # term
            self.compile_term()
        else:
            self.raise_syntax_error(self.tokenizer.see_next())

        self.write_element_end('term')

    def compile_expression(self):
        self.write_element_start('expression')

        self.compile_term()
        # (op term)*
        if self.tokenizer.next_is(self.op_tokens):
            self.compile_op()
            self.compile_term()

        self.write_element_end('expression')

    def compile_let_statement(self):
        self.write_element_start('letStatement')

        # let
        self.compile_keyword([Tokens.LET])
        # varName
        self.compile_var_name()
        # ('[' expression ']')?
        if self.tokenizer.next_is([Tokens.LEFT_SQUARE_BRACKET]):
            # [
            self.compile_symbol([Tokens.LEFT_SQUARE_BRACKET])
            # expression
            self.compile_expression()
            # ]
            self.compile_symbol([Tokens.RIGHT_SQUARE_BRACKET])
        # =
        self.compile_symbol([Tokens.EQUAL])
        # expression
        self.compile_expression()
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('letStatement')

    def compile_expression_list(self):
        self.write_element_start('expressionList')

        # (expression (',' expression)* )?
        if not self.tokenizer.next_is([Tokens.RIGHT_ROUND_BRACKET]):
            # expression
            self.compile_expression()
            # (',' expression)*
            while self.tokenizer.next_is([Tokens.COMMA]):
                self.compile_symbol([Tokens.COMMA])
                self.compile_expression()

        self.write_element_end('expressionList')

    def compile_subroutine_call(self):
        # ( のケース
        if self.tokenizer.next_is([Tokens.LEFT_ROUND_BRACKET], index=1):
            # subroutinename
            self.compile_subroutine_name()
            # (
            self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
            # expressionList
            self.compile_expression_list()
            # )
            self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        # . のケース
        elif self.tokenizer.next_is([Tokens.DOT], index=1):
            # className | varName
            self.compile_class_name()
            # .
            self.compile_symbol([Tokens.DOT])
            # subroutineName
            self.compile_subroutine_name()
            # (
            self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
            # expressionList
            self.compile_expression_list()
            # )
            self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        else:
            self.raise_syntax_error(self.tokenizer.see_next(index=1))

    def compile_do_statement(self):
        self.write_element_start('doStatement')

        # do
        self.compile_keyword([Tokens.DO])
        # subroutineCall
        self.compile_subroutine_call()
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('doStatement')

    def compile_return_statement(self):
        self.write_element_start('returnStatement')

        # return
        self.compile_keyword([Tokens.RETURN])
        # expression?
        if not self.tokenizer.next_is([Tokens.SEMICOLON]):
            self.compile_expression()
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('returnStatement')

    def compile_if_statement(self):
        self.write_element_start('ifStatement')

        # if
        self.compile_keyword([Tokens.IF])
        # (
        self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
        # expression
        self.compile_expression()
        # )
        self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        # {
        self.compile_symbol([Tokens.LEFT_CURLY_BRACKET])
        # statements
        self.compile_statements()
        # }
        self.compile_symbol([Tokens.RIGHT_CURLY_BRACKET])
        # (else { statemens })
        if self.tokenizer.next_is([Tokens.ELSE]):
            # else
            self.compile_keyword([Tokens.ELSE])
            # {
            self.compile_symbol([Tokens.LEFT_CURLY_BRACKET])
            # statements
            self.compile_statements()
            # }
            self.compile_symbol([Tokens.RIGHT_CURLY_BRACKET])

        self.write_element_end('ifStatement')

    def compile_while_statement(self):
        self.write_element_start('whileStatement')

        # while
        self.compile_keyword([Tokens.WHILE])
        # (
        self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
        # expression
        self.compile_expression()
        # )
        self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        # {
        self.compile_symbol([Tokens.LEFT_CURLY_BRACKET])
        # statements
        self.compile_statements()
        # }
        self.compile_symbol([Tokens.RIGHT_CURLY_BRACKET])

        self.write_element_end('whileStatement')

    def compile_statement(self):
        if self.tokenizer.next_is([Tokens.LET]):
            self.compile_let_statement()
        elif self.tokenizer.next_is([Tokens.IF]):
            self.compile_if_statement()
        elif self.tokenizer.next_is([Tokens.WHILE]):
            self.compile_while_statement()
        elif self.tokenizer.next_is([Tokens.DO]):
            self.compile_do_statement()
        elif self.tokenizer.next_is([Tokens.RETURN]):
            self.compile_return_statement()
        else:
            self.raise_syntax_error(self.tokenizer.see_next())

    def compile_statements(self):
        self.write_element_start('statements')
        while self.tokenizer.next_is(
            [Tokens.LET, Tokens.IF, Tokens.WHILE, Tokens.DO, Tokens.RETURN]
        ):
            self.compile_statement()
        self.write_element_end('statements')

    def compile_parameter_list(self):
        self.write_element_start('parameterList')
        if self.tokenizer.see_next() in [Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN] \
        or isinstance(self.tokenizer.see_next(), StringToken):
            self.kind = SymbolKind.ARG
            # type
            self.compile_type()
            self.var_type = self.tokenizer.current_token
            # varName
            self.compile_var_name()
            self.var_name = self.tokenizer.current_token
            self.symbol_table.define(self.var_name, self.var_type, self.kind)
            # (, type varName)*
            while self.tokenizer.next_is([Tokens.COMMA]):
                self.compile_symbol([Tokens.COMMA])
                self.compile_type()
                self.var_type = self.tokenizer.current_token
                self.compile_var_name()
                self.var_name = self.tokenizer.current_token
                self.symbol_table.define(self.var_name, self.var_type, self.kind)
        self.write_element_end('parameterList')

    def compile_type(self):
        self.tokenizer.advance()
        if self.tokenizer.current_token in [Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN] \
        or isinstance(self.tokenizer.current_token, IdentifierToken):
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_symbol(self, keyword_tokens):
        self.tokenizer.advance()
        if self.tokenizer.current_token in keyword_tokens:
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_subroutine_name(self):
        self.compile_identifier()

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
