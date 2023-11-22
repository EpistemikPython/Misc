##############################################################################################################################
# coding=utf-8
#
# ideal_words.py -- from a word list find all the words that contain only the specified letters
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-11-22"
__updated__ = "2023-11-22"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, get_filename
from mhsLogging import MhsLogger

log_control = MhsLogger(get_base_filename(__file__))
lgr = log_control.get_logger()
lgr.warning("START LOGGING")
show = log_control.show

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
DEFAULT_OUTER_LETTERS = "CONLAY"
GROUP_SIZE = len(DEFAULT_OUTER_LETTERS)
DEFAULT_REQD_LETTER = "I"
MIN_WORD_SIZE = 4

def main_ideal():
    """from a word list find all the words that contain only the specified letters"""
    solutions = []
    sct = 0
    sbw = json.load( open(WORD_FILE) )
    for item in sbw:
        if len(item) >= MIN_WORD_SIZE:
            for letter in item:
                if letter not in group + required:
                    break
            else:
                if required in item:
                    solutions.append(item)
                    sct += 1

    show(f"solution count = {sct}")
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
    show(f">> {pgct} Pangram{'' if pgct == 1 else 's'}{'!' * pgct}")

    show(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json(f"{required}-{group}_spellbee_words", solutions)


if __name__ == '__main__':
    if len(argv) <= 1:
        show(f"Usage: Python3.n[6+] {get_filename(argv[0])} save-option[Yes|No] required-letter[e.g. X] group-letters[e.g. MHSRED]")
        exit(66)

    show(f"word file = '{WORD_FILE}'")
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    show(f"save option = '{save_option}'")

    required = DEFAULT_REQD_LETTER
    if len(argv) > 2:
        request = argv[2]
        if len(request) == 1 and request.isalpha():
            show(f"requested mandatory letter = {request}")
            required = request.upper()
    show(f"required letter = {required}")
    # make sure the required letter is not among the outer letters?
    group = DEFAULT_OUTER_LETTERS
    if len(argv) > 3:
        request = argv[3]
        if len(request) == GROUP_SIZE and request.isalpha():
            # make sure all the letters are different?
            show(f"requested outer letters = {request}")
            group = request.upper()
    show(f"outer letters = {group}")

    main_ideal()
    show(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
