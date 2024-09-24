from contextlib import redirect_stdout
import unittest
from io import StringIO
from json_parser import JParser
from json_parser.extra.exceptions import InvalidJsonException
from json_parser.extra.utils import ExitMessage, ExitCode
from json_parser.jlexer import JLexer

class TestJsonParser(unittest.TestCase):
    def setUp(self):
        self.stream = StringIO()

    def test_parse_empty_json_returns_empty_dict(self):
        empty_json = "{}"

        lexer = JLexer(empty_json)
        tokens = lexer.get_tokens()

        parser = JParser(tokens)

        with self.assertRaises(SystemExit) as cm:
            parser.parse()
            result = parser.result
            self.assertDictEqual(result, {})

        self.assertEqual(cm.exception.code, ExitCode.SUCCESS)

    def test_parse_invalid_json_raises_exception(self):
        invalid_json = "{\"key\"}"

        lexer = JLexer(invalid_json)
        tokens = lexer.get_tokens()

        parser = JParser(tokens)

        with self.assertRaises(SystemExit) as cm:
            parser.parse()
            result = parser.result
            self.assertRaises(InvalidJsonException)

        self.assertEqual(cm.exception.code, ExitCode.INVALID)

    def test_parse_single_key_string_value_returns_dict(self):
        single_key_value_json = '{"key" : "value"}'
        single_key_value_dict = {"key": "value"}

        lexer = JLexer(single_key_value_json)
        tokens = lexer.get_tokens()

        parser = JParser(tokens)

        with self.assertRaises(SystemExit) as cm:
            parser.parse()
            result = parser.result
            self.assertDictEqual(result, single_key_value_dict)

        self.assertEqual(cm.exception.code, ExitCode.SUCCESS)


if __name__ == "__main__":
    unittest.main()
