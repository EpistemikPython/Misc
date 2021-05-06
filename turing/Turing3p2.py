##############################################################################################################################
# coding=utf-8
#
# Turing3p2.py -- Turing machine simulator program ported from Turing3_2.java
#
#   Python implementation of the Turing machine described in "On Computable Numbers (1936)", section 3.II,
#   which generates a sequence of 0's each followed by an increasing number of 1's, from 0 to infinity,
#   i.e. 001011011101111011111...
#   Also see <i>The Annotated Turing</i> by <b>Charles Petzold</b> Chapter 5, pp.85-94.
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-05"
__updated__ = "2021-05-06"

import sys
import time
from argparse import ArgumentParser
import mhsLogging

base_filename = mhsLogging.get_base_filename(__file__)
log_control = mhsLogging.MhsLogger(base_filename)
lgr = log_control.get_logger()
info = lgr.info
dbg = lgr.debug
show = log_control.show
lgr.warning("START LOGGING")

run_time = mhsLogging.run_ts

# number of 'squares' available on the 'tape'
DEFAULT_TAPE_SIZE = 256
# MAXIMUM number of 'squares' available on the 'tape'
MAX_TAPE_SIZE = 1024 * 16
# MINIMUM number of 'squares' available on the 'tape'
MIN_TAPE_SIZE = 16

# if displaying each step of the algorithm, DEFAULT delay (in msec) between each step
DEFAULT_DELAY_MSEC = 2000.0
# if displaying each step of the algorithm, MINIMUM delay (in msec) between each step
MIN_DELAY_MSEC = 5.0
# if displaying each step of the algorithm, MAXIMUM delay (in msec) between each step
MAX_DELAY_MSEC = 60.0 * 1000.0

# tape symbols
nBLANK = ''
nZERO  = '0'
nONE   = '1'
nX     = 'x'
nSCHWA = '@'

# machine state
STATE_BEGIN   = 0
STATE_PRINT_X = 1
STATE_ERASE_X = 2
STATE_PRINT_0 = 3
STATE_PRINT_1 = 4

# state names for display -- order MUST MATCH the values for the machine state ints
STR_STATES = ["STATE_BEGIN", "STATE_PRINT_X", "STATE_ERASE_X", "STATE_PRINT_0", "STATE_PRINT_1"]


class Turing3p2:
    """ Python implementation of the Turing machine described in "On Computable Numbers (1936)", section 3.II """
    def __init__(self, p_size=DEFAULT_TAPE_SIZE, p_pause=DEFAULT_DELAY_MSEC, p_newline=True, p_show=False):
        # use an array as a substitute for the <em>infinite</em> tape
        self.tape = dict()
        # size of the 'tape'
        self.tape_size = p_size

        global nBLANK
        # determine whether each step is displayed
        self.show_steps = p_show
        if p_show:
            nBLANK = '-' # for easier visualization
        # prepare the empty tape
        for r in range(self.tape_size):
            self.tape[str(r)] = nBLANK

        # delay, in seconds, between each step display
        self.step_delay = p_pause / 1000.0

        # start each zero on a new line
        self.show_newline = p_newline

        # current state of the machine
        self.state = STATE_BEGIN
        # current position on the 'tape'
        self.position = 0

    # run the algorithm:
    # - check the current state
    # - check the current position on the 'tape'
    # - create or erase a symbol if necessary
    # - move to a different position on the 'tape' if necessary
    # - set the next state
    def generate(self):
        step = 0
        dbg( F"Size of tape array = {str(len(self.tape.keys()))}")
        dbg( F"Step pause = {str(self.step_delay)} sec" )

        # initial state
        self.begin()
        # we don't have an infinite tape -- continue until we move past the end of the array
        while self.position < self.tape_size:
            step += 1
            current_symbol = self.tape[str(self.position)]
            show(F"current position = {self.position}; current symbol = {current_symbol}")

            if self.show_steps:
                self.show_step(step)

            if self.state == STATE_PRINT_X:
                show("STATE_PRINT_X")
                if current_symbol == nONE:
                    self.move_right()
                    self.set(nX)
                    self.move_left(3)

                elif current_symbol == nZERO:
                    self.state = STATE_PRINT_1

            elif self.state == STATE_ERASE_X:
                show("STATE_ERASE_X")
                if current_symbol == nX:
                    self.erase()
                    self.move_right()
                    self.state = STATE_PRINT_1

                elif current_symbol == nSCHWA:
                    self.move_right()
                    self.state = STATE_PRINT_0

                elif current_symbol == nBLANK:
                    self.move_left(2)

            elif self.state == STATE_PRINT_0:
                show("STATE_PRINT_0")
                if current_symbol == nBLANK:
                    self.set(nZERO)
                    self.move_left(2)
                    self.state = STATE_PRINT_X
                else:
                    self.move_right(2)

            elif self.state == STATE_PRINT_1:
                show("STATE_PRINT_1")
                if current_symbol == nBLANK:
                    self.set(nONE)
                    self.move_left()
                    self.state = STATE_ERASE_X
                else:
                    # current symbol == nZERO or nONE
                    self.move_right(2)

            else:
                raise Exception(F">>> UNKNOWN current state = {str(self.state)}?!")

        self.end()

    # the actions at the INITIAL STATE of the algorithm -- NEVER return to this state again
    def begin(self):
        if self.state != STATE_BEGIN:
            return

        show("STATE_BEGIN")
        if self.show_steps:
            self.show_step(0)

        self.set(nSCHWA)
        self.move_right()
        self.set(nSCHWA)
        self.move_right()

        self.set(nZERO)
        self.move_right(2)
        self.set(nZERO)
        self.move_left(2)
        self.state = STATE_PRINT_X

    # SET the specified symbol on the tape at the current position
    def set(self, sym:str):
        self.tape[str(self.position)] = sym

    # ERASE the symbol at the current position
    def erase(self):
        self.tape[str(self.position)] = nBLANK

    # MOVE RIGHT by the specified number of squares - not in Turing's description but more convenient
    def move_right(self, count:int = 1):
        self.position += count
        # END PROGRAM when position moves beyond the end of the tape
        if self.position >= self.tape_size:
            info("\nReached position # " + str(self.position) + " >> ENDING PROGRAM.")

    # MOVE LEFT by the specified number of squares - not in Turing's description but more convenient
    def move_left(self, count:int = 1):
        self.position -= count
        # return to 0 if move before the beginning of the tape -- SHOULD NEVER HAPPEN
        if self.position < 0:
            lgr.warning("Position: [" + str(self.position) + "] is less than 0 !")
            self.position = 0

    # DISPLAY the entire sequence of symbols on the tape, then exit
    def end(self):
        if not self.show_steps:
            self.printTape()
        show("\n == DONE ==")

    # DISPLAY the current sequence of symbols on the tape
    def printTape(self):
        for posn in self.tape.keys():
            if self.tape[posn] == nZERO and self.show_newline:
                show("")
            show(self.tape[posn], endl = '')
        show("E")

    # DISPLAY the position and machine state at a particular point in the program
    def show_step(self, step:int):
        show("Step #" + str(step) + " - State = " + STR_STATES[self.state] +
             " - Position is " + str(self.position) + "[" + self.tape[str(self.position)] + "]" , endl = '')
        self.printTape()
        # pause to allow easier inspection of each step
        try:
            time.sleep(self.step_delay) # seconds
        except Exception as ex:
            raise Exception( repr(ex) )

