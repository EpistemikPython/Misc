#   Mark Sattolo (epistemik@gmail.com)
# -----------------------------------------------
# $File: #depot/Eclipse/Java/workspace/Turing/src/mhs/turing/Turing3_2.java $
# $Revision: #3 $
# $Change: 180 $
# $DateTime: 2012/05/19 06:12:55 $
# -----------------------------------------------
#
#  mhs.turing.Turing3_2.java
#  Created May 11, 2012
#  git version created Mar 3, 2014
#  independent git repository created Apr 6, 2015

# import joptsimple.OptionParser
# import joptsimple.OptionSet

# number of 'squares' available on the 'tape'
# static int
DEFAULT_TAPE_SIZE = 256
# MAXIMUM number of 'squares' available on the 'tape'
# static int
MAX_TAPE_SIZE = 1024 * 16
# MINIMUM number of 'squares' available on the 'tape'
# static int
MIN_TAPE_SIZE = 16

# if displaying each step of the algorithm, DEFAULT delay (in msec) between each step
# static int
DEFAULT_DELAY_MS = 2000
# if displaying each step of the algorithm, MINIMUM delay (in msec) between each step
# static int
MIN_DELAY_MS = 5
# if displaying each step of the algorithm, MAXIMUM delay (in msec) between each step
# static int
MAX_DELAY_MS = 1000 * 60

# tape symbol
# static int
nBLANK = 0  # nBLANK = 0 so tape array is initialized by default to all blanks
nZERO = 1
nONE = 2
nX = 3
nSCHWA = 4

# symbols to display -- order MUST MATCH the values for the tape symbol ints
# static String[]
STR_SYMBOLS = ["",   # nBLANK
               "0",  # nZERO
               "1",  # nONE
               "x",  # nX
               "@"   # nSCHWA
               ]

# machine state
# static int
STATE_BEGIN = 0
STATE_PRINT_X = 1
STATE_ERASE_X = 2
STATE_PRINT_0 = 3
STATE_PRINT_1 = 4

# state names for display -- order MUST MATCH the values for the machine state ints
# static String[]
STR_STATES = ["STATE_BEGIN", "STATE_PRINT_X", "STATE_ERASE_X", "STATE_PRINT_0", "STATE_PRINT_1"]

# Java implementation of the Turing machine described in "On Computable Numbers (1936)", section 3.II,<br>
# which generates a sequence of 0's followed by an increasing number of 1's, from 0 to infinity,<br>
# i.e. 001011011101111011111...<br>
# See also <i>The Annotated Turing</i> by <b>Charles Petzold</b> Chapter 5, pp.85-94.
#
# @author mhsatto
# @version 1.5.1
# @date 2019-02-23
class Turing3p2:
    def __init__(self):
        # current state of the machine
        # int
        self.state = 0
        # current position on the 'tape'
        # int
        self.position = 0

        # use an array as a substitute for the <em>infinite</em> tape
        # int[]
        self.ar_tape = []

        # determine whether each step is displayed
        # boolean
        self.show_steps = False
        # delay, in milliseconds, between each step display
        # int
        self.step_delay = DEFAULT_DELAY_MS
        # default tape array size
        # boolean
        self.tape_default = True
        # size of the 'tape' array
        # int
        self.tape_size = DEFAULT_TAPE_SIZE

        # determine whether print 'new-line' starting at each zero
        # boolean
        self.show_newline = True

    # run the algorithm:<br>
    # - check the current state<br>
    # - check the current position on the "tape"<br>
    # - create or erase a symbol if necessary<br>
    # - move to a different position on the "tape" if necessary<br>
    # - set the next state<br>
    def generate(self):
        step = 0

        print(("\nUsing DEFAULT s" if self.tape_default else "\nS") + "ize of tape array = " + str(len(self.ar_tape)))
        print(".\nStep pause is " + str(self.step_delay) + ".\n" if self.show_steps else ".")

        # initial state
        self.begin()

        # we don't have an infinite tape -- continue until we move past the end of the array
        while self.position < self.tape_size:

            step += 1
            location = self.ar_tape[self.position]

            if self.show_steps:
                self.show_step(step)

            # switch(state) {

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
            # switch
        # do

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
    # @param i - symbol to set
    def set(self, i:int):
        self.ar_tape[self.position] = i

    # ERASE the symbol at the current position
    def erase(self):
        self.ar_tape[self.position] = nBLANK

    # MOVE RIGHT on the tape by one square
    # def move_right(self):
    #     self.move_right(1)

    # MOVE RIGHT by the specified number of squares - not in Turing's description but more convenient
    # @param count - number of squares to move to the right
    def move_right(self, count:int=1):
        self.position += count

        # end program when position moves beyond the end of the array
        if self.position >= self.tape_size:
            print("Reached position # " + str(self.position) + " >> ENDING PROGRAM.\n")
            self.end()

    # MOVE LEFT on the tape by one square
    # def move_left(self):
    #     self.move_left(1)

    # MOVE LEFT by the specified number of squares - not in Turing's description but more convenient
    # @param count - number of squares to move to the left
    def move_left(self, count:int=1):
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
        printSymbol(self.ar_tape[self.position], False)
        print("]")

        self.printTape()

        # pause to allow easier inspection of each step
        try:
             Thread.sleep(step_delay) # milliseconds
         catch( InterruptedException ie ):
            ie.printStackTrace()


