##############################################################################################################################
# coding=utf-8
#
# ideal_words.py -- from a word list find all the words of the specified length that contain only the specified letters
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-11-22"
__updated__ = "2023-11-23"

import time
import json
from sys import path, argv
from argparse import ArgumentParser
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger

log_control = MhsLogger(get_base_filename(__file__))
lgr = log_control.get_logger()
lgr.warning("START LOGGING")
show = log_control.show

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
DEFAULT_EXTRA_LETTERS = "NDWPGHVJKXQZ"
MAX_EXTRA_LETTERS = 20
DEFAULT_REQUIRED_LETTERS = "AEO"
MAX_REQUIRED_LETTERS = 5
DEFAULT_WORD_SIZE = 7

def run_ideal(save_option, required, group):
    """from a word list find all the words that contain only the specified letters"""

    solutions = []
    sct = 0
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        if len(item) == DEFAULT_WORD_SIZE:
            # good = True
            for letter in item:
                if letter not in group + required:
                    break
            else:
                for lt in required:
                    if lt not in item:
                        # good = False
                        break
                else:
                    solutions.append(item)
                    sct += 1

    show(f"solution count = {sct}")
    # print the solutions
    show(f"solutions:")
    for val in solutions:
        show(f"\t{val}")

    show(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json(f"{required}-{group}_ideal_words", solutions)


def process_args():
    arg_parser = ArgumentParser(description="get the save, required letters and possible letters options", prog="ideal_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save',  action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-r', '--required', type=str, default=DEFAULT_REQUIRED_LETTERS, help="letters MUST be in the words")
    arg_parser.add_argument('-o', '--other', type=str, default=DEFAULT_EXTRA_LETTERS, help="possible letters in the words")
    return arg_parser


def main_ideal(argl:list):
    args = process_args().parse_args(argl)

    save_option = "Yes" if args.save else "No"
    show(f"save option = '{save_option}'")

    required = args.required.upper()
    # make sure the required letters are not among the other letters?
    show(f"required letters = {required}")

    group = args.other.upper()
    # make sure all the letters are different?
    show(f"other letters = {group}")

    run_ideal(save_option, required, group)


if __name__ == '__main__':
    main_ideal(argv[1:])
    show(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
