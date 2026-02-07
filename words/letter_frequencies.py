##############################################################################################################################
# coding=utf-8
#
# letter_frequencies.py
# -- get the total number of times each letter is found and the number of words each letter appears in,
#    in words of a specified length from a specified word list
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2026-02-06"

import string
import time
from argparse import ArgumentParser
from collections import defaultdict
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_WORD_FILE = "input/scrabble-plus.json"
MIN_WORD_LEN     =  4
DEFAULT_WORD_LEN =  5
MAX_WORD_LEN     = 15

def run():
    """Get the total number of times each letter is found and the number of words each letter appears in,
       in words of a specified length from a specified word list."""
    freqs = dict.fromkeys(string.ascii_uppercase, 0) # total number of times each letter is found
    appearances = dict.fromkeys(string.ascii_uppercase, 0) # number of words each letter appears in
    word_count = 0
    letter_count = 0
    wds = json.load( open(word_file) )
    for item in wds:
        seen = []
        if min_size <= len(item) <= max_size:
            for letter in item:
                freqs[letter] += 1
                if letter not in seen:
                    appearances[letter] += 1
                seen.append(letter)
                letter_count += 1
            word_count += 1

    lgr.info(f"\tword count = {word_count}")
    lgr.info(f"\tletter count = {letter_count}\n")

    lett_freqs = defaultdict(str) # dict {freqs -> letter}
    total_freqs = 0
    lgr.info(f"\n\tletter frequencies:")
    for key in freqs.keys():
        lgr.info(f"\t{key}: {freqs[key]}")
        total_freqs += freqs[key]
        # concatenate letters in case there are any identical frequencies
        lett_freqs[freqs[key]] += key
    lgr.info(f"total letter frequencies = {total_freqs}")

    sorted_freqs = {}
    for item in sorted(lett_freqs, reverse = True):
        sorted_freqs[lett_freqs[item]] = item
    lgr.info(f"\n\tsorted letter frequencies:")
    for key in sorted_freqs.keys():
        lgr.info(f"\t{key}: {sorted_freqs[key]}")

    lett_appears = defaultdict(str) # dict {appearances -> letter}
    total_appears = 0
    lgr.info(f"\n\tletter appearances:")
    for key in appearances.keys():
        lgr.info(f"\t{key}: {appearances[key]}")
        total_appears += appearances[key]
        # concatenate letters in case there are any identical appearance totals
        lett_appears[appearances[key]] += key
    lgr.info(f"total letter appearances = {total_appears}")

    sorted_appears = {}
    for val in sorted(lett_appears, reverse = True):
        sorted_appears[lett_appears[val]] = val
    lgr.info(f"\n\tsorted letter appearances:")
    for key in sorted_appears.keys():
        lgr.info(f"\t{key}: {sorted_appears[key]}")

    if save_option:
        lgr.info(f"\nsolve and display elapsed time = {time.perf_counter() - start} seconds.")
        save_dict = {"Letter totals":sorted_freqs, "Letter appearances":sorted_appears}
        saved_file = save_to_json(f"{min_size}-{max_size}_letter-freqs-appears", save_dict)
        lgr.info(f"\n\t Saved results to '{saved_file}'.")

def set_args():
    arg_parser = ArgumentParser(description = "Get the total number of times each letter is found "
                                              "and the number of words each letter appears in, "
                                              "in words of a specified length from a specified word list.",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_true", default = False,
                            help = "Save the results to a JSON file.")
    arg_parser.add_argument('-i', '--input', type = str, metavar = "inPATH", default = DEFAULT_WORD_FILE,
                            help = f"Path to a file with the list of words to use; DEFAULT = '{DEFAULT_WORD_FILE}'.")

    arg_parser.add_argument('-n', '--minimum', type = int, default = DEFAULT_WORD_LEN,
                            help = f"MINIMUM number of letters in each word used, "
                                   f"SMALLEST = {MIN_WORD_LEN}, DEFAULT = {DEFAULT_WORD_LEN}.")
    arg_parser.add_argument('-x', '--maximum', type = int, default = MIN_WORD_LEN,
                            help = f"MAXIMUM number of letters in each word used, "
                                   f"LARGEST = {MAX_WORD_LEN}, DEFAULT = {DEFAULT_WORD_LEN}.")
    return arg_parser

def get_args(argl:list):
    args_log_level = DEFAULT_LOG_LEVEL
    args = set_args().parse_args(argl)

    lgr.log(args_log_level, f"save option = '{args.save}'.")

    if osp.isfile(args.input):
        infile = args.input
        lgr.log(args_log_level, f"input file = '{infile}'.")
    else:
        infile = DEFAULT_WORD_FILE
        lgr.warning(f">> BAD input file = '{args.input}'!! >> Using default file = '{infile}'.")

    lower = args.minimum if MIN_WORD_LEN <= args.minimum <= MAX_WORD_LEN else DEFAULT_WORD_LEN
    lgr.log(args_log_level, f"minimum word size = {lower}")

    upper = args.maximum if lower <= args.maximum <= MAX_WORD_LEN else lower
    lgr.log(args_log_level, f"maximum word size = {upper}\n")

    return args.save, infile, lower, upper


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, word_file, min_size, max_size = get_args(argv[1:])
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
