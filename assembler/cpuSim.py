##############################################################################################################################
# coding=utf-8
#
# cpuSim.py -- CPU simulator program ported from Pascal source code
#              - originally for CSI 1101,  Winter 1999, Assignment 8
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__       = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-02"
__updated__ = "2023-11-03"

from sys import argv, path
path.append("/home/marksa/git/Python/utils")
from mhsUtils import get_base_filename, get_current_time
from mhsLogging import MhsLogger

log_control = MhsLogger(get_base_filename(__file__))
lgr = log_control.get_logger()
info = lgr.info
dbg  = lgr.debug
show = log_control.show
lgr.warning("START LOGGING")

# the following constants give symbolic names for the opcodes
LDA = 91    # Load Accumulator from memory
STA = 39    # Store Accumulator into memory
CLA =  8    # Clear (set to zero) the Accumulator
INC = 10    # Increment (add 1 to) the Accumulator
ADD = 99    # Add to Accumulator
SUB = 61    # Subtract from Accumulator
JMP = 15    # Jump ("go to")
JZ  = 17    # Jump if the Zero status bit is True
JN  = 19    # Jump if the Negative status bit is True
DSP =  1    # Display (write on the screen)
HLT = 64    # Halt

COMMENT_MARKERS = ['/', '#']

class Byte:
    """ -99..99 """
    def __init__(self, val=0):
        self.value:int = val

    MIN_VALUE:int = -99
    MAX_VALUE:int = 99

    def set(self, val:int):
        if val < self.MIN_VALUE:
            # get the expected value from mod of negative number
            self.value = ((val * -1) % 100) * -1
        elif val >= self.MAX_VALUE:
            self.value = val % 100
        else:
            self.value = val

    def get(self) -> int:
        return self.value

class Word:
    """ 0000..9999 """
    def __init__(self, val=0):
        self.value:int = val

    MIN_VALUE:int = 0
    MAX_VALUE:int = 9999

    def set(self, val:int):
        if self.MIN_VALUE <= val <= self.MAX_VALUE:
            self.value = val
        else:
            lgr.warning(F"ILLEGAL parameter '{val}' NOT between {self.MIN_VALUE} and {self.MAX_VALUE}!")

    def get(self) -> int:
        return self.value

    def inc(self):
        if self.value < self.MAX_VALUE:
            self.value += 1
        else:
            lgr.warning(F"ILLEGAL Increment attempt! ALREADY at Max value = {self.MAX_VALUE}!")


memory = dict() # array[word] of byte

# the following are the registers in the CPU
pc  = Word()     # word   # program counter
acc = Byte()     # byte   # accumulator
opCode = Byte()  # byte   # the opcode of the current instruction
opAddr = Word()  # word   # the memory address of the operand of the current instruction
z = False        # bit    # "Zero" status bit
n = False        # bit    # "Negative" status bit
h = False        # bit    # "Halt" status bit

mar = Word()  # word   # Memory Address register
mdr = Byte()  # byte   # Memory Data    register
READ = True
WRITE = False
rw = True     # bit    # Read/Write bit.  Read = True ; Write = False

def load(filename):
    """Load a machine language program into memory"""
    show(F"load({filename})")
    address = Word()
    with open(filename) as fp:
        ct = 0
        for line in fp:
            ct += 1
            codes = line.split()
            # skip blank line
            if len(codes) < 1:
                continue
            # skip over comment
            if codes[0].isalpha() or codes[0] in COMMENT_MARKERS:
                continue
            for item in codes:
                memory[address.get()] = Byte( int(item) )
                info(F"load item {item} at address {address.get()}")
                address.inc()

def check_memory():
    for key in reversed( memory.keys() ):
        dbg(F"m[{key}]={memory[key].get()} ", '|')
    dbg("===")

def access_memory():
    info(F"rw = {rw}")
    if rw: # True = read = copy a value from memory into the CPU
        mdr.set( (memory[mar.get()]).get() )
        dbg(F"now mdr = {mdr.get()}")
    else: # False = write = copy a value into memory from the CPU
        memory[mar.get()] = Byte( mdr.get() )
        dbg(F"now memory[{mar.get()}] = {(memory[mar.get()]).get()}")

