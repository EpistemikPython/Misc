################################################################################################################################
# coding=utf-8
#
# ideal_words.py -- from a word list find all the words of the specified length that contain only the specified letters
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-11-22"
__updated__ = "2024-01-01"

import time
import json
from sys import path, argv
from argparse import ArgumentParser
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger

start = time.perf_counter()
WORD_FILE = "input/scrabble-plus.json"
DEFAULT_EXTRA_LETTERS = "NDWPGHVJKXQZ"
MAX_EXTRA_LETTERS = 20
DEFAULT_REQUIRED_LETTERS = "AEO"
MAX_REQUIRED_LETTERS = 8
DEFAULT_WORD_SIZE = 7
MIN_WORD_SIZE = 5
MAX_WORD_SIZE = 15

def run_ideal():
    """from a word list find all the words of the specified length that contain only the specified letters"""

    solutions = []
    wdf = json.load( open(WORD_FILE) )
    show(f"loaded file '{WORD_FILE}'")
    for item in wdf:
        if len(item) == word_size:
            for letter in item:
                if letter not in others + required:
                    break
            else:
                for lt in required:
                    if lt not in item:
                        break
                else:
                    solutions.append(item)

    num_wd = len(solutions)
    show(f"\nFound {num_wd} words.\n")
    # display a selection of the output
    skip = 10 if num_wd > 150 else 5 if num_wd > 30 else 1
    show(f"{'Sample' if skip >= 5 else 'All'} solutions:")
    ni = 0
    for word in solutions:
        ni += 1
        if ni % skip == 0:
            show(word)

    show(f"\nsolve & display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"{required}-{others}_ideal-words", solutions)

def set_args():
    arg_parser = ArgumentParser(description="get the save-to-file, word size, required and possible letters options", prog="python3 ideal_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-n', '--numletters', type=int, default=DEFAULT_WORD_SIZE, help="number of letters in each found word")
    arg_parser.add_argument('-r', '--required', type=str, default=DEFAULT_REQUIRED_LETTERS, help="each of these letters MUST be in EACH word")
    arg_parser.add_argument('-o', '--other', type=str, default=DEFAULT_EXTRA_LETTERS, help="other possible letters in the words")
    return arg_parser

def prep_args(argl:list) -> (bool, int, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = {args.save}")

    word_sz = args.numletters if MIN_WORD_SIZE <= args.numletters <= MAX_WORD_SIZE else DEFAULT_WORD_SIZE
    show(f"word size = {word_sz}")

    require = args.required.upper() if args.required.isalpha() and 0 < len(args.required) <= MAX_REQUIRED_LETTERS else DEFAULT_REQUIRED_LETTERS
    # make sure the required letters are not among the other letters?
    show(f"required letters = '{require}'")

    other = args.other.upper() if args.other.isalpha() and 0 < len(args.other) <= MAX_EXTRA_LETTERS else DEFAULT_EXTRA_LETTERS
    # make sure all the letters are different?
    show(f"other letters = '{other}'")

    return args.save, word_sz, require, other


if __name__ == "__main__":
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    save_option, word_size, required, others = prep_args(argv[1:])
    run_ideal()
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
