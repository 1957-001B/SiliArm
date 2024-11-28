'''
Simple Assembler For ARM64 on Apple Silicon
'''
from enum import Enum
from pathlib import Path
from typing import List
import unittest


class OpCode(Enum):
    '''
    Class to tidy up where Opcodes are defined for 64-bit operations, first only essential opcodes will be implemented.
    '''
    ORR = 0xAA000000
    ADD = 0x8B000000
    SUB = 0xCB000000
    AND = 0x8A000000
    EOR = 0xCA000000
    LSL = 0x9AC02000
    LSR = 0x9AC02400
    MOV = 0xAA0003E0  # This is actually an alias for ORR Xd, XZR, Xm e.g ORR X0, XZR, #5  | ORR X1, XZR, X0 for register to register 
    B   = 0x14000000
    BL  = 0x94000000

class Registers(Enum):
    # 64-bit Registers
    X0 = 0
    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4
    X5 = 5
    X6 = 6
    X7 = 7
    X8 = 8
    X9 = 9
    X10 = 10
    X11 = 11
    X12 = 12
    X13 = 13
    X14 = 14
    X15 = 15
    X16 = 16
    X17 = 17
    X18 = 18
    X19 = 19
    X20 = 20
    X21 = 21
    X22 = 22
    X23 = 23
    X24 = 24
    X25 = 25
    X26 = 26
    X27 = 27
    X28 = 28
    X29 = 29  # Frame pointer
    X30 = 30  # Link register
    SP = 31   # Stack pointer
    XZR = 31  # Zero register (when used as source)

class OperationBitWidth(Enum):
    BIT_64 = 64

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
        self.mnemonic = self.parse()[0]
        self.opcode = self.get_opcode()
        self.args = []

    def parse(self):
        '''
        Parse the Instruction
        '''

        if self.instruction.split()[0] == ";":
            return None

        else:
            self.mnemonic = self.instruction.split()[0]

            if len(self.instruction.split()) > 1:
                self.args = [arg.strip()
                             for arg in self.instruction.split()[1].split(',')]
            else:
                raise ValueError(f" Assembly Failed: Unkown Instruction '{
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

    def to_bytecode(self, ) -> bytes:
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
