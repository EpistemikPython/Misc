##############################################################################################################################
# coding=utf-8
#
# jumble.py
#   -- find all the letter permutations from a submitted word
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-10-27"
__updated__ = "2024-10-27"

import os
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, FILE_DATETIME_FORMAT, JSON_LABEL, get_current_time, get_base_filename, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_INPUT_WORD    = "help"

def run():
    pass
#     /**
#      * Prep the String with the submitted letters then jumble.
#      * @param str - letters from the user
#      */
#     private void go(final String str) {
#         StringBuilder letters = new StringBuilder( str );
#         jumbleLogger.info( "letters arriving: " + letters );
#
#         Vector<StringBuilder> vsb = new Vector<>( 32, 8 );
#         jumbleLogger.finer( "Vector capacity == " + vsb.capacity() );
#         jumbleLogger.finer( "Vector size == " + vsb.size() );
#
#         jumbler( letters, vsb );
#
#         jumbleLogger.info( "Final size of Vector: " + vsb.size() );
#         System.out.println( "All combinations from the submitted letters:" );
#         for( StringBuilder sb : vsb )
#             System.out.println( sb );
#     }

def jumbler():
    pass
#     /**
#      * RECURSIVE method to find all letter combinations from a selection of letters
#      * @param sb - the letters to jumble
#      * @param vsb - a vector to store the letter combinations
#      */
#     private void jumbler(StringBuilder sb, Vector<StringBuilder> vsb) {
#         jumbleLogger.fine( "Letters arriving: " + sb );
#
#         if( sb.length() == 1 ) {
#             vsb.add( sb );
#             jumbleLogger.fine( "Added " + sb + " to Vector." );
#         } else {
#             StringBuilder head = pluck( sb );
#
#             // recursive call
#             jumbler( sb, vsb );
#
#             insert( head, vsb );
#         }
#     }

def pluck():
    pass
#     /**
#      * Remove the first letter from a StringBuilder and return it as a StringBuilder
#      * @param target - letter which will be 'plucked'
#      * @return StringBuilder of the initial letter
#      */
#     private StringBuilder pluck(StringBuilder target) {
#         jumbleLogger.fine( "Target arriving: " + target );
#
#         StringBuilder headsb = new StringBuilder( target.substring( 0, 1 ) );
#
#         target.deleteCharAt( 0 );
#
#         jumbleLogger.fine( "Letter plucked from target: " + headsb );
#         jumbleLogger.fine( "Letters left after pluck():" + target );
#
#         return headsb;
#     }

def insert():
    pass
#     /**
#      * Insert the head letter into each position of each StringBuilder in the Vector
#      * @param head - letter to insert
#      * @param vsb - current collection of letter combinations
#      */
#     private void insert(final StringBuilder head, Vector<StringBuilder> vsb) {
#         jumbleLogger.fine( "Insert " + head + " to Vector." );
#
#         int len, limit = vsb.size();
#         jumbleLogger.finer( "Size of Vector == " + limit );
#
#         StringBuilder elem, newsb;
#
#         // process all the StringBuilders in the Vector
#         for( int j = 0; j < limit; j++ ) {
#             elem = vsb.elementAt( j );
#             len = elem.length();
#             // insert the head letter into each position of the target StringBuilder
#             for( int i = 0; i <= len; i++ ) {
#                 newsb = new StringBuilder( elem );
#                 newsb.insert( i, head );
#                 vsb.addElement( newsb );
#             }
#         }
#         vsb.addElement( head );
#     }

def set_args():
    arg_parser = ArgumentParser(description = "find all the letter permutations from a submitted word",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_false", default = True,
                            help = "Save the output to a new JSON file; DEFAULT = True.")
    arg_parser.add_argument('-i', '--input', type = str, default = DEFAULT_INPUT_WORD,
                            help = f"word to jumble; DEFAULT = '{DEFAULT_INPUT_WORD}'.")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    loglev = DEFAULT_LOG_LEVEL

    lgr.log(loglev, f"save option = '{args.save}'")

    inputw = args.input if args.input.isalpha() else DEFAULT_INPUT_WORD
    lgr.log(loglev, f"input file = '{inputw}'")

    return args.save, inputw


if __name__ == '__main__':
    #     public static void main(String[] args) {
    #         Jumble.setLogger();
    #
    #         // process the command line and get properly formatted user input
    #         String letters = setup( args );
    #
    #         // do the jumble
    #         Jumble j1 = new Jumble();
    #         j1.go( letters );
    #
    #         jumbleLogger.info( "*** PROGRAM ENDED ***" );
    #     }
    start = time.perf_counter()
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_word = get_args(argv[1:])
        run()
    except KeyboardInterrupt:
        lgr.exception(">> User interruption.")
        code = 13
    except ValueError:
        lgr.exception(">> Value Error.")
        code = 27
    except Exception as mex:
        lgr.exception(f">> PROBLEM: {repr(mex)}")
        code = 66

    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start} seconds")
    exit(code)
