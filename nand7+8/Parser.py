READ = "r"
C_ARITHMETIC = 1

COMMANDS_DICT = {"push": 2, "pop": 3, "label": 4, "goto": 5, "if-goto": 6,
                 "function": 7, "return": 8, "call": 9}


def filter_commands(file_lines):
    commands = []
    for line in file_lines:
        no_comments = line.split("//")[0]
        if any(c.isalpha() for c in no_comments):  # if no_comments contains a letter
            commands.append(no_comments)
    return commands


class Parser:
    def __init__(self, input_file_name):
        self.file_name = input_file_name
        self.command = 0
        self.argument1 = ""
        self.argument2 = ""
        self.input_file = open(input_file_name, READ)
        self.commands_lines = filter_commands(self.input_file.readlines())
        self.input_file.close()
        self.next_line_to_read = 0

    def has_more_commands(self):
        return self.next_line_to_read < len(self.commands_lines)

    def advance(self):
        parsed_line = self.commands_lines[self.next_line_to_read].split()
        if len(parsed_line) == 1:
            self.argument1 = parsed_line[0]  # arithmetic or return
        elif len(parsed_line) == 2:  # label, goto or if-goto
            self.argument1 = parsed_line[1]
        elif len(parsed_line) == 3:  # push, pop, function or call
            self.argument1 = parsed_line[1]
            self.argument2 = parsed_line[2]
        self.next_line_to_read = self.next_line_to_read + 1
        if parsed_line[0] in COMMANDS_DICT:
            self.command = COMMANDS_DICT[parsed_line[0]]
        else:
            self.command = C_ARITHMETIC
        return

    def command_type(self):
        return self.command

    def arg1(self):
        return self.argument1

    def arg2(self):
        return self.argument2