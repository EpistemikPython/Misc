##############################################################################################################################
# coding=utf-8
#
# Turing3p2.py -- Turing machine simulator ported from Turing3_2.java
#
#   Python implementation of the Turing machine described in "On Computable Numbers (1936)", section 3.II,
#   which generates a sequence of 0's each followed by an increasing number of 1's, from zero to infinity,
#   i.e. 001011011101111011111...
#   Also see <i>The Annotated Turing</i> by <b>Charles Petzold</b> Chapter 5, pp.85-94.
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-05"
__updated__ = "2023-10-19"

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
run_time = mhsLogging.run_ts
lgr.warning("START LOGGING")

# number of 'squares' available on the 'tape'
DEFAULT_TAPE_SIZE = 256
# MAXIMUM number of 'squares' available on the 'tape'
MAX_TAPE_SIZE = 1024 * 16
# MINIMUM number of 'squares' available on the 'tape'
MIN_TAPE_SIZE = 16

# if displaying each step of the algorithm, DEFAULT delay (in msec) between each step
DEFAULT_DELAY_MSEC = 2000
# if displaying each step of the algorithm, MINIMUM delay (in msec) between each step
MIN_DELAY_MSEC = 50
# if displaying each step of the algorithm, MAXIMUM delay (in msec) between each step
MAX_DELAY_MSEC = 60 * 1000

# tape symbols
symBLANK  = ''
SYM_ZERO  = '0'
SYM_ONE   = '1'
SYM_X     = 'x'
SYM_SCHWA = '@'

# state names for display
STATE_LABELS = ["STATE_BEGIN", "STATE_PRINT_X", "STATE_ERASE_X", "STATE_PRINT_0", "STATE_PRINT_1"]

# machine states
STATE_BEGIN   = STATE_LABELS.index("STATE_BEGIN")
STATE_PRINT_X = STATE_LABELS.index("STATE_PRINT_X")
STATE_ERASE_X = STATE_LABELS.index("STATE_ERASE_X")
STATE_PRINT_0 = STATE_LABELS.index("STATE_PRINT_0")
STATE_PRINT_1 = STATE_LABELS.index("STATE_PRINT_1")

