from json_parser.extra.utils import ExitCode

class JParserExceptionWithExitCode(Exception):
    def get_exit_code(self):
        return ExitCode.INVALID

class InvalidJsonException(JParserExceptionWithExitCode):
    pass

class InvalidTokenException(JParserExceptionWithExitCode):
    pass

class LexerError(JParserExceptionWithExitCode):
    pass

class ParserError(JParserExceptionWithExitCode):
    pass
