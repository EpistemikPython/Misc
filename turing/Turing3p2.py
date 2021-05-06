##############################################################################################################################
# coding=utf-8
#
# Turing3p2.py -- Turing machine simulator program ported from Turing3_2.java
#
#   Python implementation of the Turing machine described in "On Computable Numbers (1936)", section 3.II,<br>
#   which generates a sequence of 0's each followed by an increasing number of 1's, from 0 to infinity,<br>
#   i.e. 001011011101111011111...<br>
#   See also <i>The Annotated Turing</i> by <b>Charles Petzold</b> Chapter 5, pp.85-94.
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
nBLANK = 0  # nBLANK = 0 so tape array is initialized by default to all blanks
nZERO  = 1
nONE   = 2
nX     = 3
nSCHWA = 4

# symbols to display -- order MUST MATCH the values for the tape symbol ints
STR_SYMBOLS = ["",  # nBLANK
               "0",  # nZERO
               "1",  # nONE
               "x",  # nX
               "@"  # nSCHWA
               ]

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
        # current state of the machine
        self.state = STATE_BEGIN
        # current position on the 'tape'
        self.position = 0

        # use an array as a substitute for the <em>infinite</em> tape
        self.ar_tape = list()
        # size of the 'tape' array
        self.tape_size = p_size

        # determine whether each step is displayed
        self.show_steps = p_show
        # delay, in seconds, between each step display
        self.step_delay = p_pause / 1000.0

        # determine whether print 'new-line' starting at each zero
        self.show_newline = p_newline

    # run the algorithm:<br>
    # - check the current state<br>
    # - check the current position on the "tape"<br>
    # - create or erase a symbol if necessary<br>
    # - move to a different position on the "tape" if necessary<br>
    # - set the next state<br>
    def generate(self):
        step = 0
        show( F"Size of tape array = {str(len(self.ar_tape))}" )
        show( F"Step pause = {str(self.step_delay)} sec" )

        # initial state
        self.begin()
        # we don't have an infinite tape -- continue until we move past the end of the array
        while self.position < self.tape_size:
            step += 1
            location = self.ar_tape[self.position]

            if self.show_steps:
                self.show_step(step)

            if self.state == STATE_PRINT_X:
                if location == nONE:
                    self.move_right()
                    self.set(nX)
                    self.move_left(3)

                elif location == nZERO:
                    self.state = STATE_PRINT_1

            elif self.state == STATE_ERASE_X:
                if location == nX:
                    self.erase()
                    self.move_right()
                    self.state = STATE_PRINT_1

                elif location == nSCHWA:
                    self.move_right()
                    self.state = STATE_PRINT_0

                elif location == nBLANK:
                    self.move_left(2)

            elif self.state == STATE_PRINT_0:
                if location == nBLANK:
                    self.set(nZERO)
                    self.move_left(2)
                    self.state = STATE_PRINT_X
                else:
                    self.move_right(2)

            elif self.state == STATE_PRINT_1:
                if location == nBLANK:
                    self.set(nONE)
                    self.move_left()
                    self.state = STATE_ERASE_X
                else:
                    # location == nZERO || location == nONE
                    self.move_right(2)

            else:
                # throw new IllegalStateException("\n\t>> Current state is '" + state + "'?!")
                print("\n\t>> Current state is '" + str(self.state) + "'?!")

        self.end()

    # the actions at the INITIAL STATE of the algorithm -- NEVER return to this state again
    def begin(self):
        if self.state != STATE_BEGIN:
            return

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
    def set(self, sym:int):
        self.ar_tape[self.position] = sym

    # ERASE the symbol at the current position
    def erase(self):
        self.ar_tape[self.position] = nBLANK

    # MOVE RIGHT by the specified number of squares - not in Turing's description but more convenient
    def move_right(self, count:int = 1):
        self.position += count
        # end program when position moves beyond the end of the array
        if self.position >= self.tape_size:
            print("Reached position # " + str(self.position) + " >> ENDING PROGRAM.\n")
            self.end()

    # MOVE LEFT by the specified number of squares - not in Turing's description but more convenient
    def move_left(self, count:int = 1):
        self.position -= count
        # return to 0 if move before the start of the array -- SHOULD NEVER HAPPEN
        if self.position < 0:
            print("WARNING: Position: [" + str(self.position) + "] is less than 0 !")
            self.position = 0

    # DISPLAY the sequence of symbols on the tape, then exit.
    def end(self):
        if not self.show_steps:
            self.printTape()
        print("\n == DONE ==")
        exit(0)

    # DISPLAY the sequence of symbols on the tape
    def printTape(self):
        for posn in self.ar_tape:
            printSymbol(posn, self.show_newline)
        print("E")

    # DISPLAY the step sequence and machine state at a particular point in the program
    # @param step - current count in the series of instructions
    def show_step(self, step:int):
        print("Step #" + str(step) + " - State = " + STR_STATES[self.state] + " - Position is " + str(self.position) + "[")
        printSymbol(self.ar_tape[self.position], self.show_newline)
        print("]")

        self.printTape()

        # pause to allow easier inspection of each step
        try:
            time.sleep(self.step_delay) # seconds
        except Exception as ex:
            print(repr(ex))


