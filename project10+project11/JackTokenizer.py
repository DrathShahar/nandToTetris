import string

FIRST_IDX = 0
LINE_COMMENT = "//"
COMMENT_OPEN_1 = "/"
COMMENT_OPEN_2 = "*"
COMMENT_CLOSE_1 = "*"
COMMENT_CLOSE_2 = "/"
EMPTY_LINE = ""
SYMBOL_SET = {"&amp;", "&lt;", "&gt;"}.union(set("{}()[].,;+-*/&|<>=~"))
STR = "\""
NEW_LINE = "\n"
WHITE_SPACE = string.whitespace
DIGITS = "0123456789"
KEYWORD = 1
SYMBOL = 2
IDENTIFIER = 3
INT_CONST = 4
STRING_CONST = 5
NEED_FORMATTING_DICT = {"<": "&lt;", ">": "&gt;", "&": "&amp;"}
KEYWORD_SET = {"class", "constructor", "function", "method", "field", "static",
               "var", "int", "char", "boolean", "void", "true", "false",
               "null", "this", "let", "do", "if", "else", "while", "return"}


class JackTokenizer:
    def __init__(self, file_name):
        self.file = open(file_name)
        self.tokens = []  # here all the tokens will be
        self.file_txt = ""  # file text without comments will be stored here
        self.curr = -1
        self.remove_comments()
        self.make_tokens()
        self.format_tokens()

    def remove_comments(self):
        last = ""
        is_comment = is_line_comment = is_str = False
        while True:
            c = self.file.read(1)
            if not c:
                break
            if last == COMMENT_OPEN_1 and c == COMMENT_OPEN_2 and not is_str\
                    and not is_line_comment:
                self.file_txt = self.file_txt[:-1]
                is_comment = True
                continue
            if last == COMMENT_OPEN_1 and c == COMMENT_OPEN_1 and not is_str\
                    and not is_comment:
                self.file_txt = self.file_txt[:-1]
                is_line_comment = True
                continue
            if last == COMMENT_CLOSE_1 and c == COMMENT_CLOSE_2 and is_comment:
                is_comment = False
                self.file_txt = self.file_txt + " "
                continue
            if c == NEW_LINE and is_line_comment:
                is_line_comment = False
                self.file_txt = self.file_txt + " "
            if c == STR and not is_comment and not is_line_comment:
                is_str = not is_str
            if not is_comment and not is_line_comment:
                self.file_txt += c
            last = c

    def make_tokens(self):
        token_lst = []
        is_str = False
        last_idx = -1
        for idx in range(len(self.file_txt)):
            if self.file_txt[idx] == STR:
                if is_str:
                    token_lst.append(self.file_txt[last_idx + 1:idx + 1])
                    last_idx = idx
                is_str = not is_str
                continue
            if is_str:
                continue
            if self.file_txt[idx] in WHITE_SPACE:
                if last_idx != -1 and last_idx + 1 != idx:
                    token_lst.append(self.file_txt[last_idx + 1: idx])
                last_idx = idx
                continue
            if self.file_txt[idx] in SYMBOL_SET:
                if idx != last_idx + 1:
                    token_lst.append(self.file_txt[last_idx + 1: idx])
                token_lst.append(self.file_txt[idx])
                last_idx = idx
                continue
        self.tokens = token_lst

    def format_tokens(self):
        for idx in range(len(self.tokens)):
            if self.tokens[idx] in NEED_FORMATTING_DICT:
                self.tokens[idx] = NEED_FORMATTING_DICT[self.tokens[idx]]

    def has_more_tokens(self):
        return self.curr < len(self.tokens) and len(self.tokens) > 0

    def advance(self):
        self.curr = self.curr + 1

    def token_type(self):  # will check in which set self.tokens[self.curr]
        # is contained (like the symbol set) and will return appropriate number
        # constant (initialized at beginning)
        if self.tokens[self.curr] in SYMBOL_SET:
            return SYMBOL
        elif self.tokens[self.curr] in KEYWORD_SET:
            return KEYWORD
        elif self.tokens[self.curr][FIRST_IDX] == STR:
            return STRING_CONST
        elif self.tokens[self.curr][FIRST_IDX] in DIGITS:
            return INT_CONST
        else:
            return IDENTIFIER

    def key_word(self):
        return self.tokens[self.curr]

    def symbol(self):
        return self.tokens[self.curr]

    def identifier(self):
        return self.tokens[self.curr]

    def int_val(self):
        return self.tokens[self.curr]

    def string_val(self):
        return self.tokens[self.curr][1:-1]