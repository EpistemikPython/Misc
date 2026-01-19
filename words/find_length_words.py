##############################################################################################################################
# coding=utf-8
#
# find_length_words.py
#   -- process a list of words to find words of the specified lengths and optionally save to a JSON file
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2026-01-08"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

start = time.perf_counter()
DEFAULT_WORD_FILE = "input/scrabble-plus.json"
DEFAULT_LENGTH = 5
MIN_LENGTH = 2
MAX_LENGTH = 15

def run():
    """Process a list of words to find words of the specified lengths and optionally save to a JSON file."""
    newlist = []
    wdf = json.load( open(file_name) )
    for item in wdf:
        if lower <= len(item) <= upper:
            newlist.append(item)
    lgr.info(f"word count = {len(newlist)}\n")

    lgr.info("sample output:")
    ni = 0
    nli = len(newlist) // 30
    for word in newlist:
        if ni % nli == 0:
            lgr.info(f'"{word}",')
        ni += 1

    if save_option:
        lgr.info(f"\nsolve and display elapsed time = {time.perf_counter() - start} seconds.")
        save_name = f"{lower}-{upper}_letter_words" if lower != upper else f"{lower}-letter_words"
        saved_file = save_to_json(save_name, newlist)
        lgr.info(f"\n\t Saved results to '{saved_file}'")

def set_args():
    arg_parser = ArgumentParser(description = "process a list of words to find words of the specified lengths",
                                prog = f"python3 {argv[0]}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_true", default = False,
                            help = "Write the results to a JSON file.")
    arg_parser.add_argument('-f', '--file', type = str, default = DEFAULT_WORD_FILE,
                            help = f"path to alternate file with list of all acceptable words; DEFAULT = {DEFAULT_WORD_FILE}.")
    arg_parser.add_argument('-l', '--lower', type = int, default = DEFAULT_LENGTH,
                            help = f"minimum number of letters in the words; DEFAULT = {DEFAULT_LENGTH}; MIN = {MIN_LENGTH}.")
    arg_parser.add_argument('-u', '--upper', type = int, default = MAX_LENGTH,
                            help = f"maximum number of letters in the words; DEFAULT = {DEFAULT_LENGTH}; MAX = {MAX_LENGTH}.")
    return arg_parser

def get_args(argl:list):
    args_log_level = DEFAULT_LOG_LEVEL
    args = set_args().parse_args(argl)

    lgr.log(args_log_level, f"save option = '{args.save}'.")

    if osp.isfile(args.file):
        infile = args.file
        lgr.log(args_log_level, f"input file = '{infile}'.")
    else:
        infile = DEFAULT_WORD_FILE
        lgr.warning(f">> BAD input file = '{args.file}'!! >> Using default file = '{infile}'.")

    low = args.lower if MIN_LENGTH <= args.lower <= MAX_LENGTH else DEFAULT_LENGTH
    lgr.log(args_log_level, f"lower limit = {low}")

    up = args.upper if low <= args.upper <= MAX_LENGTH else DEFAULT_LENGTH
    lgr.log(args_log_level, f"upper limit = {up}\n")

    return args.save, infile, low, up


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, file_name, lower, upper = get_args(argv[1:])
        lgr.info("START MAIN LOGGING.")
        run()
    except KeyboardInterrupt as mki:
        lgr.exception(mki)
        code = 13
    except ValueError as mve:
        lgr.exception(mve)
        code = 27
    except Exception as mex:
        lgr.exception(mex)
        code = 66
    lgr.info(f"\n\tTotal elapsed time = {time.perf_counter() - start} seconds.")
    exit(code)
