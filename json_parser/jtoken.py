from enum import Enum, auto
from dataclasses import dataclass

class JTokenType(Enum):
    LEFT_BRACE              = auto()
    RIGHT_BRACE             = auto()
    LEFT_SQUARE_BRACKET     = auto()
    RIGHT_SQUARE_BRACKET    = auto()
    STRING                  = auto()
    NUMBER                  = auto()
    BOOL                    = auto()
    COLON                   = auto()
    COMMA                   = auto()
    EOF                     = auto()


@dataclass
class JToken:
    type: JTokenType
    lexeme: str
    literal: str | float | list
    line: int

    def __str__(self):
        return f"{self.type} [{self.literal}] at line {self.line}."
