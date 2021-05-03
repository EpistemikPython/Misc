##############################################################################################################################
# coding=utf-8
#
# py -- CPU simulator program ported from pas
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__       = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-02"
__updated__ = "2021-05-03"

import sys

# **  CSI 1101,  Winter, 1999  **
# ** Assignment 8, Simulator program **

# the following constants give symbolic names for the opcodes
LDA = 91    # Load  Accumulator from memory
STA = 39    # Store Accumulator into memory
CLA =  8    # Clear (set to zero)  the Accumulator
INC = 10    # Increment (add 1 to) the Accumulator
ADD = 99    # Add to Accumulator
SUB = 61    # Subtract from Accumulator
JMP = 15    # Jump ("go to")
JZ  = 17    # Jump if the Zero status bit is True
JN  = 19    # Jump if the Negative status bit is True
DSP =  1    # Display (write on the screen)
HLT = 64    # Halt


COMMENT_MARKER = '/'

class Byte:
    def __init__(self, val=0):
        self.value:int = val
    # = -99..99
    MIN_VALUE:int = -99
    MAX_VALUE:int = 99

    def set(self, val:int):
        if self.MIN_VALUE <= val <= self.MAX_VALUE:
            self.value = val
        else:
            print(F"ILLEGAL parameter '{val}' NOT between {self.MIN_VALUE} and {self.MAX_VALUE}!")

    def get(self) -> int:
        return self.value


class Word:
    def __init__(self, val=0):
        self.value:int = val
    # = 0000..9999
    MIN_VALUE:int = 0
    MAX_VALUE:int = 9999

    def set(self, val:int):
        if self.MIN_VALUE <= val <= self.MAX_VALUE:
            self.value = val
        else:
            print(F"ILLEGAL parameter '{val}' NOT between {self.MIN_VALUE} and {self.MAX_VALUE}!")

    def get(self) -> int:
        return self.value

    def inc(self):
        if self.value < self.MAX_VALUE:
            self.value = self.value + 1
        else:
            print(F"ILLEGAL Increment attempt! ALREADY at Max value = {self.MAX_VALUE}!")


memory = dict() # array[word] of byte

# the following are the registers in the CPU
pc  = Word()     # word   # program counter
acc = Byte()     # byte   # accumulator
opCode = Byte()  # byte   # the opcode of the current instruction
opAddr = Word()  # word   # the ADDRESS of the operand of the current instruction
z = False        # bit    # "Zero" status bit
n = False        # bit    # "Negative" status bit
h = False        # bit    # "Halt" status bit

mar = Word()  # word   # Memory Address register
mdr = Byte()  # byte   # Memory Data    register
READ = True
WRITE = False
rw = True    # bit    # Read/Write bit.  Read = True ; Write = False


def load(filename):
    """Load a machine language program into memory"""
    address = Word()
    with open(filename) as fp:
        ct = 0
        for line in fp:
            ct += 1
            codes = line.split()
            if len(codes) < 1:
                continue
            if codes[0].isalpha() or codes[0] == COMMENT_MARKER:
                continue # skip over comment
            for item in codes:
                memory[address.get()] = Byte( int(item) )
                print(F"load item {item} at address {address.get()}")
                address.inc()
    # while not EOF:
    #     if not eoln:
    #         read(first_character)
    #         if first_character != ' ':   # non-blank indicates a comment
    #             repeat                 # skip over comment
    #                 read(ch)
    #             until ch = first_character
    #             while not eoln:
    #                 read(memory[address])
    #                 address = address + 1
    #     readln


def check_memory():
    for key in reversed( memory.keys() ):
        print(F"m[{key}]={memory[key].get()} ", end = '|')
    print("===")


def access_memory():
    print("access memory")
    if rw: # True = read = copy a value from memory into the CPU
        mdr.set( (memory[mar.get()]).get() )
        print(F"now mdr = {mdr.get()}")
    else: # False = write = copy a value into memory from the CPU
        memory[mar.get()] = Byte( mdr.get() )
        print(F"now memory[{mar.get()}] = {(memory[mar.get()]).get()}")


