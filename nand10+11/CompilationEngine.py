from SymbolTable import SymbolTable
from VMWriter import VMWriter

THIS_NUM = 0

MEMORY_ALLOC = "Memory.alloc"

LABEL_NAME = "L"

STRING_APPEND_CHAR = "String.appendChar"

STRING_CONSTRUCTOR = "String.new"  

TEMP = "temp"

ARGUMENT = "argument"

THIS = "this"

NULL = "null"

FALSE = "false"

TRUE = "true"

END_STATEMENT = ";"

THAT = "that"

ADD = "+"

THAT_NUM = 1

POINTER = "pointer"

CONSTANT = "constant"

METHOD = "method"

WRITE = 'w'
NEW_LINE = "\n"
COMMA = ","

KEYWORD = 1
SYMBOL = 2
IDENTIFIER = 3
INT_CONST = 4
STRING_CONST = 5

PREFIX_DICT = {1: "<keyword>", 2: "<symbol>", 3: "<identifier>", 4: "<integerConstant>", 5: "<stringConstant>"}
SUFFIX_DICT = {1: "</keyword>", 2: "</symbol>", 3: "</identifier>", 4: "</integerConstant>", 5: "</stringConstant>"}
SUBROUTINE_SET = {"method", "constructor", "function"}
STATEMENT_SET = {"let", "if", "while", "do", "return"}
KEYWORD_CONSTANT_SET = {"true", "false", "null", "this"}
OP_SET = {"+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="}
UNARY_OP_SET = set("-~")

UNARY_OP_DICT = {"-": "- ", "~": "~"}

FIELD = "field"
STATIC = "static"
CTOR = "constructor"
METHOD = "method"
LET = "let"
IF = "if"
WHILE = "while"
DO = "do"
RETURN = "return"
VAR = "var"
ELSE = "else"

KIND_TO_SEG_DICT = {"var": "local", "static": "static", "field": "this",
                    "arg": "argument"}

NAME_SEP = "."


