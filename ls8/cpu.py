"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                #print(v)
                self.ram[address] = v
                address += 1


        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, mar):
        return self.reg[mar] 

    def ram_write(self, mar, mdr): 
        self.reg[mar] = mdr

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        halted = False
        while not halted: 
            instruction = self.ram[self.pc]
            
            if instruction == 0b10000010:
                mar = self.ram[self.pc + 1]
                mdr = self.ram[self.pc + 2]

                self.ram_write(mar, mdr)
                
                self.pc += 3
            elif instruction == 0b01000111:
                mar = self.ram[self.pc + 1]
                value = self.ram_read(mar)
                
                print(value)
                
                self.pc += 2
            elif instruction == 0b10100010:
                
                reg_a = self.ram[self.pc+1]
                reg_b = self.ram[self.pc+2]
                value = self.alu("MUL", reg_a, reg_b)

                self.pc += 3

            elif instruction == 0b00000001:
                halted = True
            else:
                print(f'unknown instruction {instruction} at address {self.pc}')
                sys.exit(1)