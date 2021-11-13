WRITE = "w"
ADD = "add"
SUB = "sub"
AND = "and"
OR = "or"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
NOT = "not"
NEW_LINE = "\n"
COMMENT_PREFIX = "// "
C_PUSH = 2
C_POP = 3
POINTER = "pointer"
CONST = "constant"
STATIC = "static"
TEMP = "temp"
FIVE = "5"
ARITHMETIC_DICT = {ADD: "+", SUB: "-", AND: "&", OR: "|", NEG: "-", NOT: "!",
                   EQ: "JEQ", GT: "JGT", LT: "JLT"}

COMMANDS_DICT_COMMENT = {1: "arithmetic", 2: "push", 3: "pop", 4: "label",
                         5: "goto", 6: "if-goto", 7: "function", 8: "return",
                         9: "call"}

LCL_ARG_THIS_THAT_DICT = {"local": "LCL", "argument": "ARG", "this":
                               "THIS", "that": "THAT"}
POINTER_DICT = {0: "THIS", 1: "THAT"}

ADD_SUB_AND_OR_COMM = "@SP\n" \
                  "M=M-1\n" \
                  "A=M\n" \
                  "D=M\n" \
                  "@SP\n" \
                  "M=M-1\n" \
                  "A=M\n" \
                  "D=M%sD\n" \
                  "M=D\n" \
                  "@SP\n" \
                  "M=M+1\n"

NEG_NOT_COMM = "@SP\n" \
              "M=M-1\n" \
               "A=M\n" \
               "M=%sM\n" \
               "@SP\n" \
               "M=M+1\n" \

EQ_GT_LT_COMM = "@SP\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@Y_POS%s\n" \
              "D;JGT\n" \
              "@SP\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@%s%s\n" \
              "D;JGT\n" \
              "@SAME_SIGN%s\n" \
              "0;JMP\n" \
              "(Y_POS%s)\n" \
              "@SP\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@%s%s\n" \
              "D;JLT\n" \
              "(SAME_SIGN%s)\n" \
              "@SP\n" \
              "M=M+1\n" \
              "A=M\n" \
              "D=M\n" \
              "@SP\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M-D\n" \
              "@TRUE%s\n" \
              "D;%s\n" \
              "@FALSE%s\n" \
              "0;JMP\n" \
              "(TRUE%s)\n" \
              "@SP\n" \
              "A=M\n" \
              "M=-1\n" \
              "@END%s\n" \
              "0;JMP\n" \
              "(FALSE%s)\n" \
              "@SP\n" \
              "A=M\n" \
              "M=0\n" \
              "(END%s)\n" \
              "@SP\n" \
              "M=M+1\n"

POP_LCL_ARG_THIS_THAT_COMM = "@%s\n" \
                            "D=A\n" \
                             "@%s\n" \
                             "D=D+M\n" \
                             "@addr\n" \
                             "M=D\n" \
                             "@SP\n" \
                             "M=M-1\n" \
                             "@SP\n" \
                             "A=M\n" \
                             "D=M\n" \
                             "@addr\n" \
                             "A=M\n" \
                             "M=D\n"

POP_TEMP_COMM = "@%s\n" \
                "D=A\n" \
                "@%s\n" \
                "D=D+A\n" \
                "@addr\n" \
                "M=D\n" \
                "@SP\n" \
                "M=M-1\n" \
                "@SP\n" \
                "A=M\n" \
                "D=M\n" \
                "@addr\n" \
                "A=M\n" \
                "M=D\n"


PUSH_LCL_ARG_THIS_THAT_COMM = "@%s\n" \
                            "D=A\n" \
                             "@%s\n" \
                             "D=D+M\n" \
                             "@addr\n" \
                             "M=D\n" \
                             "A=M\n" \
                             "D=M\n" \
                             "@SP\n" \
                             "A=M\n" \
                             "M=D\n"\
                             "@SP\n" \
                             "M=M+1\n"

PUSH_TEMP_COMM = "@%s\n" \
                            "D=A\n" \
                             "@%s\n" \
                             "D=D+A\n" \
                             "@addr\n" \
                             "M=D\n" \
                             "A=M\n" \
                             "D=M\n" \
                             "@SP\n" \
                             "A=M\n" \
                             "M=D\n"\
                             "@SP\n" \
                             "M=M+1\n"

