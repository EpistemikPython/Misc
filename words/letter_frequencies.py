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
__updated__ = "2023-12-11"

import time
import json
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from mhsLogging import MhsLogger, get_base_filename

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
ALL_LETTERS = "SEAORILTNUDYCPMHGBKFWVZJXQ"
MIN_WORD_LEN = 5
MAX_WORD_LEN = 15

def run_freqs(save_option:bool, lower:int, upper:int):
    """get the frequency of each letter in words of specified length(s) from a word file"""
    freqs = dict.fromkeys(ALL_LETTERS, 0)
    wct = lct = 0
    wds = json.load( open(WORD_FILE) )
    for item in wds:
        if lower <= len(item) <= upper:
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
        save_to_json(f"{lower}-{upper}_letter-frequencies", sorted_freqs)

def process_args():
    arg_parser = ArgumentParser(description="get the save-to-file, word size, required letters and possible letters options", prog="ideal_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-n', '--minimum', type=int, default=MIN_WORD_LEN, help="minimum number of letters in each found word")
    arg_parser.add_argument('-x', '--maximum', type=int, default=MAX_WORD_LEN, help="maximum number of letters in each found word")
    return arg_parser

def prep_freqs(argl:list) -> (bool, int, int):
    args = process_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    min_size = args.minimum if MIN_WORD_LEN <= args.minimum <= MAX_WORD_LEN else MIN_WORD_LEN
    show(f"minimum word size = {min_size}")

    max_size = args.maximum if min_size <= args.maximum <= MAX_WORD_LEN else min_size
    show(f"maximum word size = {max_size}")

    return args.save, min_size, max_size


if __name__ == "__main__":
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    save, minf, maxf = prep_freqs(argv[1:])
    run_freqs( save, minf, maxf )
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
