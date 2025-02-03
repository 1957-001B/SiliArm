from pathlib import Path
from enum import Enum
from ops import OpCodes
from ops import Registers
import os

debug = os.environ.get("DEBUG")


class Parser:

    def __init__(self, src):
        self.src = src
        if debug:
            [print(item) for item in self.parse()]

    def parse(self):
        with self.src.open("+r", encoding="utf-8") as f:
            n = 0
            src = f.read().splitlines()
            parsed = []
            for line in src:
                n += 1
                l = self.parse_l(line, n)
                parsed.append(l)
            return [item for item in parsed if item is not None]

    def parse_l(self, line, n):
        """
        Parse the Instruction

        ADD ax, bx ; Add registers

        ('ADD', ['ax,', 'bx'])
        ------   ------------
        op       args

        """

        if line.split() == ["EOF"] or not line.strip() or line.split()[0] == ";":
            return None

        code_part = line.split(";")[0].strip()

        if ":" in code_part:
            label_name, rest = code_part.split(":", 1)
            label_name = label_name.strip()
            # If there's code after the label on same line
            if rest.strip():
                tokens = [token.strip(",") for token in rest.strip().split()]
                line_code = self.parse_tokens(tokens)
                return {"label": label_name, "code": line_code, "line_num": n}
            # Just a label by itself
            return {"label": label_name, "code": [], "line_num": n}

        # Regular line without label
        tokens = [token.strip(",") for token in code_part.split()]
        line_code = self.parse_tokens(tokens)
        return {"code": line_code, "line_num": n}

    def parse_tokens(self, tokens):
        """Helper method to parse tokens"""
        line_code = []
        for token in tokens:
            match token:
                case token if token in OpCodes._member_names_:
                    if token == "SVC":
                        line_code.append(("INSTRUCTION", OpCodes.SVC))
                    else:
                        line_code.append(("INSTRUCTION", OpCodes[token]))
                case Registers.XZR._name_:
                    line_code.append(("REGISTER", Registers.XZR))
                case Registers.SP._name_:
                    line_code.append(("REGISTER", Registers.SP))
                case token if token in Registers._member_names_:
                    line_code.append(("REGISTER", Registers[token]))
                case token if token.startswith("."):  # Label reference
                    line_code.append(("LABEL_REF", token[1:]))
                case token if token.startswith("0x"):  # Hex address for branches
                    try:
                        value = int(token, 16)
                        line_code.append(("ADDRESS", value))
                    except ValueError:
                        pass
                case token if token.startswith("#"):  # For SVC #0x80 or SVC #1
                    try:
                        if token.startswith("#0x"):  # Hex number
                            value = int(token[3:], 16)
                        else:  # Decimal number
                            value = int(token[1:])
                        line_code.append(("IMMEDIATE", value))  # Fixed indentation!
                    except ValueError:
                        pass
                case token if token.isdigit():  # Immediate values
                    value = int(token)
                    line_code.append(("IMMEDIATE", value))
                case _:
                    # Handle any other cases
                    pass
        return line_code