# DISPLAY the symbol used for different types of <code>position</code> on the tape to stdout
# @param posn - position on the tape to display
# @param newline - new line starting at each 'zero'
def printSymbol(posn:int, newline:bool):
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


# process the command line arguments and initialize the program
#  <code>OptionParser</code> options: -h for help, -s [arg] for steps, -t <arg> for tape size,
#  -n for newline, -x for nice example run
#  @param args - from command line
# def setup(String[] args):
def setup(args:list):
    # Short options can accept single arguments. The argument can be made required or optional.
    # When you construct an OptionParser with a string of short option characters,
    # append a single colon (:) to an option character to configure that option to require an argument.
    # Append two colons (::) to an option character to configure that option to accept an optional argument.
    # Append an asterisk (*) to an option character, but before any "argument" indicators, to configure that option as a "help" option.

    OptionParser parser = new OptionParser("h*s::t:nx")
    OptionSet options = parser.parse(args)

    # show help
    if options.has("h"):
        System.out.println(
            "\n Java implementation of the Turing machine described in 'On Computable Numbers' (1936), section 3.II,"
            + "\n which generates a sequence of 0's followed by an increasing number of 1's, from 0 to infinity,"
            + "\n i.e. 001011011101111011111... \n"
            + "\n Usage: java <class-file> [-h] [-s [arg]] [-t <arg>] "
            + "\n -h to print this message."
            + "\n -t <int> to specify the size of the tape array (within reason)."
            + "\n -s [int] to have each step of the algorithm displayed with a 2-second pause between steps,"
            + "\n    > use the optional argument to set the pause between each step, in milliseconds."
            + "\n -n to start a new line with each zero."
            + "\n -x to run a nice example = [-n -t 602]\n")

        # try:
        #     parser.printHelpOn( System.out )
        #
        # catch( IOException ioe ):
        #     ioe.printStackTrace()
        #

        System.exit(0)

    # use -s [pause] to show each step and optionally specify a pause interval by entering an integer argument
    if options.has("s"):
        show_steps = True

        # use "-" for blank squares to see each step more clearly
        STR_SYMBOLS[nBLANK] = "-"

        # check for optional argument
        if options.hasArgument("s"):
            step_delay = Integer.valueOf((String)options.valueOf("s"))
            if (step_delay < MIN_DELAY_MS):
                System.out.println("\n\t>>> MINIMUM value for the step pause is " + MIN_DELAY_MS + ". <<<")
                step_delay = MIN_DELAY_MS
            elif ( step_delay > MAX_DELAY_MS ):
                System.out.println("\n\t>>> MAXIMUM value for the step pause is " + MAX_DELAY_MS + ". <<<")
                step_delay = MAX_DELAY_MS

    # -s

    # use -t <tape_size> to request a particular array (tape) size
    if options.has("t"):
        tape_size = Integer.valueOf((String)options.valueOf("t"))
        if tape_size < MIN_TAPE_SIZE:
            tape_size = MIN_TAPE_SIZE
            System.out.println("\n\t>>> MINIMUM value for the tape size is " + MIN_TAPE_SIZE + ". <<<")
        elif tape_size > MAX_TAPE_SIZE:
            tape_size = MAX_TAPE_SIZE
            System.out.println("\n\t>>> MAXIMUM value for the tape size is " + MAX_TAPE_SIZE + ". <<<")

        tape_default = False
    # -t

    # use -n to print a 'new-line' starting with each zero
    if options.has("n"):
        show_newline = True
    # -n

    # use -x to run a nice example
    if options.has("x"):
        tape_size = 602
        tape_default = False
        show_newline = True
    # -x

    ar_tape = new int[tape_size]

    state = STATE_BEGIN
    position = 0

# create the machine, process the command line, then start the algorithm
# @param args - from command line
main(String[] args):
    Turing3_2 turing = new Turing3_2()
    turing.setup(args)
    turing.generate()
