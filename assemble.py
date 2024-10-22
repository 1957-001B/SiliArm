from enum import Enum
from pathlib import Path
from typing import List
import unittest


class OpCode(Enum):
    MOV = 0x00
    JMP = 0x00


class Insruction:
    mnemonic: str
    opcode: OpCode
    args: List[str]

    def __init__(self, instruction):
        self.instruction = instruction
        self.parsed = self.parse()
        self.opcode = self.get_opcode()

    def parse(self):
        self.mnemonic = self.instruction.split()[0]

        if len(self.instruction.split()) > 1:
            self.args = [arg.strip()
                         for arg in self.instruction.split()[1].split(',')]

        return self.mnemonic, self.args

    def get_opcode(self):

        match self.mnemonic:
            case ["MOV"]:
                return OpCode.MOV
            case ["JMP"]:
                return OpCode.JMP

    def encode(self):
        pass


# Testing
class AssemblerTests(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.src = Path("./test.s")

    def test_parse(self):
        test_instruction1 = Insruction("MOV W1,W2")
        test_instruction2 = Insruction("JMP 0x89AB")

        self.assertEqual(test_instruction1.parsed, ('MOV', ['W1', 'W2']))
        self.assertEqual(test_instruction2.parsed, ('JMP', ['0x89AB']))


if __name__ == '__main__':
    unittest.main()
