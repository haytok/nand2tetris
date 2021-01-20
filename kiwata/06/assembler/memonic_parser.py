from code import get_dest_binary, get_comp_binary, get_jump_binary


class SymbolTable:
    def __init__(self):
        self.A_COMMAND = 0
        self.C_COMMAND = 1
        self.L_COMMAND = 2
        self.DEFINED_SYMBOL_TABLE = {
            'R0': format(0, '016b'),
            'R1': format(1, '016b'),
            'R2': format(2, '016b'),
        }
        self.SYMBOL_TABLE = {}
        self.command = {
            self.A_COMMAND : self.get_address_of_a_command,
            self.C_COMMAND : self.get_address_of_c_command,
            self.L_COMMAND : self.get_address_of_l_command,
        }


    def is_defined_symbol_table(self, input_value):
        return input_value in self.DEFINED_SYMBOL_TABLE


    def is_symbol_table(self, input_value):
        return input_value in self.SYMBOL_TABLE


    def add_symbol_table(self, memonic, address):
        self.SYMBOL_TABLE[memonic] = address


    def get_symbol_table(self):
        return self.SYMBOL_TABLE


    def get_advance(self, input_text):
        command_type = self.get_command_type(input_text)
        command = self.get_command(command_type, input_text)
        return command


    def get_command_type(self, input_text):
        if input_text[0] == '@':
            return self.A_COMMAND
        elif input_text[0] == '(' and input_text[-1] == ')':
            return self.L_COMMAND
        else:
            return self.C_COMMAND


    def get_command(self, command_type, input_text):
        return self.command[command_type](input_text)


    def get_address_of_a_command(self, input_text):
        input_value = input_text[1:]
        try:
            input_value = int(input_value)
            value = format(input_value, '016b')
            return value
        except:
            # @i のケース
            if self.is_defined_symbol_table(input_value):
                return self.DEFINED_SYMBOL_TABLE[input_value]
            elif self.is_symbol_table(input_value):
                return self.SYMBOL_TABLE[input_value]
            else:
                raise ValueError('Input in get_address_of_a_command is invalid.')


    def get_address_of_c_command(self, input_text):
        command = '111'
        if '=' in input_text:
            dest_memonic, comp_memonic = input_text.split('=')
            comp_binary = get_comp_binary(comp_memonic)
            dest_binary = get_dest_binary(dest_memonic)
            command += comp_binary + dest_binary + '000'
            return command
        elif ';' in input_text:
            comp_memonic, jump_memonic = input_text.split(';')
            comp_binary = get_comp_binary(comp_memonic)
            jump_binary = get_jump_binary(jump_memonic)
            command += comp_binary + '000' + jump_binary
            return command
        else:
            raise ValueError('Input is invalid.')


    def get_address_of_l_command(self, input_text):
        value = format(100, '016b')
        return 'l'


    def get_dest_command(self, input_text):
        return 'get_dest_command'


    def get_comp_command(self, input_text):
        return 'get_comp_command'


    def get_jump_command(self, input_text):
        return 'get_jump_command'
