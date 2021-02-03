from const import (IDENTIFIER_PATTERN, IDENTIFIER_TYPE, INTEGER_PATTERN,
                   INTEGER_TYPE, KEYWORD_PATTERN, KEYWORD_TYPE, STRING_PATTERN,
                   STRING_TYPE, SYMBOL_PATTERN, SYMBOL_TYPE, get_element)


class Tokenizer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.elements = []

        self.parse_text()
        self.create_tokens()

    def parse_text(self):
        while True:
            length = len(self.input_text)
            if length == 1:
                string = self.input_text
                string_type = self.judge_token(string)
                self.tokens.append({'type': string_type, 'value': string})
                return
            for i in range(1, length):
                string = self.input_text[0:i]
                string_next = self.input_text[0:i+1]

                string_type = self.judge_token(string)
                string_next_type = self.judge_token(string_next)
                if string_type is not None and string_next_type is None:
                    if string_type == STRING_TYPE:
                        string = string[1:-1]
                    self.tokens.append({'type': string_type, 'value': string})
                    # class Main のケースで空白文字が入っているので、それを除去する
                    self.input_text = self.input_text[i:].lstrip()
                    break

    def judge_token(self, string):
        if string in KEYWORD_PATTERN:
            return KEYWORD_TYPE
        elif string in SYMBOL_PATTERN:
            return SYMBOL_TYPE
        elif INTEGER_PATTERN.match(string):
            return INTEGER_TYPE
        elif STRING_PATTERN.match(string):
            return STRING_TYPE
        elif IDENTIFIER_PATTERN.match(string):
            return IDENTIFIER_TYPE
        else:
            return None

    def cast_string(self, string):
        if string == '<':
            return '&lt;'
        elif string == '>':
            return '&gt;'
        elif string == '&':
            return '&amp;'
        else:
            return string

    def create_tokens(self):
        for token in self.tokens:
            element = get_element(token['type'])
            self.elements.append(
                '<{}> {} </{}>'.format(
                    element, self.cast_string(token['value']), element
                )
            )