class Turing3p2:
    """Python implementation of the Turing machine described in "On Computable Numbers (1936)", section 3.II"""
    def __init__(self, p_size=DEFAULT_TAPE_SIZE, p_pause=DEFAULT_DELAY_MSEC, p_newline=True, p_show=False):
        # use as a substitute for the 'infinite' tape
        self.tape = dict()
        # size of the tape
        self.tape_size = p_size

        global symBLANK
        # determine whether each step is displayed
        self.show_steps = p_show
        if p_show:
            symBLANK = '-' # for easier visualization
        # prepare the empty tape
        for r in range(self.tape_size):
            self.tape[str(r)] = symBLANK

        # delay, in milliseconds, between each step display
        self.step_delay = p_pause

        # start each zero on a new line
        self.show_newline = p_newline

        # current state of the machine
        self.state = STATE_BEGIN
        # current position on the tape
        self.position = 0

    def begin(self):
        """set the INITIAL STATE of the machine -- should NEVER return to this state"""
        if self.state != STATE_BEGIN:
            lgr.warning(F"UNEXPECTED return to {STATE_LABELS[STATE_BEGIN]}?!")
            return

        show(STATE_LABELS[STATE_BEGIN])
        if self.show_steps:
            self.show_step(0)

        self.set(SYM_SCHWA)
        self.move_right()
        self.set(SYM_SCHWA)
        self.move_right()
        self.set(SYM_ZERO)
        self.move_right(2)
        self.set(SYM_ZERO)
        self.move_left(2)
        self.state = STATE_PRINT_X

    def generate(self):
        """run the algorithm:
        - check the current state
        - check the current position on the 'tape'
        - create or erase a symbol if necessary
        - move to a different position on the 'tape' if necessary
        - set the next state
        """
        step = 0
        dbg( F"Size of tape array = {str(len(self.tape.keys()))}")
        dbg( F"Step pause = {str(self.step_delay)} msec" )
        # set the initial state
        self.begin()

        # we don't have an infinite tape --
        # >> CONTINUE UNTIL PAST THE END OF THE TAPE
        while self.position < self.tape_size:
            step += 1
            current_symbol = self.tape[str(self.position)]
            if self.show_steps:
                dbg(F"current position = {self.position}; current symbol = {current_symbol}")
                self.show_step(step)
                dbg(STATE_LABELS[self.state])

            if self.state == STATE_PRINT_X:
                if current_symbol == SYM_ONE:
                    self.move_right()
                    self.set(SYM_X)
                    self.move_left(3)
                elif current_symbol == SYM_ZERO:
                    self.state = STATE_PRINT_1

            elif self.state == STATE_ERASE_X:
                if current_symbol == SYM_X:
                    self.erase()
                    self.move_right()
                    self.state = STATE_PRINT_1
                elif current_symbol == SYM_SCHWA:
                    self.move_right()
                    self.state = STATE_PRINT_0
                elif current_symbol == symBLANK:
                    self.move_left(2)

            elif self.state == STATE_PRINT_0:
                if current_symbol == symBLANK:
                    self.set(SYM_ZERO)
                    self.move_left(2)
                    self.state = STATE_PRINT_X
                else:
                    self.move_right(2)

            elif self.state == STATE_PRINT_1:
                if current_symbol == symBLANK:
                    self.set(SYM_ONE)
                    self.move_left()
                    self.state = STATE_ERASE_X
                else:
                    # current symbol == nZERO or nONE
                    self.move_right(2)

            else:
                raise Exception(F">>> UNKNOWN current state = {str(self.state)}?!")

    def set(self, symbol:str):
        """SET the specified symbol on the tape at the current position"""
        self.tape[str(self.position)] = symbol

    def erase(self):
        """ERASE the symbol at the current position"""
        self.tape[str(self.position)] = symBLANK

    def move_right(self, count:int=1):
        """MOVE RIGHT by the specified number of squares - not in Turing's description but more convenient"""
        self.position += count
        # END PROGRAM when position moves beyond the end of the tape
        if self.position >= self.tape_size:
            lgr.warning("Reached position # " + str(self.position) + " >> ENDING PROGRAM.")
            turing_sleep(DEFAULT_DELAY_MSEC) # to ensure the printouts are NOT interleaved
            if not self.show_steps:
                self.print_tape()
            show(" === DONE === ")

    def move_left(self, count:int=1):
        """MOVE LEFT by the specified number of squares - not in Turing's description but more convenient"""
        self.position -= count
        # return to position 0 if move BEFORE the beginning of the tape -- SHOULD NEVER HAPPEN
        if self.position < 0:
            lgr.warning("Position is less than 0 !!")
            self.position = 0

    def print_tape(self):
        """DISPLAY the current sequence of symbols on the tape"""
        current_tape = ""
        for posn in self.tape.keys():
            if self.tape[posn] == SYM_ZERO and self.show_newline:
                print("")
            print(self.tape[posn], end='')
            current_tape += self.tape[posn]
        print('E')
        current_tape += 'E'
        dbg(current_tape)

    def show_step(self, step:int):
        """DISPLAY the position and machine state at a particular point in the program"""
        show("Step #" + str(step) + " - State = " + STATE_LABELS[self.state] +
             " - Position is " + str(self.position) + "[" + self.tape[str(self.position)] + "]")
        self.print_tape()
        # pause to allow easier inspection of each step
        try:
            turing_sleep(self.step_delay)
        except Exception as ex:
            raise Exception( repr(ex) )

# END class Turing3p2

def turing_sleep(msec:int):
    """ convert msec to sec and sleep """
    time.sleep( float(msec) / 1000.0 )

def process_args():
    arg_desc = "Implementation of the state machine described in 'On Computable Numbers' (1936) by Alan Turing, " \
               "section 3.II, which generates a sequence of 0's each followed by an increasing number of 1's, " \
               "from zero to infinity, i.e. 001011011101111011111..."
    arg_parser = ArgumentParser(description = arg_desc, prog = "Turing3p2.py")
    # optional arguments
    arg_parser.add_argument('-d', "--describe", action = "store_true", help = "describe EACH algorithm step")
    arg_parser.add_argument('-s', "--size", type = int, default = DEFAULT_TAPE_SIZE,
                            help = F"number of tape 'squares' ({MIN_TAPE_SIZE} <= SIZE <= {MAX_TAPE_SIZE})")
    arg_parser.add_argument('-p', "--pause", type = int, default = DEFAULT_DELAY_MSEC,
        help = F"time to pause between each algorithm step, in msec ({MIN_DELAY_MSEC} <= PAUSE <= {MAX_DELAY_MSEC})")
    arg_parser.add_argument('-n', "--newline", action = "store_true", help = "each zero in the output starts on a new line")
    arg_parser.add_argument('-x', "--example", action = "store_true", help = "run a nice example [-n -s602]")

    return arg_parser


def process_input_parameters(argx: list):
    args = process_args().parse_args(argx)
    dbg(F"\n\targs = {args}")

    if args.example:
        newline = True
        size = 602
        pause = MIN_DELAY_MSEC
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
        lgr.error(F"PROBLEM with program: {repr(ex)}!")
        exit(66)


if __name__ == "__main__":
    start = time.perf_counter()
    show(F"Program started: {run_time}")
    main_turing(sys.argv[1:])
    show(F"\nProgram completed.\nelapsed time = {time.perf_counter() - start}")
    exit(0)
