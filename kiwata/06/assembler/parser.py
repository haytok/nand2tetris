from code import get_dest_binary, get_comp_binary, get_jump_binary

A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2


def get_advance(input_text):
    command_type = get_command_type(input_text)
    command = get_command(command_type, input_text)
    return command


def get_command_type(input_text):
    if input_text[0] == '@':
        return A_COMMAND
    elif input_text[0] == '(':
        return L_COMMAND
    else:
        return C_COMMAND


def get_command(command_type, input_text):
    command = {
        A_COMMAND : get_address_of_a_command,
        C_COMMAND : get_address_of_c_command,
        L_COMMAND : get_address_of_l_command,
    }
    return command[command_type](input_text)


def get_address_of_a_command(input_text):
    input_value = input_text[1:]
    try:
        input_value = int(input_value)
        value = format(input_value, '016b')
        return value
    except:
        # @i のケース
        return 'value'


def get_address_of_c_command(input_text):
    command = '111'
    if '=' in input_text:
        dest_memonic, comp_memonic = input_text.split('=')
        comp_binary = get_comp_binary(comp_memonic)
        dest_binary = get_dest_binary(dest_memonic)
        command += comp_binary + dest_binary + '000'
        return command
    elif ';' in input_text:
        comp_memonic, jump_memonic = input_text.split('=')
        comp_binary = get_comp_binary(comp_memonic)
        jump_binary = get_jump_binary(jump_memonic)
        command += comp_binary + '000' + jump_binary
        return command
    else:
        raise ValueError('Input is invalid.')


def get_address_of_l_command(input_text):
    value = format(100, '016b')
    return 'l'


def get_dest_command(input_text):
    return 'get_dest_command'


def get_comp_command(input_text):
    return 'get_comp_command'


def get_jump_command(input_text):
    return 'get_jump_command'
