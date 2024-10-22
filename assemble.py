'''
Simple Assembler For ARM64 on Apple Silicon
'''
from enum import Enum
from pathlib import Path
from typing import List
import unittest


class OpCode(Enum):
    '''
    Class to tidy up where Opcodes are defined
    '''
    MOV = 0x00
    JMP = 0x00


class Insruction:
    '''
    Each Instruction Has mnemonic
    '''
    mnemonic: str
    opcode: OpCode
    args: List[str]

    def __init__(self, instruction):
        self.instruction = instruction
        self.parsed = self.parse()
        self.opcode = self.get_opcode()

    def parse(self):
        '''
        Parse the Instruction
        '''
        self.mnemonic = self.instruction.split()[0]

        if len(self.instruction.split()) > 1:
            self.args = [arg.strip()
                         for arg in self.instruction.split()[1].split(',')]

        return self.mnemonic, self.args

    def get_opcode(self):
        '''
        Match the mnemonic with the opcode
        '''

        match self.mnemonic:
            case ["MOV"]:
                return OpCode.MOV
            case ["JMP"]:
                return OpCode.JMP

    def encode(self):
        '''
        Encode to machine code
        '''
        pass


# Testing
class AssemblerTests(unittest.TestCase):
    '''
    Unit tests for the assembler
    '''

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_parse(self):
        test_instruction1 = Insruction("MOV W1,W2")
        test_instruction2 = Insruction("JMP 0x89AB")

        self.assertEqual(test_instruction1.parsed, ('MOV', ['W1', 'W2']))
        self.assertEqual(test_instruction2.parsed, ('JMP', ['0x89AB']))


if __name__ == '__main__':
    unittest.main()
