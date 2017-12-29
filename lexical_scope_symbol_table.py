#!/usr/bin/python
# coding: utf8


class EntrySymbolTable:

    level_scope = 0
    offset_scope = 0
    upperScopeOffset = 0
    symbols = dict()

    def __init__(self, level, offset, upper_scope_offset, default_symbols):
        self.level_scope = level
        self.offset_scope = offset
        self.upperScopeOffset = upper_scope_offset
        self.symbols = default_symbols
        print "__init_EntrySymbolTable__: address_table=%s" % (str(hex(id(self.symbols))))

    def get_all_scope(self):
        return self.level_scope

    def get_level_scope(self, level):
        return self.level_scope[level]

    def get_offset_scope(self):
        return self.offset_scope

    def get_upper_offset(self):
        return self.upperScopeOffset

    def get_symbol_table(self):
        return self.symbols

    def set_upper_scope_offset(self, offset):
        self.upperScopeOffset = offset

    def set_offset_scope(self, offset):
        self.offset_scope = offset

    def set_symbol_table(self, symbol_table):
        self.symbols = symbol_table


class LexicalScopeSymbolTable:

    level_scope = list(list())
    current_level = 0

    def __init__(self):
        self.initialize_scope()

    def debug_level(self):
        print "DEBUG_LEVEL: Number of level => " + str(self.get_size_level())
        for scope_collection in self.level_scope:
            print "Debug_level: " + str(len(scope_collection))

    def dump_level(self, level):
        collection_scope = self.level_scope[level]
        print "#" * 35 + "Dump_Level" + "#" * 35
        for scope_offset in collection_scope:
            symbol_table = scope_offset.get_symbol_table()
            i = scope_offset.get_offset_scope()
            for k, v in symbol_table.iteritems():
                print "Scope(%s:%s) -> id: %s, value=%s, addr=%s, addr_table=%s"\
                    % (str(level), str(i), str(k)
                       , str(v.n), str(v), str(hex(id(symbol_table))))

    def add_new_scope(self):
        # upper_offset = self.get_offset_last_dominant()
        self.level_scope.append([EntrySymbolTable(self.current_level, -1, -1, dict())])
        addr_table = hex(id(self.level_scope[self.current_level][-1].get_symbol_table()))
        print "Add_new_scope: %s:%s - addr_table=%s" % ("x", "x", addr_table)

    def add_new_offset(self, index_level):
        # offset = len(self.level_scope[index_level])
        self.level_scope[index_level].append(EntrySymbolTable(index_level, -1, -1, dict()))
        addr_table = hex(id(self.level_scope[self.current_level][-1].get_symbol_table()))
        print "Add_new_offset: %s:%s - addr_table=%s" % ("x", "x", addr_table)

    def set_offset_new_scope(self):
        # offset = -1
        upper_offset = self.get_offset_last_dominant()
        if self.get_offset_current_level() == -1:
            offset = self.get_size_offset(self.get_current_level()) - 1
        else:
            offset = self.level_scope[self.get_current_level()][-1].get_offset_scope() + 1
        self.level_scope[self.get_current_level()][-1].set_offset_scope(offset)
        self.level_scope[self.get_current_level()][-1].set_upper_scope_offset(upper_offset)

    def initialize_scope(self):
        index_level = self.get_current_level()
        if index_level >= self.get_size_level():
            self.add_new_scope()
        else:
            self.add_new_offset(index_level)
        # upper_offset = self.get_offset_last_dominant()
        current_offset = self.get_offset_current_level()
        self.set_offset_new_scope()
        self.print_scope_initialization(current_offset)
        self.current_level += 1

    def bind_symbol(self, symbol, value, index_level, offset):
        symbol_table = self.get_symbol_table(index_level, offset)
        symbol_table[symbol] = value
        print "Bind_scope: %s:%s - addr_table=%s" \
            % (str(index_level), offset, str(hex(id(symbol_table))))

    def lookup_symbol(self, symbol):
        index_level = self.get_current_level() - 1
        if index_level < 0:
            print "ERROR(lexicalScopeSymbolTable.lookup_symbol): index level must be positive"
            return None
        offset = self.get_offset_by_level(index_level)
        symbol_table = self.get_symbol_table(index_level, offset)
        if symbol in symbol_table.keys():
            value = symbol_table[symbol]
            return value
        print "Lookup_symbol: Not found - " + str(symbol)
        return self.lookup_dominant_scope(symbol, index_level, offset)

    def lookup_dominant_scope(self, symbol, index_level, offset):
        dominant_level = index_level - 1
        upper_offset = self.level_scope[index_level][offset].get_upper_offset()
        if self.level_scope[dominant_level][upper_offset]:
            symbol_table = self.get_symbol_table(dominant_level, upper_offset)
            if symbol in symbol_table.keys():
                print "Lookup_dominant_scope: found %s=%s" \
                    % (symbol, symbol_table[symbol])
                return symbol_table[symbol]
        print "Lookup_dominant_scope: Not found - %s; upper_level=%s, upper_offset=%s" \
            % (str(symbol), dominant_level, upper_offset)
        return None

    def finalize_scope(self):
        self.current_level -= 1
        print "===== -> Finalize Scope %s =====" % (str(self.current_level))

    def get_offset_last_dominant(self):
        if self.get_current_level() == 0:
            return 0
        return self.level_scope[self.get_current_level() - 1][-1].get_offset_scope()

    def get_offset_level(self, index_level):
        return len(self.level_scope[index_level])

    def get_offset_current_level(self):
        return self.level_scope[self.current_level][-1].get_offset_scope()

    def get_offset_by_level(self, index_level):
        return self.level_scope[index_level][-1].get_offset_scope()

    def get_size_offset(self, index_level):
        return len(self.level_scope[index_level])

    def get_last_offset(self, index_level):
        return self.level_scope[index_level][-1].get_offset_scope()

    def create_new_offset(self):
        return len(self.level_scope[self.get_current_level()])

    def get_size_level(self):
        return len(self.level_scope)

    def get_scope(self, offset):
        return self.level_scope[self.get_current_level()][offset]

    def get_current_level(self):
        return self.current_level

    def get_symbol_table(self, index_level, offset):
        symbol_table = self.level_scope[index_level][offset].get_symbol_table()
        print "Get_symbol_table(Scope %s:%s)" % (str(index_level), offset)
        return symbol_table

    def print_scope_initialization(self, offset):
        print "===== -> Initialize Scope %s:%s - %s ====="\
            % (str(self.current_level)
               , self.get_scope(offset).get_offset_scope()
               , self.get_scope(offset).get_upper_offset())