# END class Turing3p2


def process_args():
    arg_desc = "Java implementation of the Turing machine described in 'On Computable Numbers' (1936), section 3.II,\n " \
               "which generates a sequence of 0's followed by an increasing number of 1's, from 0 to infinity,\n " \
               "i.e. 001011011101111011111... \n"

    arg_parser = ArgumentParser(description = arg_desc, prog = "Turing3p2.py")
    # optional arguments
    arg_parser.add_argument('-d', "--describe", action = "store_true", help = "describe EACH algorithm step")
    arg_parser.add_argument('-s', "--size", type = int, default = DEFAULT_TAPE_SIZE,
                            help = F"number of tape 'slots' ({MIN_TAPE_SIZE}..{MAX_TAPE_SIZE})")
    arg_parser.add_argument('-p', "--pause", type = float, default = DEFAULT_DELAY_MSEC,
                            help = F"time to pause between each algorithm step, in msec ({MIN_DELAY_MSEC}..{MAX_DELAY_MSEC})")
    arg_parser.add_argument('-n', "--newline", action = "store_true", help = "each zero in the output starts on a new line")
    arg_parser.add_argument('-x', "--example", action = "store_true", help = "run a nice example [-n -s602]")

    return arg_parser


def process_input_parameters(argx: list):
    args = process_args().parse_args(argx)
    dbg(F"\n\targs = {args}")

    if args.example:
        newline = True
        size = 602
        pause = DEFAULT_DELAY_MSEC
        desc_steps = False
    else:
        size = args.size
        if size < MIN_TAPE_SIZE:
            size = MIN_TAPE_SIZE
            lgr.warning(F"MINIMUM tape size = {MIN_TAPE_SIZE}")
        if size > MAX_TAPE_SIZE:
            size = MAX_TAPE_SIZE
            lgr.warning(F"MAXIMUM tape size = {MAX_TAPE_SIZE}")

        pause = args.pause
        if MIN_DELAY_MSEC > pause > MAX_DELAY_MSEC:
            pause = DEFAULT_DELAY_MSEC
            lgr.warning(F"step delay MUST be between {MIN_DELAY_MSEC} and {MAX_DELAY_MSEC}!")

        newline = args.newline
        desc_steps = args.describe

    return size, pause, newline, desc_steps


def main_turing(args:list):
    size, pause, newline, desc = process_input_parameters(args)
    show(F"size = {size}; pause = {pause}; newline = {newline}; desc = {desc}")
    try:
        turing = Turing3p2(size, pause, newline, desc)
        turing.generate()
    except Exception as ex:
        lgr.error(F"PROBLEM with program: {repr(ex)}")
        exit(298)


if __name__ == "__main__":
    show(F"Program started: {run_time}")
    main_turing(sys.argv[1:])
    show("Program completed.")
    exit()
