'''
一つの .vm ファイルに対してパースを行う
入力コードへのアクセスをカプセル化する
さらに、空白文字とコメントを取り除く
'''

class Parser:
    def __init__(self, input_file_name):
        self.C_ARITHMETIC = 0
        self.C_PUSH = 1
        self.C_POP = 2
        self.C_LABEL = 3
        self.C_GOTO = 4
        self.C_IF = 5
        self.C_FUNCTION = 6
        self.C_RETURN = 7
        self.C_CALL = 8
        self.SEGMENT_CONSTANT = 9
        self.command = {
            self.C_ARITHMETIC: self.get_assembly_of_arithmetic,
            self.C_PUSH: self.get_assembly_of_push,
            self.C_POP: self.get_assembly_of_pop,
            self.C_LABEL: self.get_assembly_of_flow,
            self.C_IF: self.get_assembly_of_flow,
            self.C_GOTO: self.get_assembly_of_flow,
            self.C_FUNCTION: self.get_assembly_of_function,
            self.C_CALL: self.get_assembly_of_call,
            self.C_RETURN: self.get_assembly_of_return,
        }
        self.ARITHMETIC_COUNTER = 0
        self.FILE_NAME = input_file_name.split('.')[0]


    def get_advance(self, input_text, count):
        splited_input_text = input_text.split()
        command_type = self.get_command_type(splited_input_text)
        command = self.get_command(command_type, splited_input_text, count)
        print(command)
        print('-' * 20)
        return command


    def get_command_type(self, splited_input_text):
        command_length = len(splited_input_text)
        if command_length == 1:
            if splited_input_text[0] == 'return':
                return self.C_RETURN
            else:
                return self.C_ARITHMETIC
        elif command_length == 2:
            if splited_input_text[0] == 'label':
                return self.C_LABEL
            elif splited_input_text[0] == 'if-goto':
                return self.C_IF
            elif splited_input_text[0] == 'goto':
                return self.C_GOTO
            else:
                raise ValueError('Invalid input text.')
        elif command_length == 3:
            if splited_input_text[0] == 'push':
                return self.C_PUSH
            elif splited_input_text[0] == 'pop':
                return self.C_POP
            elif splited_input_text[0] == 'function':
                return self.C_FUNCTION
            elif splited_input_text[0] == 'call':
                return self.C_CALL
            else:
                raise ValueError('Invalid input text.')
        else:
            raise ValueError('Invalid input text.')


    def get_command(self, command_type, splited_input_text, count):
        return self.command[command_type](splited_input_text, count)


    def get_assembly_of_arithmetic(self, splited_input_text, count):
        arithmetic_command = splited_input_text[0]
        # 算術演算
        if arithmetic_command == 'add':
            return self.get_assembly_of_add(arithmetic_command)
        elif arithmetic_command == 'sub':
            return self.get_assembly_of_sub(arithmetic_command)
        elif arithmetic_command == 'neg':
            return self.get_assembly_of_neg(arithmetic_command)
        elif arithmetic_command == 'eq':
            return self.get_assembly_of_eq(arithmetic_command)
        elif arithmetic_command == 'lt':
            return self.get_assembly_of_lt(arithmetic_command)
        elif arithmetic_command == 'gt':
            return self.get_assembly_of_gt(arithmetic_command)
        # 論理演算
        elif arithmetic_command == 'and':
            return self.get_assembly_of_and(arithmetic_command)
        elif arithmetic_command == 'or':
            return self.get_assembly_of_or(arithmetic_command)
        elif arithmetic_command == 'not':
            return self.get_assembly_of_not(arithmetic_command)
        else:
            raise ValueError('Invalid input text.')


    def get_assembly_of_add(self, arithmetic_command):
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D+M',
            'M=D',
            '@SP',
            'M=M+1',
            ]
        return assembly


    def get_assembly_of_eq(self, arithmetic_command):
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D-M',
            # 条件分岐
            '@EQ{}'.format(self.ARITHMETIC_COUNTER), # when !=
            'D;JEQ',
            '@0',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@NEXT{}'.format(self.ARITHMETIC_COUNTER), # 次のセクションへ飛ぶ
            '0;JMP',
            '(EQ{})'.format(self.ARITHMETIC_COUNTER), # when =
            '@0',
            'D=A',
            'D=D-1',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '(NEXT{})'.format(self.ARITHMETIC_COUNTER),
        ]
        self.ARITHMETIC_COUNTER += 1
        return assembly


    def get_assembly_of_lt(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D-M',
            # 条件分岐
            '@EQ{}'.format(self.ARITHMETIC_COUNTER), # when !=
            'D;JGT',
            '@0',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@NEXT{}'.format(self.ARITHMETIC_COUNTER), # 次のセクションへ飛ぶ
            '0;JMP',
            '(EQ{})'.format(self.ARITHMETIC_COUNTER), # when true
            '@0',
            'D=A',
            'D=D-1',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '(NEXT{})'.format(self.ARITHMETIC_COUNTER),
        ]
        return assembly


    def get_assembly_of_gt(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D-M',
            # 条件分岐
            '@EQ{}'.format(self.ARITHMETIC_COUNTER), # when !=
            'D;JLT',
            '@0',
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@NEXT{}'.format(self.ARITHMETIC_COUNTER), # 次のセクションへ飛ぶ
            '0;JMP',
            '(EQ{})'.format(self.ARITHMETIC_COUNTER), # when true
            '@0',
            'D=A',
            'D=D-1',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '(NEXT{})'.format(self.ARITHMETIC_COUNTER),
        ]
        return assembly


    def get_assembly_of_sub(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M-D',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    def get_assembly_of_neg(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            'D=-D',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    def get_assembly_of_and(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D&M',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    def get_assembly_of_or(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@SP',
            'M=M-1',
            'A=M',
            'D=D|M',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    def get_assembly_of_not(self, arithmetic_command):
        self.ARITHMETIC_COUNTER += 1
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            'D=!D',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    # push コマンド
    def get_assembly_of_push(self, splited_input_text, count):
        segment, value = splited_input_text[1], splited_input_text[2]
        if segment == 'constant':
            return self.get_assembly_of_push_constant(value)
        elif segment == 'local':
            return self.get_assembly_of_push_local(value)
        elif segment == 'that':
            return self.get_assembly_of_push_that(value)
        elif segment == 'argument':
            return self.get_assembly_of_push_argument(value)
        elif segment == 'this':
            return self.get_assembly_of_push_this(value)
        elif segment == 'temp':
            return self.get_assembly_of_push_temp(value)
        elif segment == 'pointer':
            return self.get_assembly_of_push_pointer(value)
        elif segment == 'static':
            return self.get_assembly_of_push_static(value)
        else:
            raise ValueError('Invalid input text.')


    # push constant value
    def get_assembly_of_push_constant(self, value):
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    def get_assembly_of_push_local(self, value):
        SYMBOL_NAME = 'LCL'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly

    def get_assembly_of_push_that(self, value):
        SYMBOL_NAME = 'THAT'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_push_argument(self, value):
        SYMBOL_NAME = 'ARG'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_push_this(self, value):
        SYMBOL_NAME = 'THIS'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_push_temp(self, value):
        SYMBOL_NAME = '5'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_push_pointer(self, value):
        SYMBOL_NAME = 'THIS' if value == '0' else 'THAT'
        assembly = [
            '@{}'.format(SYMBOL_NAME),
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    def get_assembly_of_push_static(self, value):
        assembly = [
            '@{}.{}'.format(self.FILE_NAME, value),
            # '@{}'.format(16 + int(value)),
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ]
        return assembly


    # pop コマンド
    def get_assembly_of_pop(self, splited_input_text, count):
        segment, value = splited_input_text[1], splited_input_text[2]
        if segment == 'local':
            return self.get_assembly_of_pop_local(value)
        elif segment == 'argument':
            return self.get_assembly_of_pop_argument(value)
        elif segment == 'this':
            return self.get_assembly_of_pop_this(value)
        elif segment == 'that':
            return self.get_assembly_of_pop_that(value)
        elif segment == 'temp':
            return self.get_assembly_of_pop_temp(value)
        elif segment == 'pointer':
            return self.get_assembly_of_pop_pointer(value)
        elif segment == 'static':
            return self.get_assembly_of_pop_static(value)
        else:
            raise ValueError('Invalid input text.')        


    def get_assembly_of_pop_local(self, value):
        SYMBOL_NAME = 'LCL'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'M=D',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_pop_argument(self, value):
        SYMBOL_NAME = 'ARG'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'M=D',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_pop_this(self, value):
        SYMBOL_NAME = 'THIS'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'M=D',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly

    def get_assembly_of_pop_that(self, value):
        SYMBOL_NAME = 'THAT'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'M=D',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_pop_temp(self, value):
        SYMBOL_NAME = '5'
        assembly = [
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M+D',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(SYMBOL_NAME),
            'A=M',
            'M=D',
            '@{}'.format(value),
            'D=A',
            '@{}'.format(SYMBOL_NAME),
            'M=M-D',
        ]
        return assembly


    def get_assembly_of_pop_pointer(self, value):
        SYMBOL_NAME = 'THIS' if value == '0' else 'THAT'
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(SYMBOL_NAME),
            'M=D',
        ]
        return assembly


    def get_assembly_of_pop_static(self, value):
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}.{}'.format(self.FILE_NAME, value),
            # '@{}'.format(16 + int(value)),
            'M=D',
        ]
        return assembly


    def get_assembly_of_flow(self, splited_input_text, count):
        segment, label = splited_input_text[0], splited_input_text[1]
        print(segment, label)
        if segment == 'label':
            return self.create_assembly_of_label(label)
        elif segment == 'if-goto':
            return self.create_assembly_of_if(label)
        elif segment == 'goto':
            return self.create_assembly_of_goto(label)
        else:
            raise ValueError('Invalid input text.')


    def create_assembly_of_label(self, value):
        assembly = [
            '({})'.format(value)
        ]
        return assembly


    def create_assembly_of_if(self, value):
        assembly = [
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@{}'.format(value),
            'D;JNE',
        ]
        return assembly


    def create_assembly_of_goto(self, value):
        assembly = [
            '@{}'.format(value),
            '0;JMP',
        ]
        return assembly


    def get_assembly_of_function(self, splited_input_text, count):
        function_name, value = splited_input_text[1], splited_input_text[2]
        print(function_name, value)
        assembly = [
            '({})'.format(function_name),
        ]
        for _ in range(int(value)):
            assembly += [
                '@SP',
                'A=M',
                'M=0',
                '@SP',
                'M=M+1',
            ]
        return assembly


    def get_assembly_of_call(self, splited_input_text, count):
        function_name, n = splited_input_text[1], splited_input_text[2]
        label = '_CALL_{}'.format(function_name)
        return_address = label + str(int(count) + 1)
        assembly = [
            # push return-address
            '@{}'.format(return_address),
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push LCL
            '@LCL',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push ARG
            '@ARG',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THIS
            '@THIS',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THAT
            '@THAT',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # ARG = SP - n - 5
            '@SP',
            'D=M',
            '@5',
            'D=D-A',
            '@{}'.format(n),
            'D=D-A',
            '@ARG',
            'M=D',
            # LCL = SP
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            # goto f
            '@{}'.format(function_name),
            '0;JMP',
            # (return-address)
            '({})'.format(return_address),
        ]
        return assembly


    def get_assembly_of_return(self, splited_input_text, count):
        assembly = [
            # FRAME = LCL
            '@LCL',
            'D=M',
            '@R13',
            'M=D',
            # RET = *(FRAME - 5)
            '@5',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@R14',
            'M=D',
            #
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',
            '@ARG',
            'A=M',
            'M=D',
            # SP = ARG + 1
            '@ARG',
            'D=M+1',
            '@SP',
            'M=D',
            # THAT = *(FRAME - 1)
            '@R13',
            'A=M-1',
            'D=M',
            '@THAT',
            'M=D',
            # THIS = *(FRAME - 2)
            '@2',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@THIS',
            'M=D',
            # ARG = *(FRAME - 3)
            '@3',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@ARG',
            'M=D',
            # LCL = *(FRAME - 4)
            '@4',
            'D=A',
            '@R13',
            'A=M-D',
            'D=M',
            '@LCL',
            'M=D',
            # goto RET
            '@R14',
            # このコマンドは必要
            # jump 命令では予め移動したいアドレスを A レジスタに設定しておく必要がある
            'A=M',
            '0;JMP',
        ]
        return assembly


    # ブートストラップコード
    def get_assembly_of_init(self):
        f_name = 'Sys.init'
        return_address = '_CALL_{}'.format(f_name)
        assembly = [
            # VM スタックは RAM[256] から先に対応づける
            '@256',
            'D=A',
            '@SP',
            'M=D',
            # Sys.init 関数を呼び出す
            # push return-address
            '@{}'.format(return_address),
            'D=A',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push LCL
            '@LCL',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push ARG
            '@ARG',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THIS
            '@THIS',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # push THAT
            '@THAT',
            'D=M',
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
            # ARG = SP - n - 5
            '@SP',
            'D=M',
            '@5',
            'D=D-A',
            '@0',
            'D=D-A',
            '@ARG',
            'M=D',
            # LCL = SP
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            # goto f
            '@{}'.format(f_name),
            '0;JMP',
            # (return-address)
            '({})'.format(return_address),
        ]
        return assembly