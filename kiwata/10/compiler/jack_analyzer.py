import re
import sys

from compilation_engine import CompilationEngine
from jack_tokenizer import Tokenizer


def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*|/\*\*.*|\*\s.*|\*\/.*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
    def _replacer(match):
        if match.group(2) is not None:
            return ''
        else:
            return match.group(1)
    return regex.sub(_replacer, string).strip()


def main():
    # Input
    if len(sys.argv) != 2:
        raise ValueError('Invalid file name.')
    input_file_path = sys.argv[1]
    input_texts = get_file_text(input_file_path)
    splited_input_file_path = input_file_path.split('/')
    input_file_name = splited_input_file_path[-1]
    # Output
    output_file_name = 'MyMainT.xml'
    output_file_path = '/'.join([*splited_input_file_path[:-1], output_file_name])
    # Text Processing
    del_commet = lambda value: value[:2] != '//'
    del_new_line = lambda value: value[:2] != '\n'
    del_blank_content = lambda value: value != ''
    replace_new_line = lambda value: value.replace('\n', '').strip()
    input_texts = list(
        filter(
            del_blank_content, map(
                remove_comments, filter(
                    del_new_line, filter(del_commet, input_texts)
                )
            )
        )
    )
    # elements = [['<tokens>']]
    # tokenizer = Tokenizer(input_texts)
    # elements.append(tokenizer.elements)
    # elements.append(['</tokens>'])
    # create_hack_file(output_file_path, elements)
    engine = CompilationEngine(input_texts)


def get_file_text(file_path):
    with open(file_path) as f:
        return f.readlines()


def create_hack_file(file_path, commands):
    f = open(file_path, 'w')
    for command in commands:
        f.write('\n'.join(command))
        f.write('\n')
    f.close()


if __name__ == '__main__':
    main()
