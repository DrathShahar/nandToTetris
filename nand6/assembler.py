import sys

PROGRAM_IDX = 1
COMMAND_IDX = 0
VALID_INST_LEN = 16
READ = "r"
WRITE = "w"
A_INST = "@"
M_REG = "M"
FIRST_IDX = 0
C_INST_PADDING = "111"
M_IN_COMP = "1"
M_NOT_IN_COMP = "0"
LABEL_INST = "("
OUTPUT_FILE_END = ".hack"
NEW_LINE = "\n"
NO_COMMAND = "NONE"
COMP_DICT_M = {"M": "110000", "!M": "110001", "-M": "110011", "M+1": "110111",
               "M-1": "110010", "D+M": "000010", "D-M": "010011",
               "M-D": "000111", "D&M": "000000", "D|M": "010101"}
COMP_DICT_A = {"0": "101010", "1": "111111", "-1": "111010", "D": "001100",
               "A": "110000", "!D": " 001101", "!A": "110001", "-D": "001111",
               "-A": "110011", "D+1": "011111",  "A+1": "110111",
               "D-1": "001110", "A-1": "110010", "D+A": "000010",
               "D-A": "010011", "A-D": "000111", "D&A": "000000",
               "D|A": "010101"}
DEST_DICT = {"NONE": "000", "A": "100", "D": "010", "M": "001", "AD": "110",
             "ADM": "111", "AM": "101", "MD": "011"}
JUMP_DICT = {"NONE": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
             "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
COMP_ZERO = "0101010"


def assemble_file():
    input_file = open(sys.argv[PROGRAM_IDX], READ)
    output_file = open(get_output_file_name(), WRITE)
    for line in input_file:
        no_white_spaces_line = "".join(line.split())
        parsed_line = no_white_spaces_line.split("//")[COMMAND_IDX]
        if parsed_line[0] == A_INST:
            output_file.write(parse_a_inst(parsed_line))
            continue
        output_file.write(parse_c_inst(parsed_line))


def parse_a_inst(a_line):
    decimal_address = a_line[1:]
    binary = bin(int(decimal_address))
    remaining_len = VALID_INST_LEN - len(binary[2:])
    binary_address = "0" * remaining_len + binary[2:] + NEW_LINE
    return binary_address


def parse_c_inst(c_line):
    parsed_c = C_INST_PADDING
    dest_parsed = c_line.split("=")
    comp = dest_parsed[len(dest_parsed) - 1].split(";")[FIRST_IDX]
    if M_REG in comp:
        parsed_c += M_IN_COMP
    else:
        parsed_c += M_NOT_IN_COMP
    if parsed_c[len(parsed_c) - 1] == M_IN_COMP:
        parsed_c += COMP_DICT_M[comp]
    else:
        parsed_c += COMP_DICT_A[comp]
    if len(dest_parsed) != 1:
        parsed_c += DEST_DICT[dest_parsed[FIRST_IDX]]
    else:
        parsed_c += DEST_DICT[NO_COMMAND]
    jmp_parsed = c_line.split(";")
    if len(jmp_parsed) != 1:
        parsed_c += JUMP_DICT[jmp_parsed[len(jmp_parsed) - 1]]
    else:
        parsed_c += JUMP_DICT[NO_COMMAND]
    return parsed_c




def get_output_file_name():
    dir_lst = sys.argv[PROGRAM_IDX].split("\\")
    dir_lst[len(dir_lst) - 1] = (dir_lst[len(dir_lst) - 1]).split(".")[0] + \
                       OUTPUT_FILE_END
    return "\\".join(dir_lst)


if __name__ == '__main__':
    print(parse_c_inst("MD=D+M;JGT"))


