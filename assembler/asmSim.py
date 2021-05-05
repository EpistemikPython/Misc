##############################################################################################################################
# coding=utf-8
#
# assembler.py -- Assembler simulator program ported from ASMproj.pas
#                 - originally for CSI 1101-X,  Winter 1999; Assignment 8
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__       = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-02"
__updated__ = "2021-05-05"

import sys
import mhsLogging

base_filename = mhsLogging.get_base_filename(__file__)
log_control = mhsLogging.MhsLogger(base_filename)
lgr = log_control.get_logger()
info = lgr.info
dbg  = lgr.debug
show = log_control.show
lgr.warning("START LOGGING")

run_time = mhsLogging.run_ts

MAX_ID_SIZE = 4   	  # maximum length of identifiers (labels, etc.)
MAX_STATEMENTS = 400  # maximum number of statements in the assembly language program, not counting comments and empty lines

COMMENT_MARKERS = ['/', '#']

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
    show("create_opcode_table()")
    with open(OPCODE_FILE) as fp:
        for line in fp:
            codes = line.split()
            if len(codes) != 2:
                continue
            if codes[0].isalpha() and codes[1].isdecimal():
                dbg(F"mnemonic = {codes[0]} and opcode = {codes[1]}")
                opCodeTable[codes[0]] = codes[1]

    for key in opCodeTable.keys():
        dbg(F"{key}:{opCodeTable[key]}")

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
    show(F"run_sim({infile})")

    ct = 1
    address = 0

    # FIRST PASS: convert mnemonics, build symbol table
    # - need to process differently three types of input line:
    # (1) empty lines and comments
    # (2) lines whose mnemonic is 'BYTE'
    # (3) lines whose mnemonic is in the opcode table. *

    with open(infile) as fp:
        for line in fp:
            dbg(F"line #{ct} = {line}")
            mach_line = ""
            codes = line.split()
            line_len = len(codes)
            # skip blank line
            if line_len < 1:
                continue
            # skip over comment
            if codes[0][0] in COMMENT_MARKERS:
                continue
            if line_len <= 3:
                # LABEL X Y
                if line_len == 3:
                    symbolTable[codes[0]] = address
                    # LABEL BYTE VALUE
                    if codes[1] == "BYTE":
                        mach_line = codes[2]
                        address += 1
                    else:
                        # LABEL MNEMONIC OPERAND
                        mach_line = F"{opCodeTable[codes[1]]} {codes[2]}"
                        address += 3
                elif line_len == 2:
                    # BYTE VALUE
                    if codes[0] == "BYTE":
                        mach_line = codes[1]
                        address += 1
                    # MNEMONIC OPERAND
                    elif codes[0] in opCodeTable.keys():
                        mach_line = F"{opCodeTable[codes[0]]} {codes[1]}"
                        address += 3
                    # LABEL MNEMONIC
                    else:
                        symbolTable[codes[0]] = address
                        mach_line = opCodeTable[codes[1]]
                        address += 1
                # MNEMONIC
                elif line_len == 1:
                    mach_line = opCodeTable[codes[0]]
                    address += 1
                machineLang.append(mach_line)
                ct += 1

    info(F"processed {ct-1} ASM lines.")
    dbg("Symbol Table:")
    for key in symbolTable.keys():
        dbg(F"{key}:{symbolTable[key]}")
    dbg("Machine Language File:")
    for entry in machineLang:
        dbg(F"{entry}")

    # SECOND PASS:
    # look up symbolic operands in the Symbol Table
    # (unless the mnemonic is 'BYTE' - the operand for 'BYTE'
    # is not a symbol, it is an integer that is to be directly used)
    # and write out the machine language program line by line.	*

    base_infile = mhsLogging.get_base_filename(infile)
    outfile_name = "code/" + base_infile + "_" + mhsLogging.file_ts + ".code"
    show(F"outfile name = {outfile_name}")
    with open(outfile_name, 'w') as writer:
        writer.write(F"{COMMENT_MARKERS[1]} {base_filename}: run on {run_time} from file {infile}\n")
        for line in machineLang:
            newline = ""
            words = line.split()
            for word in words:
                dbg(F"check word = {word}")
                # find the labels in the symbol table
                if word in symbolTable.keys():
                    indx = machineLang.index(line)
                    token = symbolTable[word]
                    addr = str(token // 100) + " " + str(token % 100)
                    # replace the label with the address
                    newline = line.replace(word, addr)
                    machineLang.remove(line)
                    machineLang.insert(indx, newline)
                    writer.write(" " + newline + '\n')
            if not newline:
                writer.write(" " + line + '\n')

    dbg("Machine Language File:")
    for entry in machineLang:
        dbg(F"{entry}")


def main_asm_sim(fn:str):
    show(F"Program started: {run_time}")
    try:
        create_opcode_table()
        run_sim( fn )
    except Exception as ex:
        lgr.error(F"PROBLEM with program: {repr(ex)}")
        exit(202)


if __name__ == "__main__":
    if len( sys.argv ) > 1:
        main_asm_sim(sys.argv[1])
    else:
        lgr.warning("MISSING file name!")
    show("Program completed.")
    exit()
