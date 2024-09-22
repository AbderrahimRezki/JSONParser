from json_parser.extra.exceptions import ParserError
from json_parser.jtoken import JToken, JTokenType
from typing import List


class JParser:
    def __init__(self, tokens):
        self.result = {}
        self.tokens = tokens
        self.current = 0

    def __call__(self, tokens):
        return self.parse(tokens)

    def parse(self, tokens):
        self.entry()
        self.consume(JTokenType.EOF, "Expected EOF Token at the end of the file.")

    def entry(self):
        self.consume(JTokenType.LEFT_BRACE, "Expected JSON String to start with '{'.")
        self.parse_kv_pairs()
        self.consume(JTokenType.RIGHT_BRACE, "Expected JSON String to end with '}'")

    def parse_kv_pairs(self): pass

    def consume(self, token_type: JTokenType, error_message: str):
        if self.match(token_type): return self.advance()
        raise ParserError(error_message)

    def match(self, *token_types):
        token_type: JTokenType
        for token_type in token_types:
            if self.peek().type == token_type:
                return True

        return False

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        token = self.peek()
        self.current += 1
        return token

    def is_at_end(self):
        return self.peek() == JTokenType.EOF
