from const import *


class Tokenizer:
    def __init__(self, input_texts):
        self.elements = []
        self.tokens = []
        self.current_token = None

        for input_text in input_texts:
            self.current_tokens = []
            self.input_text = input_text
            self.parse_text()
            self.create_current_tokens()

    def parse_text(self):
        while True:
            length = len(self.input_text)
            if length == 1:
                string = self.input_text
                token = self.judge_token(string)
                self.current_tokens.append(token)
                self.tokens.append(token)
                return
            for i in range(1, length):
                string = self.input_text[0:i]
                string_next = self.input_text[0:i+1]

                token = self.judge_token(string)
                next_token = self.judge_token(string_next)
                if token is not None and next_token is None:
                    self.current_tokens.append(token)
                    self.tokens.append(token)
                    # class Main のケースで空白文字が入っているので、それを除去する
                    self.input_text = self.input_text[i:].lstrip()
                    break

    def judge_token(self, string):
        if string in KEYWORD_PATTERN:
            return KEYWORD_PATTERN[string]
        elif string in SYMBOL_PATTERN:
            return SYMBOL_PATTERN[string]
        elif INTEGER_PATTERN.match(string):
            return IntegerToken(string)
        elif STRING_PATTERN.match(string):
            return StringToken(string)
        elif IDENTIFIER_PATTERN.match(string):
            return IdentifierToken(string)
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

    def create_current_tokens(self):
        for token in self.current_tokens:
            element = get_element(token.type)
            self.elements.append(
                '<{}> {} </{}>'.format(
                    element, token.token_displayed, element
                )
            )

    def advance(self):
        self.current_token = self.tokens.pop(0)

    def see_next(self, index=0):
        return self.tokens[index] if len(self.tokens) > index else None
    
    def next_is(self, tokens, index=0):
        return self.see_next(index) in tokens
