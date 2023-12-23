##############################################################################################################################
# coding=utf-8
#
# choose_words.py -- process a list of words to find words of the specified lengths and save to a json file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2023-12-23"

import time
import json
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
DEFAULT_LENGTH = 5
MIN_LENGTH = 2
MAX_LENGTH = 15

def run_choose():
    """process a list of words to find words of the specified length(s) and save to a json file"""
    newlist = []
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        if lower <= len(item) <= upper:
            newlist.append(item)
    print(f"word count = {len(newlist)}\n")

    print("sample output:")
    ni = 0
    nli = len(newlist) // 50
    for word in newlist:
        if ni % nli == 0:
            print(f'"{word}",')
        ni += 1

    print(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"{lower}-{upper}_letter_words", newlist)


def process_args():
    arg_parser = ArgumentParser(description="get the save-to-file, lower and upper limits options", prog="python3.11 choose_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-l', '--lower', type=int, default=DEFAULT_LENGTH, help="minimum number of letters in the words")
    arg_parser.add_argument('-u', '--upper', type=int, default=MAX_LENGTH, help="maximum number of letters in the words")
    return arg_parser


def prep_choose(argl:list) -> (bool, str, str):
    args = process_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    low = args.lower if MIN_LENGTH <= args.lower <= MAX_LENGTH else DEFAULT_LENGTH
    show(f"lower limit = {low}")

    up = args.upper if low <= args.upper <= MAX_LENGTH else MAX_LENGTH
    show(f"upper limit = {up}")

    return args.save, low, up


if __name__ == '__main__':
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    save_option, lower, upper = prep_choose(argv[1:])
    run_choose()
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
