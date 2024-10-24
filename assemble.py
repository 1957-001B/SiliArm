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
    ORR = 0x00000
    B = 0x00101
    ADD = 0x00001


class Instruction:
    '''
    Each Instruction Has mnemonic, opcode, args,parsed
    '''
    mnemonic: str
    opcode: OpCode
    args: List[str]

    def __init__(self, instruction):
        self.instruction = instruction
        self.parsed = self.parse()

        if self.parse == [0, 0]:
            return 0

        self.mnemonic = self.parse()[0]
        self.opcode = self.get_opcode()
        self.args = []

    def parse(self):
        '''
        Parse the Instruction
        '''

        if self.instruction.split()[0] == ";":
            return [0, 0]

        else:
            self.mnemonic = self.instruction.split()[0]

            if len(self.instruction.split()) > 1:
                self.args = [arg.strip()
                             for arg in self.instruction.split()[1].split(',')]
            else:
                raise ValueError(f" Assembly Failed Unkown Instruction: '{
                                 self.instruction}' \n Did you provide Operands?")

            return self.mnemonic, self.args

    def get_opcode(self):
        '''
        Match the mnemonic with the opcode
        '''

        match self.mnemonic:
            case "ORR":
                return OpCode.ORR
            case "B":
                return OpCode.B
            case "ADD":
                return OpCode.ADD
            case _:
                raise Exception(
                    f" {self.mnemonic} is not a recognized mnemonic")

    def get_args(self): self.args
    def get_mnemonic(self): self.mnemonic


class Assembler:
    '''
    The Assembler
    '''

    def __init__(self, path) -> None:
        self.src = path
        self.instructions = self.get_instructions()

    def assemble(self):

        return 0

    def get_instructions(self):
        '''Obvious'''

        with self.src.open("+r", encoding="utf-8") as f:
            src = f.read().splitlines()
            instructions = []
            for line in src:
                l = vars(Instruction(line))
                print(l)
                instructions.append(l)
            return instructions

    def encode(self, type):
        '''
        Mnemonic --> Opcode (machine code)
        Args --> Operand (machine code)
        '''
        if self.current_mode == "OPCODE":

            match self.opcode:
                case OpCode.ORR:
                    encoded_string: str = OpCode.ORR.value + self.encoded_args

                case OpCode.B:
                    encoded_string: str = OpCode.B.value + self.encoded_args

                case OpCode.ADD:
                    encoded_string: str = OpCode.ADD.value + self.encoded_args

                case _:
                    raise Exception(
                        "This case is not possible, if it is. You are special")

        return 0


if __name__ == '__main__':
    path = Path("./example.s")
    Assembler(path)

# Tests


class AssemblerTests(unittest.TestCase):
    '''
    Unit tests for the assembler
    '''

    def test_parse(self):
        '''
        Simple sense check
        '''
        test_instruction1 = Instruction("MOV W1,W2")
        test_instruction2 = Instruction("JMP 0x89AB")

        self.assertEqual(test_instruction1.parsed, ('MOV', ['W1', 'W2']))
        self.assertEqual(test_instruction2.parsed, ('JMP', ['0x89AB']))