class CompilationEngine:
    def __init__(self, tokenizer, output_xml, output_vm):
        self.tokenizer = tokenizer
        self.class_table = SymbolTable()
        self.subroutine_table = SymbolTable()
        self.class_name = ""
        self.vmWriter = VMWriter(output_vm)
        self.label_counter = 0

    def eat(self, token):
        self.tokenizer.advance()

    def compile_class(self):
        self.tokenizer.advance()
        self.eat(self.tokenizer.key_word())  # class
        self.class_name = self.tokenizer.identifier()
        self.eat(self.tokenizer.identifier())  # class name
        self.eat(self.tokenizer.symbol())  # {
        while self.tokenizer.key_word() == FIELD or self.tokenizer.key_word() == STATIC:
            self.compile_class_var_dec()
        while self.tokenizer.key_word() in SUBROUTINE_SET:
            self.compile_subroutine()
        self.eat(self.tokenizer.symbol())  # }

    def compile_class_var_dec(self):
        kind = self.tokenizer.key_word()
        self.eat(self.tokenizer.key_word())  # field\static
        if self.tokenizer.token_type() == KEYWORD:
            var_type = self.tokenizer.key_word()
            self.eat(self.tokenizer.key_word())  # type
        elif self.tokenizer.token_type() == IDENTIFIER:
            var_type = self.tokenizer.identifier()
            self.eat(self.tokenizer.identifier())  # class name
        name = self.tokenizer.identifier()
        self.class_table.define(name, var_type, kind)
        self.eat(self.tokenizer.identifier())  # first variable name

        while self.tokenizer.symbol() == COMMA:
            self.eat(self.tokenizer.symbol())  # ,
            name = self.tokenizer.identifier()
            self.class_table.define(name, var_type, kind)
            self.eat(self.tokenizer.identifier())  # another variable name

        self.eat(self.tokenizer.symbol())  # ;

    def this_init(self, size):
        self.vmWriter.write_push(CONSTANT, size)
        self.vmWriter.write_call(MEMORY_ALLOC, 1)
        self.vmWriter.write_pop(POINTER, THIS_NUM)

    def method_init(self):
        self.vmWriter.write_push(ARGUMENT, 0)
        self.vmWriter.write_pop(POINTER, THIS_NUM)

    def compile_subroutine(self):
        self.subroutine_table.start_subroutine()
        func_key_word = self.tokenizer.key_word()
        self.eat(self.tokenizer.key_word())  # constructor\method\function
        if self.tokenizer.token_type() == KEYWORD:
            self.eat(self.tokenizer.key_word())  # void\type
        elif self.tokenizer.token_type() == IDENTIFIER:
            self.eat(self.tokenizer.identifier())  # class name
        name = self.class_name + NAME_SEP + self.tokenizer.identifier()
        self.eat(self.tokenizer.identifier())  # subroutine name
        self.eat(self.tokenizer.symbol())  # (
        self.compile_parameter_list()
        self.eat(self.tokenizer.symbol())  # )
        is_ctor = False
        is_method = False
        if func_key_word == CTOR:
            is_ctor = True
        elif func_key_word == METHOD:
            is_method = True
        self.compile_subroutine_body(name, is_ctor, is_method)

    def compile_parameter_list(self):
        counter = 0
        kind = "arg"
        while self.tokenizer.token_type() != SYMBOL or \
                self.tokenizer.token_type() == SYMBOL and self.tokenizer.symbol() != ")":
            counter = counter + 1
            if self.tokenizer.token_type() == KEYWORD:
                var_type = self.tokenizer.key_word()
                self.eat(self.tokenizer.key_word())  # type
            else:
                var_type = self.tokenizer.key_word()
                self.eat(self.tokenizer.identifier())  # class name
            name = self.tokenizer.identifier()
            self.subroutine_table.define(name, var_type, kind)
            self.eat(self.tokenizer.identifier())  # var name
            if self.tokenizer.symbol() == COMMA:
                self.eat(self.tokenizer.symbol())  # ,
        return counter

    def compile_var_dec(self):
        counter = 1
        self.eat(self.tokenizer.key_word())  # var
        kind = "var"
        if self.tokenizer.token_type() == KEYWORD:
            var_type = self.tokenizer.key_word()
            self.eat(self.tokenizer.key_word())  # type
        elif self.tokenizer.token_type() == IDENTIFIER:
            var_type = self.tokenizer.identifier()
            self.eat(self.tokenizer.identifier())  # class name
        name = self.tokenizer.identifier()
        self.subroutine_table.define(name, var_type, kind)
        self.eat(self.tokenizer.identifier())  # first variable name
        while self.tokenizer.symbol() == COMMA:
            counter = counter + 1
            self.eat(self.tokenizer.symbol())  # ,
            name = self.tokenizer.identifier()
            self.subroutine_table.define(name, var_type, kind)
            self.eat(self.tokenizer.identifier())  # another variable name
        self.eat(self.tokenizer.symbol())  # ;
        return counter

    def compile_statements(self):
        while self.tokenizer.token_type() == KEYWORD:
            if self.tokenizer.key_word() == LET:
                self.compile_let()
            elif self.tokenizer.key_word() == IF:
                self.compile_if()
            elif self.tokenizer.key_word() == WHILE:
                self.compile_while()
            elif self.tokenizer.key_word() == DO:
                self.compile_do()
            elif self.tokenizer.key_word() == RETURN:
                self.compile_return()

    def compile_do(self):
        self.eat(self.tokenizer.key_word())  # do
        self.compile_subroutine_call()
        self.eat(self.tokenizer.symbol())  # ;
        self.vmWriter.write_pop(TEMP, 0)

    def compile_subroutine_call(self):
        first_name = self.tokenizer.identifier()
        second_name = ""
        self.eat(self.tokenizer.identifier())  # subroutine/class/var name
        if self.tokenizer.symbol() == ".":
            self.eat(self.tokenizer.symbol())  # .
            second_name = self.tokenizer.identifier()
            self.eat(self.tokenizer.identifier())  # subroutine name
        if second_name != "" and (self.subroutine_table.contain(first_name) or self.class_table.contain(first_name)):
            self.compile_method_call(first_name, second_name)
        elif second_name != "":  # first name is not an object
            self.compile_function_call(first_name, second_name)
        elif second_name == "":
            self.compile_inner_method_call(first_name)

    def compile_inner_method_call(self, name):
        self.vmWriter.write_push(POINTER, 0)  # push this
        self.eat(self.tokenizer.symbol())  # (
        counter = 1 + self.compile_expression_list()
        self.eat(self.tokenizer.symbol())  # )
        full_name = self.class_name + NAME_SEP + name
        self.vmWriter.write_call(full_name, counter)

    def compile_method_call(self, this_arg, name):
        if self.subroutine_table.contain(this_arg):   
            kind = self.subroutine_table.kind_of(this_arg)   
            index = self.subroutine_table.index_of(this_arg)   
            class_name = self.subroutine_table.type_of(this_arg)   
        elif self.class_table.contain(this_arg):   
            kind = self.class_table.kind_of(this_arg)   
            index = self.class_table.index_of(this_arg)   
            class_name = self.class_table.type_of(this_arg)   
        self.vmWriter.write_push(KIND_TO_SEG_DICT[kind], index)  # push object
        self.eat(self.tokenizer.symbol())  # (
        counter = 1 + self.compile_expression_list()   
        self.eat(self.tokenizer.symbol())  # )
        full_name = class_name + NAME_SEP + name   
        self.vmWriter.write_call(full_name, counter)   

    def compile_function_call(self, class_name, function_name):
        self.eat(self.tokenizer.symbol())  # (
        counter = self.compile_expression_list()   
        self.eat(self.tokenizer.symbol())  # )
        full_name = class_name + NAME_SEP + function_name   
        self.vmWriter.write_call(full_name, counter)

    def init_that(self):
        self.vmWriter.write_arithmetic(ADD)
        self.vmWriter.write_pop("temp", 0)

    def get_var_segment(self, name):
        seg = KIND_TO_SEG_DICT[self.class_table.kind_of(name)] if \
            self.class_table.contain(name) else \
            KIND_TO_SEG_DICT[self.subroutine_table.kind_of(name)]
        return seg

    def get_var_idx(self, name):
        idx = self.class_table.index_of(name) if self.class_table.contain(name) \
            else self.subroutine_table.index_of(name)
        return idx

    def compile_let(self):
        self.eat(self.tokenizer.key_word())  # let
        name = self.tokenizer.identifier()
        self.eat(self.tokenizer.identifier())  # var name
        is_arr = False
        if self.tokenizer.symbol() == "[":
            is_arr = TRUE
            self.eat(self.tokenizer.symbol())  # [
            self.compile_expression()
            self.eat(self.tokenizer.symbol())  # ]
            self.push_term_identifier(name)
            self.init_that()
        self.eat(self.tokenizer.symbol())  # =
        self.compile_expression()
        if is_arr:
            self.vmWriter.write_push("temp", 0)
            self.vmWriter.write_pop(POINTER, 1)
            self.vmWriter.write_pop(THAT, 0)
        else:
            self.vmWriter.write_pop(self.get_var_segment(name),
                                    self.get_var_idx(name))
        self.eat(self.tokenizer.symbol())  # ;

    def compile_while(self):
        self.label_counter = self.label_counter + 1
        label_1 = LABEL_NAME + str(self.label_counter)
        self.label_counter = self.label_counter + 1
        label_2 = LABEL_NAME + str(self.label_counter)
        self.vmWriter.write_label(label_1)  # label L1
        self.eat(self.tokenizer.key_word())  # while
        self.eat(self.tokenizer.symbol())  # (
        self.compile_expression()
        self.vmWriter.write_arithmetic(UNARY_OP_DICT["~"])  # not
        self.eat(self.tokenizer.symbol())  # )
        self.vmWriter.write_if(label_2) # if goto L2
        self.eat(self.tokenizer.symbol())  # {
        self.compile_statements()
        self.eat(self.tokenizer.symbol())  # }
        self.vmWriter.write_goto(label_1)  # goto L1
        self.vmWriter.write_label(label_2) # label L2

    def compile_return(self):
        self.eat(self.tokenizer.key_word())  # return
        if self.tokenizer.symbol() != END_STATEMENT:
            self.compile_expression()
        else:
            self.vmWriter.write_push(CONSTANT, 0)
        self.eat(self.tokenizer.symbol())  # ;
        self.vmWriter.write_return()

    def compile_if(self):
        self.label_counter = self.label_counter + 1
        label_1 = LABEL_NAME + str(self.label_counter)
        self.label_counter = self.label_counter + 1
        label_2 = LABEL_NAME + str(self.label_counter)
        self.eat(self.tokenizer.key_word())  # if
        self.eat(self.tokenizer.symbol())  # (
        self.compile_expression()
        self.vmWriter.write_arithmetic(UNARY_OP_DICT["~"])  # not
        self.eat(self.tokenizer.symbol())  # )
        self.vmWriter.write_if(label_1)  # if goto L1
        self.eat(self.tokenizer.symbol())  # {
        self.compile_statements()
        self.eat(self.tokenizer.symbol())  # }
        self.vmWriter.write_goto(label_2)  # goto L2
        self.vmWriter.write_label(label_1)  # label L1
        if self.tokenizer.key_word() == ELSE:
            self.eat(self.tokenizer.key_word())  # else
            self.eat(self.tokenizer.symbol())  # {
            self.compile_statements()
            self.eat(self.tokenizer.symbol())  # }
        self.vmWriter.write_label(label_2)  # label L2

    def compile_expression(self):
        self.compile_term()
        while self.tokenizer.token_type() == SYMBOL and \
                self.tokenizer.symbol() in OP_SET:
            op = self.tokenizer.symbol()
            self.eat(self.tokenizer.symbol())  # op
            self.compile_term()
            self.vmWriter.write_arithmetic(op)

    def push_term_identifier(self, name):
        if self.subroutine_table.contain(name):
            kind = KIND_TO_SEG_DICT[self.subroutine_table.kind_of(name)]
            idx = self.subroutine_table.index_of(name)
            self.vmWriter.write_push(kind, idx)
        elif self.class_table.contain(name):
            kind = KIND_TO_SEG_DICT[self.class_table.kind_of(name)]
            idx = self.class_table.index_of(name)
            self.vmWriter.write_push(kind, idx)

    def push_array_expression(self):
        self.eat(self.tokenizer.symbol())  # [
        self.compile_expression()
        self.vmWriter.write_arithmetic(ADD)
        self.vmWriter.write_pop(POINTER, THAT_NUM)
        self.vmWriter.write_push(THAT, 0)
        self.eat(self.tokenizer.symbol())  # ]

    def push_keyword_const(self, key_word):
        if key_word == FALSE or key_word == NULL:
            self.vmWriter.write_push(CONSTANT, 0)
        elif key_word == TRUE:
            self.vmWriter.write_push(CONSTANT, 1)
            self.vmWriter.write_arithmetic(UNARY_OP_DICT["-"])
        elif key_word == THIS:
            self.vmWriter.write_push(POINTER, THIS_NUM)

    def push_string(self, string):
        self.vmWriter.write_push(CONSTANT, len(string))
        self.vmWriter.write_call(STRING_CONSTRUCTOR, 1)
        for char in string:
            self.vmWriter.write_push(CONSTANT, ord(char))
            self.vmWriter.write_call(STRING_APPEND_CHAR, 2)

    def compile_term(self):
        if self.tokenizer.token_type() == SYMBOL and \
                self.tokenizer.symbol() == "(":
            self.compile_term_parenthesis()
            return
        if self.tokenizer.token_type() == IDENTIFIER:  # varName\varName[expression]\subroutineCall
            name = self.tokenizer.identifier()
            second_name = ""   
            self.eat(self.tokenizer.identifier())  # name
            if (self.subroutine_table.contain(name) or
                    self.class_table.contain(name)) and self.tokenizer.symbol() != NAME_SEP:
                self.push_term_identifier(name)
            if self.tokenizer.token_type() == SYMBOL and \
                    self.tokenizer.symbol() == "[":  # varName[expression]
                self.push_array_expression()
            elif self.tokenizer.token_type() == SYMBOL and \
                    self.tokenizer.symbol() == ".":  # subroutine call option 2
                self.eat(self.tokenizer.symbol())  # .
                second_name = self.tokenizer.identifier()   
                self.eat(self.tokenizer.identifier())
            if self.tokenizer.token_type() == SYMBOL and \
                    self.tokenizer.symbol() == "(":  # subroutine call
                if second_name != "" and \
                        (self.subroutine_table.contain(name) or self.class_table.contain(name)):   
                    self.compile_method_call(name, second_name)   
                elif second_name != "":  # first name is not an object
                    self.compile_function_call(name, second_name)
                elif second_name == "":
                    self.compile_function_call(self.class_name, name)
        elif self.tokenizer.token_type() == INT_CONST:
            self.vmWriter.write_push(CONSTANT, int(self.tokenizer.int_val()))
            self.eat(self.tokenizer.int_val())
        elif self.tokenizer.token_type() == STRING_CONST:
            self.push_string(self.tokenizer.string_val())               
            self.eat(self.tokenizer.string_val())
        elif self.tokenizer.token_type() == KEYWORD and \
                self.tokenizer.key_word() in KEYWORD_CONSTANT_SET:
            self.push_keyword_const(self.tokenizer.key_word())
            self.eat(self.tokenizer.key_word())
        elif self.tokenizer.token_type() == SYMBOL and \
                self.tokenizer.symbol() in UNARY_OP_SET:
            op = self.tokenizer.symbol()
            self.eat(self.tokenizer.symbol())  # unary op
            self.compile_term()
            self.vmWriter.write_arithmetic(UNARY_OP_DICT[op])

    def compile_term_parenthesis(self):
        self.eat(self.tokenizer.symbol())  # (
        self.compile_expression()
        self.eat(self.tokenizer.symbol())  # )

    def compile_expression_list(self):
        counter = 0
        while self.tokenizer.token_type() != SYMBOL or \
                self.tokenizer.token_type() == SYMBOL and self.tokenizer.symbol() != ")":
            counter = counter + 1   
            self.compile_expression()
            if self.tokenizer.symbol() == COMMA:
                self.eat(self.tokenizer.symbol())  # ,
        return counter   

    def compile_subroutine_body(self, name, is_ctor, is_method):
        counter = 0
        self.eat(self.tokenizer.symbol())  # {
        while self.tokenizer.key_word() == VAR:
            counter = counter + self.compile_var_dec()
        self.vmWriter.write_function(name, counter)
        if is_ctor:
            self.this_init(self.class_table.var_count(FIELD))
        elif is_method:
            self.method_init()
        self.compile_statements()
        self.eat(self.tokenizer.symbol())  # }
        return
