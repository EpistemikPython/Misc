##############################################################################################################################
# coding=utf-8
#
# spellingbee_words.py -- from a word list file, find all words that fulfill the specified spelling bee requirements
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2023-12-08"

import time
import json
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
DEFAULT_OUTER_LETTERS = "CONLAY"
GROUP_SIZE = len(DEFAULT_OUTER_LETTERS)
DEFAULT_REQD_LETTER = "I"
MIN_WORD_SIZE = 4

def run_sb(save_option, required, group):
    """find all words from a list that fulfill the specified spelling bee requirements"""
    solutions = []
    sbw = json.load( open(WORD_FILE) )
    for item in sbw:
        if len(item) >= MIN_WORD_SIZE:
            for letter in item:
                if letter not in group + required:
                    break
            else:
                if required in item:
                    solutions.append(item)

    show(f"solution count = {len(solutions)}")
    # check for pangrams and print the solutions
    pgct = 0
    show(f"solutions:")
    for val in solutions:
        pg = True
        for lett in group:
            if lett not in val:
                pg = False
                break
        if pg:
            show(f"\t{val} : Pangram!")
            pgct += 1
        else:
            show(f"\t{val}")
    show(f">> {pgct if pgct > 0 else 'NO'} Pangram{'' if pgct == 1 else 's'}{'!' * pgct}")

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"{required}-{group}_spellbee_words", solutions)


def process_args():
    arg_parser = ArgumentParser(description="get the save-to-file, required letter and outer letters options", prog="spellingbee_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-r', '--required', type=str, default=DEFAULT_REQD_LETTER, help="this letter MUST be in each word")
    arg_parser.add_argument('-o', '--outer', type=str, default=DEFAULT_OUTER_LETTERS, help="other possible letters in the words")
    return arg_parser


def prep_sb(argl:list) -> (bool, str, str):
    args = process_args().parse_args(argl)

    lgr.warning("START LOGGING")
    show(f"save option = '{args.save}'")

    required = args.required[0].upper() if args.required.isalpha() else DEFAULT_REQD_LETTER
    # make sure the required letter is not in the outer letters?
    show(f"required letter = {required}")

    outer = args.outer.upper() if args.outer.isalpha() and len(args.outer) == GROUP_SIZE else DEFAULT_OUTER_LETTERS
    # make sure all the outer letters are different?
    show(f"outer letters = {outer}")

    return args.save, required, outer


if __name__ == '__main__':
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    save, reqd, others = prep_sb(argv[1:])
    run_sb( save, reqd, others )
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
