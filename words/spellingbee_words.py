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
__updated__ = "2023-10-30"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
DEFAULT_OUTER_LETTERS = "CONLAY"
GROUP_SIZE = len(DEFAULT_OUTER_LETTERS)
DEFAULT_REQD_LETTER = "I"
MIN_WORD_SIZE = 4

def main_sb():
    """find all words from a list that fulfill the specified spelling bee requirements"""
    solutions = []
    sct = 0
    spj = json.load( open(WORD_FILE) )
    for item in spj:
        if len(item) >= MIN_WORD_SIZE:
            for letter in item:
                if not( letter in group + required ):
                    break
            else:
                if required in item:
                    solutions.append(item)
                    sct += 1

    print(f"solution count = {sct}")
    # check for pangrams and print the solutions
    pgct = 0
    print(f"solutions:")
    for val in solutions:
        pg = True
        for lett in group:
            if not lett in val:
                pg = False
                break
        if pg:
            print(f"\t{val} : Pangram!")
            pgct += 1
        else:
            print(f"\t{val}")
    if pgct == 0:
        print(">> NO Pangrams!!")

    print(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json(f"{required}-{group}_spellingbee_words", solutions)


if __name__ == '__main__':
    print(f"word file = '{WORD_FILE}'")
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    print(f"save option = '{save_option}'")

    required = DEFAULT_REQD_LETTER
    if len(argv) > 2:
        request = argv[2]
        if len(request) == 1 and request.isalpha():
            print(f"requested mandatory letter = {request}")
            required = request.upper()
    print(f"required letter = {required}")
    # make sure the required letter is not among the outer letters?
    group = DEFAULT_OUTER_LETTERS
    if len(argv) > 3:
        request = argv[3]
        if len(request) == GROUP_SIZE and request.isalpha():
            # make sure all the letters are different?
            print(f"requested outer letters = {request}")
            group = request.upper()
    print(f"outer letters = {group}")

    main_sb()
    print(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
