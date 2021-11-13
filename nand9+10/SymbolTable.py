INDEX_IDX = 2
TYPE_IDX = 0
KIND_IDX = 1
STATIC = "static"
FIELD = "field"
ARG = "arg"
VAR = "var"


class SymbolTable:
    def __init__(self):
        self.var_dict = {}
        self.kind_count_dict = {STATIC: 0, FIELD: 0, ARG: 0, VAR: 0}

    def start_subroutine(self):
        self.var_dict = {}
        self.kind_count_dict = dict.fromkeys(self.kind_count_dict, 0)

    def define(self, name, var_type, kind):
        self.var_dict[name] = (var_type, kind, self.kind_count_dict[kind])
        self.kind_count_dict[kind] = self.kind_count_dict[kind] + 1

    def var_count(self, kind):
        return self.kind_count_dict[kind]

    def kind_of(self, name):
        return self.var_dict[name][KIND_IDX]

    def type_of(self, name):
        return self.var_dict[name][TYPE_IDX]

    def index_of(self, name):
        return self.var_dict[name][INDEX_IDX]

    def contain(self, name):
        return name in self.var_dict


