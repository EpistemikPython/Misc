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
__updated__ = "2023-10-31"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
import mhsLogging

log_control = mhsLogging.MhsLogger(mhsLogging.get_base_filename(__file__))
lgr = log_control.get_logger()
lgr.warning("START LOGGING")
show = log_control.show

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
ALL_LETTERS = "SEAORILTNUDYCPMHGBKFWVZJXQ"
MIN_WORD_LEN = 5
MAX_WORD_LEN = 15

def main_freqs():
    """get the frequency of each letter in words of specified length(s) from a word file"""
    freqs = dict.fromkeys(ALL_LETTERS, 0)
    wct = lct = 0
    scp = json.load( open(WORD_FILE) )
    for item in scp:
        if lower <= len(item) <= upper:
            for letter in item:
                freqs[letter] += 1
                lct += 1
            wct += 1

    show(f"word count = {wct}")
    show(f"letter count = {lct}")
    rev_freqs = {}
    sorted_freqs = {}
    show(f"letter frequencies:")
    for key in freqs.keys():
        show(f"\t{key}: {freqs[key]}")
        # hopefully there are not two frequencies exactly the same
        rev_freqs[freqs[key]] = key

    show(f"\nsorted letter frequencies:")
    for val in sorted(rev_freqs, reverse = True):
        show(f"\t{rev_freqs[val]}: {val}")
        sorted_freqs[rev_freqs[val]] = val

    show(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json(f"{lower}-{upper}_letter_frequencies", sorted_freqs)


if __name__ == "__main__":
    show(f"word file = '{WORD_FILE}'")
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    show(f"save option = '{save_option}'")

    lower = MIN_WORD_LEN
    if len(argv) > 2:
        request = int(argv[2])
        if MAX_WORD_LEN >= request > MIN_WORD_LEN:
            show(f"requested lower size = {request}")
            lower = request
    show(f"lower word size = {lower}")
    upper = lower
    if len(argv) > 3:
        request = int(argv[3])
        if MAX_WORD_LEN >= request > lower:
            show(f"requested upper size = {request}")
            upper = request
    show(f"upper word size = {upper}\n")

    main_freqs()
    show(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