def run_sim():  # This implements the Fetch-Execute cycle
    pc.set(0)   # always start execution at location 0
    global rw
    global h
    h = False   # reset the Halt status bit
    global z
    global n
    # repeat
    while not h:
        print("FETCH OPCODE")
        mar.set( pc.get() )
        pc.inc()  # = pc + 1   # NOTE that pc is incremented immediately
        rw = READ
        access_memory()
        opCode.set( mdr.get() )

        opcode = opCode.get()
        # If the opcode is odd, it needs an operand.
        if opcode % 2 == 1:
            print("FETCH THE ADDRESS OF THE OPERAND")
            mar.set( pc.get() )
            pc.inc() # = pc + 1   # NOTE that pc is incremented immediately
            rw = READ
            access_memory()
            opAddr.set( mdr.get() ) # this is just the HIGH byte of the opAddr
            mar.set( pc.get() )
            pc.inc() # = pc + 1   # NOTE that pc is incremented immediately
            rw = READ
            access_memory()    # this gets the LOW byte
            opAddr.set( (100 * opAddr.get()) + mdr.get() )  # put the two bytes together
            print(F"Operand Address = {opAddr.get()}")

        # EXECUTE THE OPERATION
        if opcode == LDA: # Get the Operand"s value from memory
            print("LDA")
            mar.set( opAddr.get() )
            rw = READ
            access_memory()
            acc.set( mdr.get() )  # and store it in the Accumulator
            print(F"now Accumulator value = {acc.get()}")

        elif opcode == STA: # Store the Accumulator
            print("STA")
            mdr.set( acc.get() )
            mar.set( opAddr.get() )   # into the Operand's address
            rw = WRITE
            access_memory()

        elif opcode == CLA: # Clear = set the Accumulator to zero
            print("CLA")
            acc.set( 0 )
            print(F"now Accumulator value = {acc.get()}")
            z = True       # set the Status Bits appropriately
            n = False

        elif opcode == INC: # Increment = add 1 to the Accumulator
            print("INC")
            acc.set( (acc.get()+1) % 100 )
            print(F"now Accumulator value = {acc.get()}")
            z = (acc.get() == 0)   # set the Status Bits appropriately
            n = (acc.get() < 0)

        elif opcode == ADD:
            print("ADD")
            mar.set( opAddr.get() )    # Get the Operand's value from memory
            rw = READ
            access_memory()
            acc.set( (acc.get() + mdr.get()) % 100 ) # and add it to the Accumulator
            print(F"now Accumulator value = {acc.get()}")
            z = (acc.get() == 0)   # set the Status Bits appropriately
            n = (acc.get() < 0)

        elif opcode == SUB:
            print("SUB")
            mar.set( opAddr.get() )    # Get the Operand's value from memory
            rw  = READ
            access_memory()
            acc.set( (acc.get() - mdr.get()) % 100 ) # and subtract it from the Accumulator
            print(F"now Accumulator value = {acc.get()}")
            z = (acc.get() == 0)   # set the Status Bits appropriately
            n = (acc.get() < 0)

        elif opcode == JMP:
            print("JMP")
            pc.set( opAddr.get() )  # opAddr is the address of the next instruction to execute

        elif opcode == JZ :
            print("JZ")
            if z :
                pc.set( opAddr.get() ) # Jump if the Z status bit is True

        elif opcode == JN :
            print("JN")
            if n :
                pc.set( opAddr.get() ) # Jump if the N status bit is True

        elif opcode == HLT:
            print("HLT")
            h = True  # set the Halt status bit

        elif opcode == DSP:
            print("DSP")
            mar.set( opAddr.get() )   # Get the Operand's value from memory
            rw = READ
            access_memory()
            print(F"memory location {mar.get()} contains the value {mdr.get()}")


def main_sim(fn:str):
    try:
        load( fn )
        run_sim()
    except Exception as ex:
        print("PROBLEM with program: " + repr(ex))
        exit(222)


if __name__ == "__main__":
    if len( sys.argv ) > 1:
        main_sim( sys.argv[1] )
    else:
        print("MISSING file name!")
    print("Program completed.")
    exit()
