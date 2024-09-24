from enum import Enum

class ExitMessage(str, Enum):
    SUCCESS = "JSON parsed successfully."
    INVALID = "Invalid JSON."

class ExitCode(int, Enum):
    SUCCESS = 0
    INVALID = 1
    FAILURE = 2
