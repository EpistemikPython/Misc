##############################################################################################################################
# coding=utf-8
#
# letter_frequencies.py -- get the frequency of each letter in words of specified lengths from a word file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2023-10-30"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
ORDERED_LETTERS = "SEAORILTNUDYCPMHGBKFWVZJXQ"
MIN_LOWER = 5
MAX_UPPER = 15

def main_words():
    """get the frequency of each letter in words of specified length(s) from a word file"""
    freqs = dict.fromkeys(ORDERED_LETTERS, 0)
    wct = lct = 0
    scp = json.load(open(WORD_FILE))
    for item in scp:
        if lower <= len(item) <= upper:
            for letter in item:
                freqs[letter] += 1
                lct += 1
            wct += 1

    print(f"word count = {wct}")
    print(f"letter count = {lct}")
    rev_freqs = {}
    sorted_freqs = {}
    print(f"letter frequencies:")
    for key in freqs.keys():
        print(f"\t{key}: {freqs[key]}")
        rev_freqs[freqs[key]] = key

    print(f"\nsorted letter frequencies:")
    for val in sorted(rev_freqs, reverse = True):
        print(f"\t{rev_freqs[val]}: {val}")
        sorted_freqs[rev_freqs[val]] = val

    print(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json(f"{lower}-{upper}_letter_frequencies", sorted_freqs)


if __name__ == "__main__":
    print(f"word file = '{WORD_FILE}'")
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    print(f"save option = '{save_option}'")

    lower = MIN_LOWER
    if len(argv) > 2:
        request = int(argv[2])
        if MAX_UPPER > request > MIN_LOWER:
            print(f"requested lower size = {request}")
            lower = request
    upper = lower
    if len(argv) > 3:
        request = int(argv[3])
        if MAX_UPPER >= request > MIN_LOWER:
            print(f"requested upper size = {request}")
            upper = request
    if lower > upper:
        lower = upper - 1
    print(f"lower word size = {lower}")
    print(f"upper word size = {upper}\n")

    main_words()
    print(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
