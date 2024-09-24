from contextlib import redirect_stdout
import unittest
from io import StringIO
from json_parser import JParser
from json_parser.extra.exceptions import InvalidJsonException, InvalidTokenException
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
        self.assertRaises(InvalidJsonException, parser.parse)


    def test_parse_empty_json_returns_empty_dict(self):
        empty_json = "{}"
        empty_dict = {}

        self._test_parse_json_returns_dict(empty_json, empty_dict)


    def test_parse_single_key_string_value_returns_dict(self):
        json_string = '{"key" : "value"}'
        result_dict = {"key": "value"}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_single_key_int_value_returns_dict(self):
        json_string = '{"key" : 37}'
        result_dict = {"key": 37}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_single_key_float_value_returns_dict(self):
        json_string = '{"key" : 37.56}'
        result_dict = {"key": 37.56}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_single_key_float_value_raises_exception(self):
        json_string = '{"key" : 37.5.6}'
        lexer = JLexer(json_string)
        self.assertRaises(InvalidTokenException, lexer.get_tokens)

    def test_parse_single_key_bool_value_returns_dict(self):
        json_string = '{"key" : true}'
        result_dict = {"key": True}

        self._test_parse_json_returns_dict(json_string, result_dict)

        json_string = '{"key" : false}'
        result_dict = {"key": False}

        self._test_parse_json_returns_dict(json_string, result_dict)

        json_string = '{"key" : null}'
        result_dict = {"key": None}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_json_multi_types_returns_dict(self):
        json_string = '{\n\t"key": "value", \n\t"key2": 19, \n\t"key3": null, \n\t"key4": true, \n\t"key5": false}'
        result_dict = {"key": "value", "key2": 19, "key3": None, "key4": True, "key5": False}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_json_empty_array_value_returns_dict(self):
        json_string = '{"key": []}'
        result_dict = {"key": []}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_json_array_value_returns_dict(self):
        json_string = '{"key": ["value", 1, null, false]}'
        result_dict = {"key": ["value", 1, None, False]}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_json_empty_object_value_returns_dict(self):
        json_string = '{"key": {}}'
        result_dict = {"key":{}}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_json_object_value_returns_dict(self):
        json_string = '{"key": {"key1":"value"}}'
        result_dict = {"key":{"key1":"value"}}

        self._test_parse_json_returns_dict(json_string, result_dict)

    def test_parse_json_object_with_nested_structures_returns_dict(self):
        json_string = '''{
            "key1": "value",
            "key2": [
                {
                    "key2-1": [],
                    "key2-2": {
                        "key2-2-1": true
                    }
                },
                false,
                null
            ]
        }'''

        result_dict = {
            "key1": "value",
            "key2": [
                {
                    "key2-1": [],
                    "key2-2": {
                        "key2-2-1": True
                    }
                },
                False,
                None
            ]
        }

        self._test_parse_json_returns_dict(json_string, result_dict)

    def _test_parse_json_returns_dict(self, json_string, result_dict, debug=True):
        lexer = JLexer(json_string)
        tokens = lexer.get_tokens()

        if debug:
            print("Tokens: ", *tokens, sep="\n\t-")

        parser = JParser(tokens)

        parser.parse()
        result = parser.result

        self.assertDictEqual(result, result_dict)


if __name__ == "__main__":
    unittest.main()
