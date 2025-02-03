# Oh these things are a headache

def write_macho_header(self, f, code_size):
        # Mach Header 64
        f.write(0xFEEDFACF.to_bytes(4, byteorder="little"))  # Magic
        f.write(0x0100000C.to_bytes(4, byteorder="little"))  # CPU Type (ARM64)
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # CPU Subtype
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # File Type (MH_OBJECT)
        f.write(0x00000004.to_bytes(4, byteorder="little"))  # Number of load commands
        f.write(0x00000118.to_bytes(4, byteorder="little"))  # Size of load commands
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # Flags
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # Reserved

        # LC_SEGMENT_64 command
        f.write(0x00000019.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000098.to_bytes(4, byteorder="little"))  # cmdsize
        f.write(b"\x00" * 16)  # segname
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
        f.write(0x00000138.to_bytes(4, byteorder="little"))  # offset
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # align
        f.write(0x00000168.to_bytes(4, byteorder="little"))  # reloff
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nreloc
        f.write(0x80000400.to_bytes(4, byteorder="little"))  # flags
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # reserved1
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # reserved2

        # LC_BUILD_VERSION command
        f.write(0x00000032.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # cmdsize
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # platform
        f.write(0x000F0000.to_bytes(4, byteorder="little"))  # minos (15.0)
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # sdk
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # ntools

        # LC_SYMTAB command
        f.write(0x00000002.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # cmdsize
        f.write(0x00000170.to_bytes(4, byteorder="little"))  # symoff
        f.write(0x00000004.to_bytes(4, byteorder="little"))  # nsyms
        f.write(0x000001B0.to_bytes(4, byteorder="little"))  # stroff
        f.write(0x00000018.to_bytes(4, byteorder="little"))  # strsize

        # LC_DYSYMTAB command
        f.write(0x0000000B.to_bytes(4, byteorder="little"))  # cmd
        f.write(0x00000050.to_bytes(4, byteorder="little"))  # cmdsize
        f.write(0x00000000.to_bytes(4, byteorder="little"))  # ilocalsym
        f.write(0x00000002.to_bytes(4, byteorder="little"))  # nlocalsym
        f.write(0x00000002.to_bytes(4, byteorder="little"))  # iextdefsym
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nextdefsym
        f.write(0x00000003.to_bytes(4, byteorder="little"))  # iundefsym
        f.write(0x00000001.to_bytes(4, byteorder="little"))  # nundefsym
        f.write(0x00000000.to_bytes(4, byteorder="little") * 12)  # remaining fields

        # Ensure text section is aligned
        f.seek(0x138)