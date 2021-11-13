from Parser import Parser
from CodeWriter import CodeWriter
import sys
import os

INPUT_FILE_NAME_IDX = 1
C_ARITHMETIC = 1
C_PUSH = 2
C_POP = 3
C_LABEL = 4
C_GOTO = 5
C_IF = 6
C_FUNCTION = 7
C_RETURN = 8
C_CALL = 9
OUTPUT_FILE_END = ".asm"
PROGRAM_IDX = 1


def get_output_file_name(input_file_dir):
    head, tail = os.path.split(input_file_dir)
    head = str(head)
    tail = str(tail)
    tail = tail.split(".")[0] + OUTPUT_FILE_END
    return os.path.join(head, tail)


def get_output_file_name_dir(input_file_dir):
    head, tail = os.path.split(input_file_dir)
    tail = str(tail)
    tail = tail + OUTPUT_FILE_END
    return os.path.join(input_file_dir, tail)


def translate_file(input_file_name, code_writer):
    parser = Parser(input_file_name)
    head, tail = os.path.split(input_file_name)
    tail = str(tail)
    code_writer.set_static_name(tail.split(".")[0])
    code_writer.write_init()
    while parser.has_more_commands():
        code_writer.counter = code_writer.counter + 1
        parser.advance()
        if parser.command_type() == C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif parser.command_type() == C_PUSH:
            code_writer.write_push_pop(C_PUSH, parser.arg1(), parser.arg2())
        elif parser.command_type() == C_POP:
            code_writer.write_push_pop(C_POP, parser.arg1(), parser.arg2())
        elif parser.command_type() == C_LABEL:
            code_writer.write_label(parser.arg1())
        elif parser.command_type() == C_GOTO:
            code_writer.write_goto(parser.arg1())
        elif parser.command_type() == C_IF:
            code_writer.write_if(parser.arg1())
        elif parser.command_type() == C_FUNCTION:
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == C_RETURN:
            code_writer.write_return()
        elif parser.command_type() == C_CALL:
            code_writer.write_call(parser.arg1(), parser.arg2())


def main():
    if len(sys.argv) == 1:
        sys.argv.append(os.path.dirname(os.path.abspath(__file__)))
    code_writer = CodeWriter()
    if os.path.isfile(sys.argv[PROGRAM_IDX]):
        output_file_name = get_output_file_name(sys.argv[PROGRAM_IDX])
        code_writer.set_file_name(output_file_name)
        translate_file(sys.argv[PROGRAM_IDX], code_writer)
        return
    output_file_name = get_output_file_name_dir(sys.argv[PROGRAM_IDX])
    code_writer.set_file_name(output_file_name)
    for file in os.listdir(sys.argv[PROGRAM_IDX]):
        file_path = os.path.join(sys.argv[PROGRAM_IDX], str(file))
        split_file_name = file_path.split(".")
        if os.path.isfile(file_path) and \
                split_file_name[len(split_file_name) - 1] == "vm":
            translate_file(file_path, code_writer)


if __name__ == '__main__':
    main()