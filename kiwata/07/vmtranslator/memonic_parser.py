'''
一つの .vm ファイルに対してパースを行う
入力コードへのアクセスをカプセル化する
さらに、空白文字とコメントを取り除く
'''

class Parser:
    def __init__(self):
        self.C_ARITHMETIC = 0
        self.C_PUSH = 1
        self.C_POP = 2
        self.C_LABEL = 3
        self.C_GOTO = 4
        self.C_IF = 5
        self.C_FUNCTION = 6
        self.C_RETURN = 7
        self.C_CALL = 8
        self.command = {
            self.C_ARITHMETIC: self.get_assembly_of_arithmetic,
            self.C_PUSH: self.get_assembly_of_push,
        }
        self.SEGMENT_CONSTANT = 9
        self.ARITHMETIC_COUNTER = 0


    def get_advance(self, input_text):
        splited_input_text = input_text.split()
        command_type = self.get_command_type(splited_input_text)
        command = self.get_command(command_type, splited_input_text)
        print(command)
        print('-' * 20)
        return command


    def get_command_type(self, splited_input_text):
        command_length = len(splited_input_text)
        if command_length == 1:
            return self.C_ARITHMETIC
        elif command_length == 3:
            if splited_input_text[0] == 'push':
                return self.C_PUSH
            elif splited_input_text[0] == 'pop':
                return self.C_POP
            else:
                raise ValueError('Invalid input text.')
        else:
            raise ValueError('Invalid input text.')


    def get_command(self, command_type, splited_input_text):
        return self.command[command_type](splited_input_text)


    def get_assembly_of_arithmetic(self, splited_input_text):
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


    def get_assembly_of_push(self, splited_input_text):
        segment, value = splited_input_text[1], splited_input_text[2]
        if segment == 'constant':
            return self.get_assembly_of_const(value)
        else:
            raise ValueError('Invalid input text.')


    def get_assembly_of_const(self, value):
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
