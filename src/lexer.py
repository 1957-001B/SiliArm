from pathlib import Path
from enum import Enum
from ops import OpCodes
from ops import Registers


def lex_file(filepath):
    with filepath.open("+r", encoding="utf-8") as f:
            n=0
            src = f.read().splitlines()
            instructions = []
            for line in src:
                n+=1
                l = lex_line(line,n)
                instructions.append(l)

    return instructions
    


def lex_line(line, n):
        '''
        Parse the Instruction

        ADD ax, bx ; Add registers
        
        ('ADD', ['ax,', 'bx'])
        ------   ------------
        op       args

        '''

        if line.split() == ["EOF"]:
             return None 

        if not line.strip():
           return None 

        if line.split()[0] == ";":
            return None 

        else:
            tokens = [token.strip(',') for token in line.split(';')[0].strip().split()]
            line_code=[]
            for token in tokens:
                match token:

                    case token if token in OpCodes._member_names_:
                        op = ("INSTRUCTION", OpCodes[token])
                        line_code.append(op)

                    case Registers.XZR._name_:
                        print("yo")
                        reg = ("REGISTER", Registers.XZR)
                        line_code.append(reg)

                    case  Registers.SP._name_:
                        print("bro")
                        reg = ("REGISTER", Registers.SP)
                        line_code.append(reg)

                    case token if token in Registers._member_names_:
                        reg = ("REGISTER", Registers[token])
                        line_code.append(reg)

                    case _:
                        # this means its an argument or a typo 
                        pass

        print(line_code)
                