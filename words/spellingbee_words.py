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
__updated__ = "2023-12-30"

import time
import json
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger

start = time.perf_counter()
WORD_FILE = "input/scrabble-plus.json"
DEFAULT_OUTER_LETTERS = "DARCON"
GROUP_SIZE = len(DEFAULT_OUTER_LETTERS)
DEFAULT_REQD_LETTER = "V"
MIN_WORD_SIZE = 4

def run():
    """find all words from a list that fulfill the specified spelling bee requirements"""
    solutions = []
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        if len(item) >= MIN_WORD_SIZE:
            for letter in item:
                if letter not in outers + required:
                    break
            else:
                if required in item:
                    solutions.append(item)

    show(f"solution count = {len(solutions)}")
    # check for pangrams and print the solutions
    skip = 1 if len(solutions) < 30 else 5
    ct = 0
    pgct = 0
    show(f"{'Sample' if skip == 5 else 'All'} solutions:")
    for val in solutions:
        pg = True
        for lett in outers:
            if lett not in val:
                pg = False
                break
        if pg:
            show(f"\t{val} : Pangram!")
            pgct += 1
        else:
            ct += 1
            if ct % skip == 0:
                show(f"\t{val}")
    show(f">> {pgct if pgct > 0 else 'NO'} Pangram{'' if pgct == 1 else 's'}{'!' * pgct}")

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"{required}-{outers}_spellbee-words", solutions)

def set_args():
    arg_parser = ArgumentParser(description="get the save-to-file, required letter and outer letters options", prog="python3 spellingbee_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-r', '--required', type=str, default=DEFAULT_REQD_LETTER, help="this ONE letter MUST be in each word")
    arg_parser.add_argument('-o', '--outer', type=str, default=DEFAULT_OUTER_LETTERS, help="SIX other POSSIBLE letters in the words")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    if args.required.isalpha() and len(args.required) == 1:
        require = args.required.upper()
        show(f"required letter = {require}")
    else:
        require = DEFAULT_REQD_LETTER
        show(f"INVALID required letter parameter '{args.required}'! Using DEFAULT '{DEFAULT_REQD_LETTER}'.")

    # make sure all the outer letters are different?
    outer = args.outer.upper()
    if outer.isalpha() and len(outer) == GROUP_SIZE:
        if require in outer:
            others = outer.replace(require, 'X')
            show(f"INVALID outer letters '{args.outer}'! Required letter '{require}' CANNOT be in outers! >> Replace with 'X': outers = '{others}'")
        else:
            others = outer
            show(f"outer letters = {others}")
    else:
        show(f"INVALID outer letters '{args.outer}'!! Using DEFAULT '{DEFAULT_OUTER_LETTERS}'.")
        others = DEFAULT_OUTER_LETTERS

    return args.save, require, others


if __name__ == '__main__':
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    code = 0
    try:
        save_option, required, outers = prep_args(argv[1:])
        run()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem = '{repr(ex)}'")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
