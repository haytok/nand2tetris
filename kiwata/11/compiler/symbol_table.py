from const import SymbolKind

class SymbolTable:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        print(self.tokenizer)
        # スコープがクラス
        self.static_table = {}
        self.field_table = {}
        # スコープがサブルーチン
        self.argument_table = {}
        self.var_table = {}

        for token in self.tokenizer.tokens:
            print(token)

    def start_subroutine(self):
        self.argument_table = {}
        self.var_table = {}

    # name: a, type: int, kind: SymbolKind.STATIC
    def define(self, name, var_type, kind):
        class Symbol:
            def __init__(self, name, var_type, kind, index):
                self.name = name
                self.type = var_type
                self.kind = kind
                self.index = index

        symbol = Symbol(name, var_type, kind, serl.var_count(kind))
        if kind == SymbolKind.STATIC:
            self.static_table[name] = symbol
        elif kind == SymbolKind.FIELD:
            self.field_table[name] = symbol
        elif kind == SymbolKind.ARG:
            self.argument_table[name] = symbol
        elif kind == SymbolKind.VAR:
            self.var_table[name] = symbol
        else:
            raise ValueError('Invalid value in SymbolTable.define.')

    def var_count(self, kind):
        if kind == SymbolKind.STATIC:
            return len(self.static_table)
        elif kind == SymbolKind.FIELD:
            return len(self.field_table)
        elif kind == SymbolKind.ARG:
            return len(self.argument_table)
        elif kind == SymbolKind.VAR:
            return len(self.var_table)

    def kind_of(self, name):
        symbol = self._find_by_name(name)
        if symbol is not None:
            return symbol.kind
        else:
            return None

    def type_of(self, name):
        symbol = self._find_by_name(name)
        if symbol is not None:
            return symbol.type
        else:
            raise ValueError('Invalid valud in SymbolTable.type_of.')
    
    def index_of(self, name):
        symbol = self._find_by_name(name)
        if symbol is not None:
            return symbol.index
        else:
            raise ValueError('Invalid valud in SymbolTable.index_of.')

    def _find_by_name(self, name):
        if name in self.static_table:
            return self.static_table[name]
        elif name in self.field_table:
            return SymbolKind.FIELD[name]
        elif name in self.argument_table:
            return SymbolKind.ARG[name]
        elif name in self.var_table:
            return SymbolKind.VAR[name]
        else:
            return None
