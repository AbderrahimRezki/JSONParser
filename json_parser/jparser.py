import sys
from json_parser.extra.exceptions import JParserExceptionWithExitCode, ParserError
from json_parser.extra.utils import ExitCode
from json_parser.jtoken import JToken, JTokenType
from typing import List


class JParser:
    def __init__(self, tokens):
        self.result = {}
        self.tokens = tokens
        self.current = 0

    def __call__(self):
        return self.parse()

    def parse(self):
        try:
            self.entry()
            self.consume(JTokenType.EOF, error_message="Expected EOF Token at the end of the file.")
        except JParserExceptionWithExitCode as e:
            sys.exit(e.get_exit_code())
        except Exception as e:
            sys.exit(ExitCode.FAILURE)
        else:
            sys.exit(ExitCode.SUCCESS)

    def entry(self):
        self.consume(JTokenType.LEFT_BRACE, error_message="Expected JSON String to start with '{'.")
        while not self.match(JTokenType.RIGHT_BRACE):
            self.parse_kv_pairs()
        self.consume(JTokenType.RIGHT_BRACE, error_message="Expected JSON String to end with '}'")

    def parse_kv_pairs(self):
        key = self.consume(JTokenType.STRING, error_message="Expected JSON Key to be a string.")
        self.consume(JTokenType.COLON, error_message="Expected ':' after JSON Key.")
        value = self.consume(
            JTokenType.STRING, JTokenType.NUMBER, JTokenType.BOOL,
            error_message="Expected JSON value after ':'.")

        self.result[key.literal] = value.literal

    def consume(self, *token_types, error_message: str = ""):
        if self.match(*token_types): return self.advance()
        raise ParserError(error_message)

    def match(self, *token_types):
        token_type: JTokenType
        for token_type in token_types:
            if self.check(token_type):
                return True

        return False

    def check(self, token_type: JTokenType):
        return self.peek().type == token_type

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.peek()
        self.current += 1
        return token

    def is_at_end(self):
        return self.peek() == JTokenType.EOF
