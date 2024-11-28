from lexer import lex_file
from pathlib import Path


def assemble (filepath):
    lex_file(filepath)

assemble(Path("/Users/mivo/fun/SiliArm/example.s"))