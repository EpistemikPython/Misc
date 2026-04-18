##############################################################################################################################
# coding=utf-8
#
# check_spellbee_words.py
#   -- from a word file, get all words which can be valid SpellingBee responses and save to a new file
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2026-04-17"
__updated__ = "2026-04-18"

import time
from sys import path, argv
from argparse import ArgumentParser
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_INPUT_FILE = "./input/all_words.txt"
MIN_NUM_LETTERS = 4
MAX_DIFF_LETTERS = 7

def run():
    """From a word file, get all words which can be valid SpellingBee responses and save to a new file."""
    found_words = []
    with open(input_file) as file_in:
        for it in file_in:
            if len(it) < MIN_NUM_LETTERS:
                continue
            result = []
            item = get_clean_word(it)
            for lett in item:
                if lett not in result:
                    result.append(lett)
            if len(result) <= MAX_DIFF_LETTERS:
                found_words.append(str(item))
    if save_option:
        outfile_name = save_to_json("check_spellbee_words", found_words)
        lgr.info(f"\nSaved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "from a word file, get all words which can be valid SpellingBee responses "
                                              "and save to a new file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-n', '--nosave', action = "store_true", default = False,
                            help = "DO NOT save the output to a new JSON file; DEFAULT = False.")
    arg_parser.add_argument('-f', '--file', type = str, metavar = "PATH", default = DEFAULT_INPUT_FILE,
                            help = f"path to a word file with the words to check; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)
    lgr.info(f"save option = '{not args.nosave}'")
    infile = args.file if osp.isfile(args.file) else DEFAULT_INPUT_FILE
    lgr.info(f"input file = '{infile}'")
    return (not args.nosave), infile


log_control = MhsLogger(get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_file = get_args(argv[1:])
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

    lgr.info(f"\nElapsed time = {time.perf_counter() - start} seconds")
    exit(code)