POINTER_PUSH_COMM = "@%s\n" \
                    "D=M\n" \
                    "@SP\n" \
                    "A=M\n" \
                    "M=D\n" \
                    "@SP\n" \
                    "M=M+1\n"

POINTER_POP_COMM = "@SP\n" \
                    "M=M-1\n" \
                    "A=M\n" \
                    "D=M\n" \
                    "@%s\n" \
                    "M=D\n" \

PUSH_CONSTANT_COMM = "@%s\n" \
                     "D=A\n" \
                     "@SP\n" \
                     "A=M\n" \
                     "M=D\n" \
                     "@SP\n" \
                     "M=M+1\n"

POP_STATIC_COMM = "@SP\n" \
                  "M=M-1\n"\
                  "A=M\n" \
                  "D=M\n" \
                  "@%s.%s\n" \
                  "M=D\n"

PUSH_STATIC_COMM = "@%s.%s\n" \
                   "D=M\n" \
                   "@SP\n" \
                   "A=M\n" \
                   "M=D\n" \
                   "@SP\n" \
                   "M=M+1\n"

FUNCTION_COMM = "(%s)\n" \
                "@%s\n" \
                "D=A\n" \
                "@num_vars\n" \
                "M=D\n" \
                "@i\n" \
                "M=0\n" \
                "(LOOP.%s)\n" \
                "@num_vars\n" \
                "D=M\n" \
                "@i\n" \
                "D=D-M\n" \
                "@END_LOOP.%s\n" \
                "D;JEQ\n" \
                "@SP\n" \
                "A=M\n" \
                "M=0\n" \
                "@SP\n" \
                "M=M+1\n" \
                "@i\n" \
                "M=M+1\n" \
                "@LOOP.%s\n" \
                "0;JMP\n" \
                "(END_LOOP.%s)\n"

CALL_COMM = "@%s$ret.%s\n" \
            "D=A\n" \
            "@SP\n" \
            "A=M\n" \
            "M=D\n" \
            "@SP\n" \
            "M=M+1\n" \
            "@LCL\n" \
            "D=M\n" \
            "@SP\n" \
            "A=M\n" \
            "M=D\n" \
            "@SP\n" \
            "M=M+1\n" \
            "@ARG\n" \
            "D=M\n" \
            "@SP\n" \
            "A=M\n" \
            "M=D\n" \
            "@SP\n" \
            "M=M+1\n" \
            "@THIS\n" \
            "D=M\n" \
            "@SP\n" \
            "A=M\n" \
            "M=D\n" \
            "@SP\n" \
            "M=M+1\n" \
            "@THAT\n" \
            "D=M\n" \
            "@SP\n" \
            "A=M\n" \
            "M=D\n" \
            "@SP\n" \
            "M=M+1\n" \
            "D=M\n" \
            "@5\n" \
            "D=D-A\n" \
            "@%s\n" \
            "D=D-A\n" \
            "@ARG\n" \
            "M=D\n" \
            "@SP\n" \
            "D=M\n" \
            "@LCL\n" \
            "M=D\n" \
            "@%s\n" \
            "0;JMP\n" \
            "(%s$ret.%s)\n"

RETURN_COMM = "@LCL\n" \
              "D=M\n" \
              "@endFrame\n" \
              "M=D\n" \
              "@5\n" \
              "A=D-A\n" \
              "D=M\n" \
              "@retAdd\n" \
              "M=D\n" \
              "@SP\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@ARG\n" \
              "A=M\n" \
              "M=D\n" \
              "@ARG\n" \
              "D=M+1\n" \
              "@SP\n" \
              "M=D\n" \
              "@endFrame\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@THAT\n" \
              "M=D\n" \
              "@endFrame\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@THIS\n" \
              "M=D\n" \
              "@endFrame\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@ARG\n" \
              "M=D\n" \
              "@endFrame\n" \
              "M=M-1\n" \
              "A=M\n" \
              "D=M\n" \
              "@LCL\n" \
              "M=D\n" \
              "@retAdd\n" \
              "A=M\n" \
              "0;JMP\n"

LABEL_COMM = "(%s%s)\n"

GOTO_COMM = "@%s%s\n" \
            "0;JMP\n"

IF_GOTO_COMM = "@SP\n" \
               "M=M-1\n" \
               "A=M\n" \
               "D=M\n" \
               "@%s%s\n" \
               "D;JNE\n"

INIT_COMM = "@256\n" \
            "D=A\n" \
            "@SP\n" \
            "M=D\n"


