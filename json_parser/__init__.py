from .jparser import JParser
from .jlexer import JLexer


def parse_json(json_string):
    tokens = JLexer(json_string)()
    parser = JParser(tokens)
    parser.parse()
    
    return parser.result


