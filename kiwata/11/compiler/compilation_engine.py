from jack_tokenizer import Tokenizer
from const import *

from symbol_table import SymbolTable


class CompilationEngine:
    def __init__(self, input_texts, output_file_path, vmw):
        self.tokenizer = Tokenizer(input_texts)
        self.wf = open(output_file_path, 'w')
        self.vmw = vmw
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

        # VM
        self.subroutine_class_name = None
        self.subroutine_name = None
        self.label_number = 0

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

    def compile_class_var_dec(self):
        self.write_element_start('classVarDec')

        # static or field
        self.compile_keyword([Tokens.STATIC, Tokens.FIELD])
        self.kind = self.get_kind(self.tokenizer.current_token)
        # type
        self.compile_type()
        self.var_type = self.tokenizer.current_token
        # varName
        self.compile_var_name(define=True, var_type=self.var_type, kind=self.kind)

        # (, varName)*
        while self.tokenizer.next_is([Tokens.COMMA]):
            self.compile_symbol([Tokens.COMMA])
            self.compile_var_name(define=True, var_type=self.var_type, kind=self.kind)

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

        # VM
        subroutine_type = self.tokenizer.current_token

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

        # VM
        subroutine_name = self.tokenizer.current_token

        # (
        self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
        # parameterList
        self.compile_parameter_list()
        # )
        self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        # subroutineBody
        self.compile_subroutine_body(subroutine_type, subroutine_name)

        self.write_element_end('subroutineDec')

    def compile_subroutine_body(self, subroutine_type, subroutine_name):
        self.write_element_start('subroutineBody')


        # {
        self.compile_keyword([Tokens.LEFT_CURLY_BRACKET])
        # varDec*
        local_var_counts = 0
        while not self.tokenizer.next_is(self.statement_tokens):
            counts = self.compile_var_dec()
            local_var_counts += counts

        # VM
        function_name = '{}.{}'.format(self.class_name, subroutine_name)
        self.vmw.write_function(function_name, local_var_counts)
        if subroutine_type == Tokens.CONSTRUCTOR:
            self.vmw.write_push(
                SegmentType.CONST,
                self.symbol_table.var_count(SymbolKind.FIELD)
            )
            self.vmw.write_call('Memory.alloc', 1)
            self.vmw.write_pop(SegmentType.POINTER, 0)
        elif subroutine_type == Tokens.METHOD:
            self.vmw.write_push(SegmentType.ARG, 0)
            self.vmw.write_pop(SegmentType.POINTER, 0)
        elif subroutine_type == Tokens.FUNCTION:
            pass
        else:
            self.raise_syntax_error('Invalid subroutine type.')

        # statements
        self.compile_statements()
        # }
        self.compile_keyword([Tokens.RIGHT_CURLY_BRACKET])

        self.write_element_end('subroutineBody')

    def compile_var_dec(self):
        self.write_element_start('varDec')

        local_var_counts = 0

        self.kind = SymbolKind.VAR
        # var
        self.compile_keyword([Tokens.VAR])
        # type
        self.compile_type()
        self.var_type = self.tokenizer.current_token
        # varName
        self.compile_var_name(define=True, var_type=self.var_type, kind=self.kind)
        local_var_counts += 1
        # (',' varName)*
        while self.tokenizer.next_is([Tokens.COMMA]):
            self.compile_symbol([Tokens.COMMA])
            self.compile_var_name(define=True, var_type=self.var_type, kind=self.kind)
            local_var_counts += 1
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        self.write_element_end('varDec')

        return local_var_counts

    def compile_term(self):
        self.write_element_start('term')

        if isinstance(self.tokenizer.see_next(), IntegerToken):
            self.compile_integer_constant()
            self.vmw.write_push(SegmentType.CONST, self.tokenizer.current_token)
        elif isinstance(self.tokenizer.see_next(), StringToken):
            self.compile_string_constant()
        elif isinstance(self.tokenizer.see_next(), KeywordToken):
            if self.tokenizer.see_next() == Tokens.TRUE:
                self.vmw.write_push(SegmentType.CONST, 1)
                self.vmw.write_arithmetic(ArithmeticType.NEG)
            elif self.tokenizer.see_next() in [Tokens.FALSE, Tokens.NULL]:
                self.vmw.write_push(SegmentType.CONST, 0)
            elif self.tokenizer.see_next() == Tokens.THIS:
                self.vmw.write_push(SegmentType.POINTER, 0)
            self.compile_keyword(self.keyword_constant_tokens)
        elif isinstance(self.tokenizer.see_next(), IdentifierToken):
            # varName[expression]
            if self.tokenizer.next_is([Tokens.LEFT_SQUARE_BRACKET], index=1):
                # varName
                self.compile_var_name(is_other=True)

                # VM
                var_name = self.tokenizer.current_token.token
                kind = self.symbol_table.kind_of(var_name)
                index = self.symbol_table.index_of(var_name)
                segment_type = self.get_segment_type(kind)
                self.vmw.write_push(segment_type, index)

                # [
                self.compile_symbol([Tokens.LEFT_SQUARE_BRACKET])
                # expression
                self.compile_expression()
                # ]
                self.compile_symbol([Tokens.RIGHT_SQUARE_BRACKET])

                # VM a[i] のケースのみを考慮
                self.vmw.write_arithmetic(ArithmeticType.ADD)
                self.vmw.write_pop(SegmentType.POINTER, 1)
                self.vmw.write_push(SegmentType.THAT, 0)

            # subroutineCall
            elif self.tokenizer.next_is([Tokens.LEFT_ROUND_BRACKET, Tokens.DOT], index=1):
                self.compile_subroutine_call()
            # varName
            else:
                self.compile_var_name()
        # ( expression )
        elif self.tokenizer.next_is([Tokens.LEFT_ROUND_BRACKET]):
            # (
            self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
            # expression
            self.compile_expression()
            # )
            self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])
        # unaryOp -
        elif self.tokenizer.see_next() == Tokens.MINUS:
            # unaryOp
            self.compile_symbol([Tokens.MINUS])
            # term
            self.compile_term()
            # VM
            self.vmw.write_arithmetic(ArithmeticType.NEG)
        # unaryOp ~
        elif self.tokenizer.see_next() == Tokens.TILDE:
            # unaryOp
            self.compile_symbol([Tokens.TILDE])
            # term
            self.compile_term()
            # VM
            self.vmw.write_arithmetic(ArithmeticType.NOT)
        else:
            self.raise_syntax_error(self.tokenizer.see_next())


        self.write_element_end('term')

    def compile_expression(self):
        self.write_element_start('expression')

        self.compile_term()
        # (op term)*
        while self.tokenizer.next_is(self.op_tokens):
            self.compile_op()
            op_token = self.tokenizer.current_token
            self.compile_term()
            if op_token == Tokens.PLUS:
                self.vmw.write_arithmetic(ArithmeticType.ADD)
            elif op_token == Tokens.MINUS:
                self.vmw.write_arithmetic(ArithmeticType.SUB)
            elif op_token == Tokens.MULTI:
                self.vmw.write_call('Math.multiply', 2)
            elif op_token == Tokens.DIV:
                self.vmw.write_call('Math.divide', 2)
            elif op_token == Tokens.GREATER_THAN:
                self.vmw.write_arithmetic(ArithmeticType.GT)
            elif op_token == Tokens.LESS_THAN:
                self.vmw.write_arithmetic(ArithmeticType.LT)
            elif op_token == Tokens.AND:
                self.vmw.write_arithmetic(ArithmeticType.AND)
            elif op_token == Tokens.OR:
                self.vmw.write_arithmetic(ArithmeticType.OR)
            elif op_token == Tokens.TILDE:
                self.vmw.write_arithmetic(ArithmeticType.NOT)
            elif op_token == Tokens.EQUAL:
                self.vmw.write_arithmetic(ArithmeticType.EQ)
            else:
                self.raise_syntax_error('Invalid op token.')

        self.write_element_end('expression')

    def compile_expression_list(self):
        self.write_element_start('expressionList')

        # VM
        argument_counts = 0

        # (expression (',' expression)* )?
        if not self.tokenizer.next_is([Tokens.RIGHT_ROUND_BRACKET]):
            # expression
            self.compile_expression()
            argument_counts += 1
            # (',' expression)*
            while self.tokenizer.next_is([Tokens.COMMA]):
                self.compile_symbol([Tokens.COMMA])
                self.compile_expression()
                argument_counts += 1

        self.write_element_end('expressionList')

        return argument_counts

    def compile_subroutine_call(self):
        # ( のケース
        if self.tokenizer.next_is([Tokens.LEFT_ROUND_BRACKET], index=1):
            # subroutinename
            self.compile_subroutine_name()

            # VM
            subroutine_name = self.tokenizer.current_token.token
            self.vmw.write_push(SegmentType.POINTER, 0)

            # (
            self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
            # expressionList
            argument_counts = self.compile_expression_list()
            argument_counts += 1
            # )
            self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])

            function_name = '{}.{}'.format(self.class_name, subroutine_name)
            self.vmw.write_call(function_name, argument_counts)
        # . のケース
        elif self.tokenizer.next_is([Tokens.DOT], index=1):
            # className | varName
            self.compile_class_name()
            # varName (クラスのインスタンスのメソッドを使用するケース)
            if self.symbol_table.kind_of(self.tokenizer.current_token.token) is not None:
                # VM
                instance_name = self.tokenizer.current_token.token

                # .
                self.compile_symbol([Tokens.DOT])
                # subroutineName
                self.compile_subroutine_name()

                # VM
                subroutine_name = self.tokenizer.current_token.token
                kind = self.symbol_table.kind_of(instance_name)
                index = self.symbol_table.index_of(instance_name)
                segment_type = self.get_segment_type(kind)
                self.vmw.write_push(segment_type, index)

                # (
                self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
                # expressionList
                argument_counts = self.compile_expression_list()
                argument_counts += 1
                # )
                self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])

                # VM
                function_name = '{}.{}'.format(
                    self.symbol_table.type_of(instance_name),
                    subroutine_name,
                )
                self.vmw.write_call(function_name, argument_counts)
            # className (例えば Output.printInt 関数を使用するケース)
            else:
                # VM
                class_name = self.tokenizer.current_token
                # .
                self.compile_symbol([Tokens.DOT])
                # subroutineName
                self.compile_subroutine_name()
                # VM
                subroutine_name = self.tokenizer.current_token
                # (
                self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
                # expressionList
                argument_counts = self.compile_expression_list()
                # )
                self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])

                # VM
                function_name = '{}.{}'.format(
                    class_name,
                    subroutine_name,
                )
                self.vmw.write_call(function_name, argument_counts)
        else:
            self.raise_syntax_error(self.tokenizer.see_next(index=1))

    def compile_let_statement(self):
        self.write_element_start('letStatement')

        # let
        self.compile_keyword([Tokens.LET])
        # varName
        self.compile_var_name(is_other=True)

        # VM
        let_var_name = self.tokenizer.current_token.token
        kind = self.symbol_table.kind_of(let_var_name)
        index = self.symbol_table.index_of(let_var_name)
        segment_type = self.get_segment_type(kind)

        # ('[' expression ']')?
        if self.tokenizer.next_is([Tokens.LEFT_SQUARE_BRACKET]):
            # [
            self.compile_symbol([Tokens.LEFT_SQUARE_BRACKET])
            # expression
            self.compile_expression()
            # ]
            self.compile_symbol([Tokens.RIGHT_SQUARE_BRACKET])

            # VM a[i] のケースのみを考慮
            self.vmw.write_push(segment_type, index)
            self.vmw.write_arithmetic(ArithmeticType.ADD)
            self.vmw.write_pop(SegmentType.TEMP, 1)

            # =
            self.compile_symbol([Tokens.EQUAL])
            # expression
            self.compile_expression()

            # VM
            self.vmw.write_push(SegmentType.TEMP, 1)
            self.vmw.write_pop(SegmentType.POINTER, 1)
            self.vmw.write_pop(SegmentType.THAT, 0)

            # ;
            self.compile_symbol([Tokens.SEMICOLON])
        else:
            # =
            self.compile_symbol([Tokens.EQUAL])
            # expression
            self.compile_expression()
            # ;
            self.compile_symbol([Tokens.SEMICOLON])

            # VM
            self.vmw.write_pop(segment_type, index)

        self.write_element_end('letStatement')

    def compile_if_statement(self):
        self.write_element_start('ifStatement')

        label_first = self.get_label()
        label_last = self.get_label()

        # if
        self.compile_keyword([Tokens.IF])
        # (
        self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
        # expression
        self.compile_expression()
        # )
        self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])

        # VM
        self.vmw.write_arithmetic(ArithmeticType.NOT)
        self.vmw.write_if(label_first)

        # {
        self.compile_symbol([Tokens.LEFT_CURLY_BRACKET])
        # statements
        self.compile_statements()
        # }
        self.compile_symbol([Tokens.RIGHT_CURLY_BRACKET])

        # VM
        self.vmw.write_goto(label_last)
        self.vmw.write_label(label_first)

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

        # VM
        self.vmw.write_label(label_last)

        self.write_element_end('ifStatement')

    def compile_while_statement(self):
        self.write_element_start('whileStatement')

        label_first = self.get_label()
        label_last = self.get_label()

        self.vmw.write_label(label_first)

        # while
        self.compile_keyword([Tokens.WHILE])
        # (
        self.compile_symbol([Tokens.LEFT_ROUND_BRACKET])
        # expression
        self.compile_expression()
        # )
        self.compile_symbol([Tokens.RIGHT_ROUND_BRACKET])

        # VM
        self.vmw.write_arithmetic(ArithmeticType.NOT)
        self.vmw.write_if(label_last)

        # {
        self.compile_symbol([Tokens.LEFT_CURLY_BRACKET])
        # statements
        self.compile_statements()
        # }
        self.compile_symbol([Tokens.RIGHT_CURLY_BRACKET])

        self.vmw.write_goto(label_first)
        self.vmw.write_label(label_last)

        self.write_element_end('whileStatement')

    def compile_do_statement(self):
        self.write_element_start('doStatement')

        # do
        self.compile_keyword([Tokens.DO])
        # subroutineCall
        self.compile_subroutine_call()
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        # VM
        self.vmw.write_pop(SegmentType.TEMP, 0)

        self.write_element_end('doStatement')

    def compile_return_statement(self):
        self.write_element_start('returnStatement')

        # return
        self.compile_keyword([Tokens.RETURN])
        # expression?
        if not self.tokenizer.next_is([Tokens.SEMICOLON]):
            self.compile_expression()
        else:
            self.vmw.write_push(SegmentType.CONST, 0)
        # ;
        self.compile_symbol([Tokens.SEMICOLON])

        # VM
        self.vmw.write_return()

        self.write_element_end('returnStatement')

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
        or isinstance(self.tokenizer.see_next(), StringToken) \
        or isinstance(self.tokenizer.see_next(), IdentifierToken):

            self.kind = SymbolKind.ARG
            # type
            self.compile_type()
            self.var_type = self.tokenizer.current_token
            # varName
            self.compile_var_name(define=True, var_type=self.var_type, kind=self.kind)
            # (, type varName)*
            while self.tokenizer.next_is([Tokens.COMMA]):
                self.compile_symbol([Tokens.COMMA])
                self.compile_type()
                self.var_type = self.tokenizer.current_token
                self.compile_var_name(define=True, var_type=self.var_type, kind=self.kind)

        self.write_element_end('parameterList')

    def compile_op(self):
        self.compile_symbol(self.op_tokens)

    def compile_type(self):
        self.tokenizer.advance()
        if self.tokenizer.current_token in [Tokens.INT, Tokens.CHAR, Tokens.BOOLEAN] \
        or isinstance(self.tokenizer.current_token, IdentifierToken):
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_class_name(self):
        self.compile_identifier()
        self.subroutine_class_name = self.tokenizer.current_token

    def compile_subroutine_name(self):
        self.compile_identifier()
        self.subroutine_name = self.tokenizer.current_token

    def compile_var_name(self, define=False, var_type=None, kind=None, is_other=False):
        if define:
            self.symbol_table.define(self.tokenizer.see_next().token, var_type, kind)
        elif is_other:
            pass
        else:
            # VM
            kind = self.symbol_table.kind_of(self.tokenizer.see_next().token)
            index = self.symbol_table.index_of(self.tokenizer.see_next().token)
            segment_type = self.get_segment_type(kind)
            self.vmw.write_push(segment_type, index)

        self.compile_identifier()

    def compile_keyword(self, keyword_tokens):
        self.tokenizer.advance()
        if self.tokenizer.current_token in keyword_tokens:
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

    def compile_symbol(self, keyword_tokens):
        self.tokenizer.advance()
        if self.tokenizer.current_token in keyword_tokens:
            self.write_element(self.tokenizer.current_token)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

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
            # VM
            string = str(self.tokenizer.current_token)
            length = len(string)
            self.vmw.write_push(SegmentType.CONST, length)
            self.vmw.write_call('String.new', 1)
            for s in string:
                self.vmw.write_push(SegmentType.CONST, ord(s))
                self.vmw.write_call('String.appendChar', 2)
        else:
            self.raise_syntax_error(self.tokenizer.current_token)

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

    def get_kind(self, token):
        if token == Tokens.STATIC:
            return SymbolKind.STATIC
        elif token == Tokens.FIELD:
            return SymbolKind.FIELD
        else:
            return ValueError('Invalid token in get_kind.')

    def get_segment_type(self, kind):
        if kind == SymbolKind.STATIC:
            return SegmentType.STATIC
        elif kind == SymbolKind.FIELD:
            return SegmentType.THIS
        elif kind == SymbolKind.ARG:
            return SegmentType.ARG
        elif kind == SymbolKind.VAR:
            return SegmentType.LOCAL
        else:
            self.raise_syntax_error('Invalid kind and index error.')

    def get_label(self):
        self.label_number += 1
        return 'LABEL_{}'.format(self.label_number)