class CodeWriter:
    def __init__(self):
        self.file_name = ""
        self.file = None
        self.static_name = ""
        self.counter = 0
        self.func_name = ""

    def set_static_name(self, static_start):
        self.static_name = static_start

    def write_arithmetic(self, command):
        c_str = str(self.counter)
        self.write_command_comment(command)
        if command == NEG or command == NOT:
            self.file.write(NEG_NOT_COMM % ARITHMETIC_DICT[command])
            return
        if command == GT:
            self.file.write(EQ_GT_LT_COMM % (c_str, "TRUE", c_str, c_str,
                c_str, "FALSE", c_str, c_str, c_str, ARITHMETIC_DICT[command],
                                        c_str, c_str, c_str, c_str, c_str))
            return
        if command == LT:
            self.file.write(EQ_GT_LT_COMM % (c_str, "FALSE", c_str, c_str,
                c_str, "TRUE", c_str, c_str, c_str, ARITHMETIC_DICT[command],
                                        c_str, c_str, c_str, c_str, c_str))
            return
        if command == EQ:
            self.file.write(EQ_GT_LT_COMM % (c_str, "FALSE", c_str, c_str,
                c_str, "FALSE", c_str, c_str, c_str, ARITHMETIC_DICT[command],
                                        c_str, c_str, c_str, c_str, c_str))
            return
        self.file.write(ADD_SUB_AND_OR_COMM % ARITHMETIC_DICT[command])

    def write_push_pop(self, command, segment, idx):
        self.write_command_comment(COMMANDS_DICT_COMMENT[command] +
                                   " " + segment + " " + idx)
        if command == C_PUSH:
            if segment in LCL_ARG_THIS_THAT_DICT:
                self.file.write(PUSH_LCL_ARG_THIS_THAT_COMM %
                                (str(idx), LCL_ARG_THIS_THAT_DICT[segment]))
            elif segment == TEMP:
                self.file.write(PUSH_TEMP_COMM %
                                (str(idx), FIVE))
            elif segment == POINTER:
                self.file.write(POINTER_PUSH_COMM % POINTER_DICT[int(idx)])
            elif segment == CONST:
                self.file.write(PUSH_CONSTANT_COMM % str(idx))
            elif segment == STATIC:
                self.file.write(PUSH_STATIC_COMM % (self.static_name, idx))
            return
        if segment in LCL_ARG_THIS_THAT_DICT:
            self.file.write(POP_LCL_ARG_THIS_THAT_COMM %
                            (str(idx), LCL_ARG_THIS_THAT_DICT[segment]))
        elif segment == TEMP:
            self.file.write(POP_TEMP_COMM %
                            (str(idx), FIVE))
        elif segment == POINTER:
            self.file.write(POINTER_POP_COMM % POINTER_DICT[int(idx)])
        elif segment == STATIC:
            self.file.write(POP_STATIC_COMM % (self.static_name, idx))

    def close(self):
        self.file.close()

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.file = open(self.file_name, WRITE)
        self.counter = 0

    def write_command_comment(self, comment):
        self.file.write(COMMENT_PREFIX + comment + "\n")

    def write_function(self, function_name, num_vars):
        c_str = str(self.counter)
        n_str = str(num_vars)
        self.write_command_comment("function" + " " + function_name + " " + n_str)
        self.file.write(FUNCTION_COMM % (function_name, n_str, c_str,
                                         c_str, c_str, c_str))

    def write_call(self, function_name, num_args):
        c_str = str(self.counter)
        n_str = str(num_args)
        self.write_command_comment("call" + " " + function_name + " " + n_str)
        self.file.write(CALL_COMM % (function_name, c_str, n_str,
                                         function_name, function_name, c_str))

    def write_init(self):
        self.write_command_comment("init")
        self.file.write(INIT_COMM)
        self.write_call("Sys.init", 0)

    def write_return(self):
        self.write_command_comment("return")
        self.file.write(RETURN_COMM)

    def write_label(self, label_name):
        self.write_command_comment("label " + label_name)
        self.file.write(LABEL_COMM % (self.func_name + ":", label_name))

    def write_goto(self, label_name):
        self.write_command_comment("goto " + label_name)
        self.file.write(GOTO_COMM % (self.func_name + ":", label_name))

    def write_if(self, label_name):
        self.write_command_comment("if-goto " + label_name)
        self.file.write(IF_GOTO_COMM % (self.func_name + ":", label_name))



