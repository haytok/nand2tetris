from jack_tokenizer import Tokenizer


class CompilationEngine:
    def __init__(self, input_texts):
        self.tokenizer = Tokenizer(input_texts)
        self.elements = []
    
    def compile(self):
        self.compile_class()

    def compile_class(self):
        print('Hello', self.tokenizer.tokens)
