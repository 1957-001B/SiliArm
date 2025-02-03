from enum import Enum


class OpCodes(Enum):
    # Base opcodes for 64-bit operations
    ORR_IMM = 0xB2400000  # ORR with immediate
    ORR_REG = 0xAA000000  # ORR with register
    ADD_IMM = 0x91000000  # ADD with immediate 
    ADD_REG = 0x8B000000  # ADD with register
    MOV_IMM = 0xD2800000  # MOV with immediate
    SVC = 0xD4000001
    B = 0x14000000

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
    SP = ("SP", 31)  # Stack pointer
    XZR = ("XZR", 31)  # Zero register (when used as source)

    @property
    def register_number(self):
        return self._value_
