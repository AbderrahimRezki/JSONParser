from json_parser.jtoken import JToken, JTokenType
from json_parser.extra.exceptions import *
from typing import List


class JLexer:
    def __init__(self, json_string):
        self.json_string = json_string
        self.tokens: List[JToken] = []

        self.start = 0
        self.current = 0
        self.line = 1

    def __call__(self):
        return self.get_tokens()

    def get_tokens(self):
        while not self.is_at_end():
            self.get_token()
            self.start = self.current

        self.add_token(JTokenType.EOF)
        return self.tokens

    def get_token(self):
        c = self.advance()

        match(c):
            case x if x in [" ", "\t", "\r"]: pass

            case   "{": self.add_token(JTokenType.LEFT_BRACE)
            case   "}": self.add_token(JTokenType.RIGHT_BRACE)
            case  "\"": self.string()
            case   ":": self.add_token(JTokenType.COLON)
            case  "\n": self.line += 1
            case     _: raise InvalidTokenException(f"Character <{c}> is not recognized.")

    def string(self):
        while not self.peek() == "\"" and not self.is_at_end():
            if self.peek() == "\n": self.line += 1
            self.advance()

        if self.is_at_end():
            raise LexerError(f"Unterminated string at line {self.line}.")

        literal = self.json_string[self.start + 1:self.current]
        self.add_token_(JTokenType.STRING, literal)
        self.advance()


    def peek(self):
        return self.json_string[self.current]

    def add_token(self, token_type):
        self.add_token_(token_type, None)

    def add_token_(self, token_type, literal):
        lexeme = self.json_string[self.start:self.current]
        token = JToken(token_type, lexeme, literal, self.line)

        self.tokens.append(token)

    def advance(self):
        value = self.json_string[self.current]
        self.current += 1
        return value

    def is_at_end(self):
        return self.current >= len(self.json_string)
