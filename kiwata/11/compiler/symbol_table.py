from const import SymbolKind

class SymbolTable:
    def __init__(self):
        # スコープがクラス
        self.static_table = {}
        self.field_table = {}
        # スコープがサブルーチン
        self.argument_table = {}
        self.var_table = {}

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

            def __str__(self):
                return self.name

        symbol = Symbol(name, var_type, kind, self.var_count(kind))
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
        self.show_tables()

    def show_tables(self):
        for item in self.static_table:
            print('static_table', item, self.static_table[item].type)
        print('-' * 10)
        for item in self.field_table:
            print('field_table', item, self.field_table[item].type)
        print('-' * 10)
        for item in self.argument_table:
            print('argument_table', item, self.argument_table[item].type)
        print('-' * 10)
        for item in self.var_table:
            print('var_table', item, self.var_table[item].type)
        print('=' * 10)

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
