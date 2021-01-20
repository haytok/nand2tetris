import sys

from memonic_parser import get_advance

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
    replace_new_line = lambda value: value.replace('\n', '')
    input_texts = list(
        map(
            replace_new_line, filter(
                del_new_line, filter(del_commet, input_texts)
            )
        )
    )
    print(input_texts)
    for input_text in input_texts:
        command = get_advance(input_text)
        print(input_text, command)
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
