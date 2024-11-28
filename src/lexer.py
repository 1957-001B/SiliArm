from pathlib import Path

def tokenize(filepath):
    with filepath.open("+r", encoding="utf-8") as f:
            n=0
            src = f.read().splitlines()
            instructions = []
            for line in src:
                print(line)
                n+=1
                l = parse(line,n)
                print(l)
                instructions.append(l)
            

def parse(line, n):
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
            op = tokens[0]
            args = tokens[1:]

        return op, args
