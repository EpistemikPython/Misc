##############################################################################################################################
# coding=utf-8
#
# letter_frequencies.py -- get the frequency of each letter in words of specified length(s) from a word list
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2023-12-28"

import time
import json
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from mhsLogging import MhsLogger, get_base_filename

start = time.perf_counter()
WORD_FILE = "input/scrabble-plus.json"
ALL_LETTERS = "SEAORILTNUDYCPMHGBKFWVZJXQ"
MIN_WORD_LEN = 5
MAX_WORD_LEN = 15

def run_freqs():
    """get the frequency of each letter in words of specified length(s) from a word file"""
    freqs = dict.fromkeys(ALL_LETTERS, 0)
    wct = lct = 0
    wds = json.load( open(WORD_FILE) )
    for item in wds:
        if min_size <= len(item) <= max_size:
            for letter in item:
                freqs[letter] += 1
                lct += 1
            wct += 1

    show(f"word count = {wct}")
    show(f"letter count = {lct}")

    rev_freqs = {}
    show(f"letter frequencies:")
    for key in freqs.keys():
        show(f"\t{key}: {freqs[key]}")
        # hopefully there are not two frequencies exactly the same
        rev_freqs[freqs[key]] = key

    sorted_freqs = {}
    show(f"\nsorted letter frequencies:")
    for val in sorted(rev_freqs, reverse = True):
        show(f"\t{rev_freqs[val]}: {val}")
        sorted_freqs[rev_freqs[val]] = val

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"{min_size}-{max_size}_letter-frequencies", sorted_freqs)

def process_args():
    arg_parser = ArgumentParser(description="get the save-to-file, minimum and maximum word size options", prog="python3 letter_frequencies.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-n', '--minimum', type=int, default=MIN_WORD_LEN, help="minimum number of letters in each found word")
    arg_parser.add_argument('-x', '--maximum', type=int, default=MAX_WORD_LEN, help="maximum number of letters in each found word")
    return arg_parser

def prep_freqs(argl:list) -> (bool, int, int):
    args = process_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    lower = args.minimum if MIN_WORD_LEN <= args.minimum <= MAX_WORD_LEN else MIN_WORD_LEN
    show(f"minimum word size = {lower}")

    upper = args.maximum if lower <= args.maximum <= MAX_WORD_LEN else lower
    show(f"maximum word size = {upper}")

    return args.save, lower, upper


if __name__ == "__main__":
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    save_option, min_size, max_size = prep_freqs(argv[1:])
    run_freqs()
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