def run_sim():
    """ implements the Fetch-Execute cycle """
    show("run_sim()")
    pc.set(0)   # always start execution at location 0
    global rw
    global h
    h = False   # reset the Halt status bit
    global z
    global n
    # repeat
    while not h:
        dbg("FETCH OPCODE")
        mar.set( pc.get() )
        pc.inc()  # pc is incremented immediately
        rw = READ
        access_memory()
        opCode.set( mdr.get() )

        opcode = opCode.get()
        # If the opcode is odd, it needs operands
        if opcode % 2 == 1:
            dbg("FETCH THE ADDRESS OF THE OPERAND")
            mar.set( pc.get() )
            pc.inc() # pc is incremented immediately
            rw = READ
            access_memory()
            opAddr.set( mdr.get() ) # this is just the HIGH byte of the opAddr
            mar.set( pc.get() )
            pc.inc() # pc is incremented immediately
            rw = READ
            access_memory() # this gets the LOW byte
            opAddr.set( (100 * opAddr.get()) + mdr.get() ) # put the two bytes together
            info(F"Operand Address = {opAddr.get()}")

        # EXECUTE THE OPERATION
        if opcode == LDA: # Get the Operand"s value from memory
            show("LDA")
            mar.set( opAddr.get() )
            rw = READ
            access_memory()
            acc.set( mdr.get() ) # and store it in the Accumulator
            dbg(F"now Accumulator value = {acc.get()}")

        elif opcode == STA: # Store the Accumulator
            show("STA")
            mdr.set( acc.get() )
            mar.set( opAddr.get() ) # into the Operand's address
            rw = WRITE
            access_memory()

        elif opcode == CLA: # Clear = set the Accumulator to zero
            show("CLA")
            acc.set( 0 )
            dbg(F"now Accumulator value = {acc.get()}")
            z = True  # set the Status Bits appropriately
            n = False

        elif opcode == INC: # Increment = add 1 to the Accumulator
            show("INC")
            acc.set( acc.get() + 1 )
            dbg(F"now Accumulator value = {acc.get()}")
            z = ( acc.get() == 0 ) # set the Status Bits appropriately
            n = ( acc.get() < 0 )

        elif opcode == ADD:
            show("ADD")
            mar.set( opAddr.get() ) # Get the Operand's value from memory
            rw = READ
            access_memory()
            acc.set( acc.get() + mdr.get() ) # and add it to the Accumulator
            dbg(F"now Accumulator value = {acc.get()}")
            z = ( acc.get() == 0 ) # set the Status Bits appropriately
            n = ( acc.get() < 0 )

        elif opcode == SUB:
            show("SUB")
            mar.set( opAddr.get() ) # Get the Operand's value from memory
            rw  = READ
            access_memory()
            acc.set( acc.get() - mdr.get() ) # and subtract it from the Accumulator
            dbg(F"now Accumulator value = {acc.get()}")
            z = ( acc.get() == 0 ) # set the Status Bits appropriately
            n = ( acc.get() < 0 )

        elif opcode == JMP:
            show("JMP")
            pc.set( opAddr.get() ) # opAddr is the address of the next instruction to execute

        elif opcode == JZ:
            show("JZ")
            if z:
                pc.set( opAddr.get() ) # Jump if the Z status bit is True

        elif opcode == JN:
            show("JN")
            if n:
                pc.set( opAddr.get() ) # Jump if the N status bit is True

        elif opcode == HLT:
            show("HLT")
            h = True  # set the Halt status bit

        elif opcode == DSP:
            info("DSP")
            mar.set( opAddr.get() ) # Get the Operand's value from memory
            rw = READ
            access_memory()
            show(F"memory location {mar.get()} contains the value {mdr.get()}")

def main_cpu_sim(filename:str):
    show(F"Program started: {get_current_time()}")
    try:
        load( filename )
        run_sim()
    except Exception as ex:
        lgr.error(F"PROBLEM with program: {repr(ex)}")
        exit(66)


if __name__ == "__main__":
    if len(argv) > 1:
        main_cpu_sim(argv[1])
    else:
        lgr.warning("MISSING file name!")
    show("Program completed.")
    exit()
