import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

INPUT_FILE_NAME_IDX = 1
READ = "r"
OUTPUT_XML_END = ".xml"
OUTPUT_VM_END = ".vm"
KEYWORD = 1


def get_xml_name(input_file_name):
    head, tail = os.path.split(input_file_name)
    head = str(head)
    tail = str(tail)
    tail = tail.split(".")[0] + OUTPUT_XML_END
    return os.path.join(head, tail)


def get_vm_name(input_file_name):
    head, tail = os.path.split(input_file_name)
    head = str(head)
    tail = str(tail)
    tail = tail.split(".")[0] + OUTPUT_VM_END
    return os.path.join(head, tail)


def main():
    if os.path.isfile(sys.argv[INPUT_FILE_NAME_IDX]):
        output_xml_name = get_xml_name(sys.argv[INPUT_FILE_NAME_IDX])
        output_vm_name = get_vm_name(sys.argv[INPUT_FILE_NAME_IDX])
        tokenizer = JackTokenizer(sys.argv[INPUT_FILE_NAME_IDX])
        engine = CompilationEngine(tokenizer, output_xml_name, output_vm_name)
        engine.compile_class()
        return

    for file in os.listdir(sys.argv[INPUT_FILE_NAME_IDX]):
        file_path = os.path.join(sys.argv[INPUT_FILE_NAME_IDX], str(file))
        split_file_name = file_path.split(".")
        if os.path.isfile(file_path) and \
                split_file_name[len(split_file_name) - 1] == "jack":
            output_xml_name = get_xml_name(file_path)
            output_vm_name = get_vm_name(file_path)
            tokenizer = JackTokenizer(file_path)
            engine = CompilationEngine(tokenizer, output_xml_name,
                                       output_vm_name)
            engine.compile_class()
    return


if __name__ == '__main__':
    main()
