from enum import Enum


class OpCodes(Enum):
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
    B = 0x14000000
    BL = 0x94000000


class Registers(Enum):

    def __new__(cls, *args):

        obj = object.__new__(cls)
        return obj

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
    SP = ("SP", 31) # Stack pointer
    XZR = ("XZR", 31) # Zero register (when used as source)

    @property
    def register_number(self):
        return self._value_
   
