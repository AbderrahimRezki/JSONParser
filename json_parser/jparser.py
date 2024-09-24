import sys
from unittest import result
from json_parser.extra.exceptions import JParserExceptionWithExitCode, ParserError
from json_parser.extra.utils import ExitCode
from json_parser.jtoken import JToken, JTokenType
from typing import List, Tuple, Any


class JParser:
    def __init__(self, tokens):
        self.result = {}
        self.tokens = tokens
        self.current = 0

    def __call__(self):
        return self.parse()

    def parse(self):
        try:
            obj = self.parse_object()
            self.consume(JTokenType.EOF, error_message="Expected EOF Token at the end of the file.")
            self.result = obj
        except JParserExceptionWithExitCode as e:
            sys.exit(e.get_exit_code())
        except Exception as e:
            sys.exit(ExitCode.FAILURE)
        else:
            sys.exit(ExitCode.SUCCESS)

    def parse_object(self):
        self.consume(JTokenType.LEFT_BRACE, error_message="Expected JSON String to start with '{'.")
        kv_pairs: List[Tuple[Any, Any]] = self.parse_kv_pairs()
        self.consume(JTokenType.RIGHT_BRACE, error_message="Expected JSON String to end with '}'")

        result = dict(kv_pairs)

    def parse_kv_pairs(self) -> List[Tuple[Any, Any]]:
        kv_pairs = []

        if not self.match(JTokenType.RIGHT_BRACE):
            kv_pairs.append(self.parse_kv_pair())

        while self.match(JTokenType.COMMA):
            self.consume(JTokenType.COMMA, "Expected ','.")
            kv_pairs.append(self.parse_kv_pair())

        return kv_pairs

    def parse_kv_pair(self) -> Tuple:
        key = self.consume(JTokenType.STRING, error_message="Expected JSON Key to be a string.").literal
        self.consume(JTokenType.COLON, error_message="Expected ':' after JSON Key.")
        value = self.parse_value()

        return key, value

    def parse_value(self):
        basic_data_types = [JTokenType.STRING, JTokenType.NUMBER, JTokenType.BOOL]
        value = None

        if self.match(*basic_data_types):
            value = self.consume(*basic_data_types, error_message="Expected JSON value after ':'.").literal
        elif self.match(JTokenType.LEFT_SQUARE_BRACKET):
            value = self.parse_array()
        elif self.match(JTokenType.LEFT_BRACE):
            value = self.parse_object()

        return value

    def parse_array(self):
        self.consume(JTokenType.LEFT_SQUARE_BRACKET)

        result_array = []
        if self.match(JTokenType.RIGHT_SQUARE_BRACKET):
            self.consume(JTokenType.RIGHT_SQUARE_BRACKET)
            return result_array

        result_array.append(self.parse_value())
        while self.match(JTokenType.COMMA):
            self.consume(JTokenType.COMMA)
            result_array.append(self.parse_value())

        self.consume(JTokenType.RIGHT_SQUARE_BRACKET, error_message="'[' opened but was never closed.")
        return result_array

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
