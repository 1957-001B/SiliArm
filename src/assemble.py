from pathlib import Path
from parser import Parser
from ops import OpCodes
import argparse
import os

debug = os.environ.get("DEBUG")

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("-o", "--output")


class Assembler:

    def __init__(self):
        self.args = parser.parse_args()
        self.src = Path(self.args.filename)
        self.out = Path(self.args.output)
        self.symbol_table = {}
        self.current_address = 0
        if debug:
            print(f"Running {self} with DEBUG=1")

    def write_macho_header(self, f, code_size):
        # Mach Header 64
        f.write(0xFEEDFACF.to_bytes(4, byteorder="little"))  # Magic
        f.write(0x0100000C.to_bytes(4, byteorder="little"))  # CPU Type (ARM64)
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # CPU Subtype
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # File Type (MH_OBJECT)
        f.write(
            0x00000004.to_bytes(4, byteorder="little")
        )  # Number of load commands (4)
        f.write(
            0x00000118.to_bytes(4, byteorder="little")
        )  # Size of load commands (280 bytes)
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # Flags
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # Reserved

        # LC_SEGMENT_64 command
        f.write(0x00000019.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000098.to_bytes(4, byteorder="little"))  # cmdsize (152 bytes)
        f.write(b"\x00" * 16)  # Empty segname
        f.write(0x0000000000000000.to_bytes(8, byteorder="little"))  # vmaddr
        f.write(code_size.to_bytes(8, byteorder="little"))  # vmsize
        f.write(0x0000000000000138.to_bytes(8, byteorder="little"))  # fileoff
        f.write(code_size.to_bytes(8, byteorder="little"))  # filesize
        f.write(0x00000007.to_bytes(4, byteorder="little"))  # maxprot
        f.write(0x00000007.to_bytes(4, byteorder="little"))  # initprot
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nsects
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # flags

        # Section header
        f.write(b"__text\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")  # sectname
        f.write(b"__TEXT\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")  # segname
        f.write(0x0000000000000000.to_bytes(8, byteorder="little"))  # addr
        f.write(code_size.to_bytes(8, byteorder="little"))  # size
        f.write(0x0000000000000138.to_bytes(4, byteorder="little"))  # offset
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # align (2^0)
        f.write(0x0000000000000168.to_bytes(4, byteorder="little"))  # reloff
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nreloc
        f.write(0x80000400.to_bytes(4, byteorder="little"))  # flags
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # reserved1
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # reserved2

        # LC_BUILD_VERSION command
        f.write(0x00000032.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # cmdsize (24 bytes)
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # platform (macOS)
        f.write(0x000F0000.to_bytes(4, byteorder="little"))  # minos (15.0)
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # sdk
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # ntools

        # LC_SYMTAB command
        f.write(0x00000002.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # cmdsize (24 bytes)
        f.write(0x0000000000000170.to_bytes(4, byteorder="little"))  # symoff
        f.write(0x00000004.to_bytes(4, byteorder="little"))  # nsyms
        f.write(0x00000000000001B0.to_bytes(4, byteorder="little"))  # stroff
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # strsize

        # LC_DYSYMTAB command
        f.write(0x0000000B.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # cmdsize (80 bytes)
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # ilocalsym
        f.write(0x00000002.to_bytes(4, byteorder="little"))  # nlocalsym
        f.write(0x00000002.to_bytes(4, byteorder="little"))  # iextdefsym
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nextdefsym
        f.write(0x00000003.to_bytes(4, byteorder="little"))  # iundefsym
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nundefsym
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # tocoff
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # ntoc
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # modtaboff
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # nmodtab
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # extrefsymoff
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # nextrefsyms
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # indirectsymoff
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # nindirectsyms
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # extreloff
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # nextrel
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # locreloff
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # nlocrel

        # Ensure text section is aligned
        f.seek(0x138)

    def first_pass(self):
        parser = Parser(self.src)
        parsed = parser.parse()

        for line in parsed:
            if "label" in line:
                label_name = line["label"]
                self.symbol_table[label_name] = self.current_address

            if "code" in line and any(
                token[0] == "INSTRUCTION" for token in line["code"]
            ):
                self.current_address += 4

        if debug:
            print(self.symbol_table)

    def second_pass(self):
        parser = Parser(self.src)
        parsed = parser.parse()
        current_address = 0
        output: list = []

        for line in parsed:
            if "code" not in line or not line["code"]:
                continue

            instruction = line["code"]
            if instruction[0][0] != "INSTRUCTION":
                continue

            opcode = instruction[0][1].value
            machine_code = None

            if opcode == OpCodes.B.value:
                if len(instruction) > 1:
                    if instruction[1][0] == "ADDRESS":
                        target = instruction[1][1]
                        offset = (target - current_address) // 4
                        machine_code = opcode | (offset & 0x3FFFFFF)
                    elif instruction[1][0] == "LABEL_REF":
                        target = self.symbol_table[instruction[1][1]]
                        offset = (target - current_address) // 4
                        machine_code = opcode | (offset & 0x3FFFFFF)

            elif opcode == OpCodes.SVC.value:
                if len(instruction) > 1 and instruction[1][0] == "IMMEDIATE":
                    imm = instruction[1][1] & 0xFFFF
                    machine_code = opcode | (imm << 5)

            elif opcode == OpCodes.MOV.value:
                if len(instruction) >= 2 and instruction[1][0] == "REGISTER":
                    dest_reg = (
                        instruction[1][1].value
                        if hasattr(instruction[1][1], "value")
                        else instruction[1][1]
                    )
                    if len(instruction) >= 3:
                        if instruction[2][0] == "IMMEDIATE":
                            imm = instruction[2][1] & 0xFFF
                            machine_code = opcode | dest_reg | (imm << 10)
                        elif instruction[2][0] == "REGISTER":
                            src_reg = (
                                instruction[2][1].value
                                if hasattr(instruction[2][1], "value")
                                else instruction[2][1]
                            )
                            machine_code = opcode | dest_reg | (src_reg << 16)

            elif opcode in [OpCodes.ADD.value, OpCodes.ORR.value]:
                if len(instruction) >= 2 and instruction[1][0] == "REGISTER":
                    dest_reg = (
                        instruction[1][1].value
                        if hasattr(instruction[1][1], "value")
                        else instruction[1][1]
                    )

                    if len(instruction) >= 3 and instruction[2][0] == "REGISTER":
                        src_reg = (
                            instruction[2][1].value[1]
                            if isinstance(instruction[2][1].value, tuple)
                            else instruction[2][1].value
                        )

                        if len(instruction) > 3:
                            if instruction[3][0] == "IMMEDIATE":
                                imm = instruction[3][1] & 0xFFF
                                machine_code = (
                                    opcode | dest_reg | (src_reg << 5) | (imm << 10)
                                )
                            elif instruction[3][0] == "REGISTER":
                                src_reg2 = (
                                    instruction[3][1].value
                                    if hasattr(instruction[3][1], "value")
                                    else instruction[3][1]
                                )
                                machine_code = (
                                    opcode
                                    | dest_reg
                                    | (src_reg << 5)
                                    | (src_reg2 << 16)
                                )
                        else:
                            machine_code = opcode | dest_reg | (src_reg << 5)

            if machine_code is not None:
                output.append(machine_code)
                current_address += 4

        with open(self.out, "wb") as f:
            code_size = len(output) * 4
            symtab_offset = self.write_macho_header(f, code_size)

            # Write machine code
            for code in output:
                f.write(code.to_bytes(4, byteorder="little"))

            # Write symbol table entries
            str_offset = 1  # Start at 1 to account for initial null byte
            str_offsets = {}
            string_table = bytearray(b"\x00")  # Start with null byte

            # First build string table and get offsets
            for symbol_name in self.symbol_table.keys():
                str_offsets[symbol_name] = len(string_table)
                string_table.extend(symbol_name.encode("utf-8") + b"\x00")

            # Write symbol table entries
            for symbol_name, value in self.symbol_table.items():
                f.write(
                    str_offsets[symbol_name].to_bytes(4, byteorder="little")
                )  # strx
                f.write(0x0F.to_bytes(1, byteorder="little"))  # type (N_SECT | N_EXT)
                f.write(0x1.to_bytes(1, byteorder="little"))  # sect
                f.write(0x0.to_bytes(2, byteorder="little"))  # desc
                f.write(value.to_bytes(8, byteorder="little"))  # value

            # Write string table
            f.write(string_table)

    def assemble(self):
        self.first_pass()
        self.second_pass()


x = Assembler()
x.assemble()
