import sys

from memonic_parser import (
    SymbolTable,
)

def main():
    print(sys.argv)
    if len(sys.argv) != 2:
        raise ValueError('Invalid file name.')
    input_file_name = sys.argv[1]
    input_texts = get_file_text(input_file_name)
    # Output
    output_file_name = '{}.hack'.format(input_file_name.split('.')[0])
    commands = []
    # Text processing
    del_commet = lambda value: value[:2] != '//'
    del_new_line = lambda value: value[:2] != '\n'
    replace_new_line = lambda value: value.replace('\n', '').strip().split(' ')[0]
    input_texts = list(
        map(
            replace_new_line, filter(
                del_new_line, filter(del_commet, input_texts)
            )
        )
    )
    print('-' * 10)
    # Create Symbol Table.
    address = 0
    symbol_table = SymbolTable()
    for input_text in input_texts:
        command_type = symbol_table.get_command_type(input_text)
        if command_type == symbol_table.A_COMMAND:
            address += 1
        elif command_type == symbol_table.L_COMMAND:
            symbol_table.add_symbol_table(
                input_text[1:-1],
                format(address, '016b')
            )
        else:
            address += 1
    print(symbol_table.get_symbol_table())
    print('-' * 10)
    # Create binary.
    for input_text in input_texts:
        command_type = symbol_table.get_command_type(input_text)
        if command_type != symbol_table.L_COMMAND:
            command = symbol_table.get_advance(input_text)
            commands.append(command)
    create_hack_file(output_file_name, commands)


def get_file_text(file_path):
    with open(file_path) as f:
        return f.readlines()


def create_hack_file(file_path, commands):
    f = open(file_path, 'w')
    f.write('\n'.join(commands))
    f.close()


if __name__ == '__main__':
    main()
