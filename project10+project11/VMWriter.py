RETURN_COMM = "return\n"
WRITE = "w"
PUSH_COMMAND = "push %s %d\n"

POP_COMMAND = "pop %s %d\n"

END_LINE = "\n"

ARITHMETIC_DICT = {"+": "add", "-": "sub", "*": "call Math.multiply 2",
                   "/": "call Math.divide 2", "&amp;": "and", "- ": "neg",
                   "|": "or", "<": "lt", ">": "gt", "=": "eq", "~": "not",
                   "&gt;": "gt", "&lt;": "lt"}

LABEL_COMMAND = "label %s\n"

GOTO_COMMAND = "goto %s\n"

IF_GOTO_COMMAND = "if-goto %s\n"

CALL_COMMAND = "call %s %s\n"

FUNC_COMMAND = "function %s %s\n"


class VMWriter:
    def __init__(self, output_file):
        self.file = open(output_file, WRITE)

    def write_push(self, seg, idx):
        self.file.write(PUSH_COMMAND % (seg, idx))

    def write_pop(self, seg, idx):
        self.file.write(POP_COMMAND % (seg, idx))

    def write_arithmetic(self, command):
        self.file.write(str(ARITHMETIC_DICT[command]) + END_LINE)  # **

    def write_label(self, label):
        self.file.write(LABEL_COMMAND % label)

    def write_goto(self, label):
        self.file.write(GOTO_COMMAND % label)

    def write_if(self, label):
        self.file.write(IF_GOTO_COMMAND % label)

    def write_call(self, name, n_args):
        self.file.write(CALL_COMMAND % (name, n_args))

    def write_function(self, name, n_locals):
        self.file.write(FUNC_COMMAND % (name, n_locals))

    def write_return(self):
        self.file.write(RETURN_COMM)

    def close(self):
        self.file.close()

