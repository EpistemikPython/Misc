##############################################################################################################################
# coding=utf-8
#
# assembler.py -- Assembler simulator program ported from ASMproj.pas
#                 - originally for CSI 1101-X,  Winter, 1999; Assignment 8
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__       = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-02"
__updated__ = "2021-05-04"

import sys
import mhsLogging

log_control = mhsLogging.MhsLogger(mhsLogging.get_base_filename(__file__))
asmsim_lgr = log_control.get_logger()
show = log_control.show
asmsim_lgr.warning("START LOGGING")

MAX_ID_SIZE = 4   	  # maximum length of identifiers (labels, etc.)
MAX_STATEMENTS = 400  # maximum number of statements in the assembly language program, not counting comments and empty lines
OPCODE_FILE = "data/Opcodes.data"

opCodeTable = dict()
symbolTable = dict()
machineLang = list()


# create_opcode_table - reads "opcode_table" from the file whose DOS/Windows name
# is 'opcodes.dat'.  Each line of opcodes.dat contains:  a mnemonic (string of maxIDsize
# or fewer non-blank characters) starting in column 1, followed by one or more blanks,
# followed by the integer opcode corresponding to the mnemonic.
def create_opcode_table():
    """load the mnemonic:opCode entries from file"""
    with open(OPCODE_FILE) as fp:
        for line in fp:
            codes = line.split()
            if len(codes) is not 2:
                continue
            if codes[0].isalpha() and codes[1].isdecimal():
                opCodeTable[codes[0]] = codes[1]


# read_asm_line - reads the next line of input (keyboard), and extracts from
# the input line values for "labl", "mnemonic", and "operand".
# Each input line is assumed to be an empty line or a correctly formatted line
# of an assembly language program.  You are NOT REQUIRED to do any input checking.
# If the input line is empty, or is a comment ('/' in column 1), "labl",
# "mnemonic", and "operand" are all set to be the empty string ('').
# If there is a blank (' ') in column 1, "labl" is set to the empty string
# otherwise "labl" is set to contain the sequence of non-blank characters
# starting in column 1 up to (but not including) the first blank.
# "mnemonic" is set to be the first sequence of non-blank characters beginning
# after the first blank on the line.
# "operand" is set to be the first sequence of non-blank characters beginning
# after the first blank after the end of "mnemonic".  If there is no non-blank
# character after the end of "mnemonic", "operand" is set to the empty string ('').
# NOTE: "label" is a keyword in Pascal, so it cannot be used as a variable name.

# assemble - This def reads an assembly language program and writes out the
# corresponding machine language program.  For each non-empty, non-comment line of
# assembly language there must be one line of output containing its machine language
# equivalent.  The machine language produced should be in a format that can be read by
# the simulator program (a8sim.pas).
#
# You must follow the two-pass algorithm shown in class.
#
# The main task of the first pass is to create a "symbol table"
# - this is a list that contains:
#     - the symbolic statement labels that have occurred in the
#       assembly language program,
# and, for each label,
#     - the numerical memory address that corresponds to that label
#       (assuming the program starts at location 0).
#
# Conversion of each symbolic mnemonic to the corresponding numerical opcode (by
# looking it up in the opcode table) can be done in the first pass (as in class)
# or on the second pass.  The first pass does nothing with the symbolic operands
# in the assembly language program.  The main task of the second pass is to
# convert these to addresses by looking them up in the symbol table. The second
# pass also prints out the machine language program line by line.


def run_sim(infile:str):
    create_opcode_table()

    lines = 0

    # FIRST PASS: convert mnemonics, build symbol table
    # - need to process differently three types of input line:
    # (1) empty lines and comments
    # (2) lines whose mnemonic is 'BYTE'
    # (3) lines whose mnemonic is in the opcode table. *

    with open(infile) as fp:
        for line in fp:
            codes = line.split()
            line_len = len(codes)
            if line_len == 3:
                continue
            if line_len == 2:
                continue
            if line_len == 1:
                continue
            if codes[0].isalpha() and codes[1].isdecimal():
                opCodeTable[codes[0]] = codes[1]
            lines += 1

    # SECOND PASS:
    # look up symbolic operands in the Symbol Table
    # (unless the mnemonic is 'BYTE' - the operand for 'BYTE'
    # is not a symbol, it is an integer that is to be directly used)
    # and write out the machine language program line by line.	*


def main_cpu_sim(fn:str):
    show("Program started: " + mhsLogging.run_ts)
    try:
        run_sim(fn)
    except Exception as ex:
        asmsim_lgr.error("PROBLEM with program: " + repr(ex))
        exit(256)


if __name__ == "__main__":
    if len( sys.argv ) > 1:
        main_cpu_sim(sys.argv[1])
    else:
        show("MISSING file name!")
    show("Program completed.")
    exit()
