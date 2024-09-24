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

    def test_parse_empty_json_returns_empty_dict(self):
        empty_json = "{}"
        empty_dict = {}

        self._test_parse_json_returns_dict_and_exit_code(empty_json, empty_dict)


    def test_parse_single_key_string_value_returns_dict(self):
        json_string = '{"key" : "value"}'
        result_dict = {"key": "value"}

        self._test_parse_json_returns_dict_and_exit_code(json_string, result_dict)

    def test_parse_single_key_int_value_returns_dict(self):
        json_string = '{"key" : 37}'
        result_dict = {"key": 37}

        self._test_parse_json_returns_dict_and_exit_code(json_string, result_dict)


    def _test_parse_json_returns_dict_and_exit_code(self, json_string, result_dict, exit_code=ExitCode.SUCCESS, debug=True):
        lexer = JLexer(json_string)
        tokens = lexer.get_tokens()

        if debug:
            print("Tokens: ", *tokens, sep="\n\t-")

        parser = JParser(tokens)

        with self.assertRaises(SystemExit) as cm:
            parser.parse()
            result = parser.result
            self.assertDictEqual(result, result_dict)

        self.assertEqual(cm.exception.code, exit_code)

if __name__ == "__main__":
    unittest.main()
