import unittest
from pathlib import Path

from parser import parse
from parser import tokenize


class LexerTests(unittest.TestCase):
    """
    Unit tests for the assembler
    """

    def test_parse_typical(self):

        # Good inputs
        assert parse("MOV ax, bx", 1) == ("MOV", ["ax", "bx"])
        assert parse("PUSH ax", 1) == ("PUSH", ["ax"])
        assert parse("; This is a comment", 1) == None
        assert parse("ADD ax, bx ; Add registers", 1) == ("ADD", ["ax", "bx"])

    def test_parse_edge(self):
        # Bad inputs that will raise errors
        try:
            parse("", 1)  # Empty line
            parse("MOV", 1)  # Missing arguments
        except ValueError as e:
            print(f"Error: {e}")

    def test_full(self):

        assert (
            tokenize(Path("../example.s")) == Path("../example.s.tokenized").read_text()
        )
