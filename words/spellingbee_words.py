##############################################################################################################################
# coding=utf-8
#
# spellingbee_words.py -- find all words from a list that fulfill the specified spelling bee requirements
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2023-10-29"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
DEFAULT_OUTER_LETTERS = "CONLAY"
GROUP_SIZE = len(DEFAULT_OUTER_LETTERS)
DEFAULT_REQD_LETTER = "I"
solutions = []
MIN_WORD_SIZE = 4

def main_sb():
    sct = 0
    scp = json.load(open("scrabble-plus.json"))
    for item in scp:
        if len(item) >= MIN_WORD_SIZE:
            for letter in item:
                if not (letter in DEFAULT_OUTER_LETTERS + DEFAULT_REQD_LETTER):
                    break
            else:
                if DEFAULT_REQD_LETTER in item:
                    solutions.append(item)
                    sct += 1

    print(f"solution count = {sct}")
    print(f"solutions = {solutions}")
    # rev_freqs = {}
    # print(f"\nsorted letter frequencies:")
    # for val in sorted(rev_freqs, reverse = True):
    #     print(f"{rev_freqs[val]}: {val}")

    global save_option
    save_option = save_option.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("letter_frequencies", solutions)


if __name__ == '__main__':
    save_option = 'No'
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]

    group = DEFAULT_OUTER_LETTERS
    required = DEFAULT_REQD_LETTER
    if len(argv) > 2:
        request = argv[2]
        if len(request) == 1 and request.isalpha():
            print(f"requested necessary letter = {request}")
            required = request
    if len(argv) > 3:
        request = argv[3]
        if len(request) == GROUP_SIZE and request.isalpha():
            print(f"requested outer letters = {request}")
            group = request
    print(f"required letter = {required}")
    print(f"outer letters = {group}")

    main_sb()
    print(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