# END class Turing3p2


# DISPLAY the symbol used for different types of <code>position</code> on the tape to stdout
# @param posn - position on the tape to display
# @param newline - new line starting at each 'zero'
def printSymbol(posn: int, newline: bool):
    if posn == nBLANK:
        print(STR_SYMBOLS[nBLANK])

    elif posn == nSCHWA:
        print(STR_SYMBOLS[nSCHWA])

    elif posn == nX:
        print(STR_SYMBOLS[nX])

    elif posn == nZERO:
        if newline:
            print("")
        print(STR_SYMBOLS[nZERO])

    elif posn == nONE:
        print(STR_SYMBOLS[nONE])

    else:
        # throw new IllegalStateException("\n\t>> Current symbol is '" + posn + "'?!")
        print("\n\t>> Current symbol is '" + str(posn) + "'?!")


def process_args():
    arg_help = "Java implementation of the Turing machine described in 'On Computable Numbers' (1936), section 3.II,\n " \
               "which generates a sequence of 0's followed by an increasing number of 1's, from 0 to infinity,\n " \
               "i.e. 001011011101111011111... \n"

    arg_parser = ArgumentParser(description = arg_help, prog = "Turing3p2.py")
    # optional arguments
    arg_parser.add_argument('-d', "--describe", action = "store_true", help = "describe EACH algorithm step")
    arg_parser.add_argument('-s', "--size", type = int, default = DEFAULT_TAPE_SIZE,
                            help = "amount of output (number of digits)")
    arg_parser.add_argument('-p', "--pause", type = int, default = 2, help = "pause between each step, in seconds")
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
        if MIN_TAPE_SIZE > size > MAX_TAPE_SIZE:
            size = DEFAULT_TAPE_SIZE
            show(F"size = {size}")
        pause = args.pause
        if MIN_DELAY_MSEC > pause > MAX_DELAY_MSEC:
            pause = DEFAULT_DELAY_MSEC
            show(F"pause = {pause}")
        newline = args.newline
        desc_steps = args.describe

    return size, pause, newline, desc_steps


def main_turing(args: list):
    show(F"Program started: {run_time}")
    size, pause, newline, desc = process_input_parameters(args)
    try:
        turing = Turing3p2(size, pause, newline, desc)
        turing.generate()
    except Exception as ex:
        lgr.error(F"PROBLEM with program: {repr(ex)}")
        exit(349)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main_turing(sys.argv[1:])
    else:
        lgr.warning("MISSING file name!")
    show("Program completed.")
    exit()
