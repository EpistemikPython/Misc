##############################################################################################################################
# coding=utf-8
#
# periodle_words.py -- process a words file to find periodle (5-10 letter) words and save to a separate file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-12-18"
__updated__ = "2023-12-18"

import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

WORD_FILE = "scrabble-plus.json"

def run_periodle():
    """process a words file to find periodle (5-10 letter) words and save to a separate file"""

    print(f"save option = '{save_option}'\n")
    prd_list = []
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        if 10 >= len(item) >= 5:
            prd_list.append(item)

    num_wd = len(prd_list)
    print(f"periodle word count = {num_wd}\n")

    ni = 0
    nli = num_wd // 50 if num_wd > 150 else 5
    # display a selection of the output
    for word in prd_list:
        if ni % nli == 0:
            print(f"periodle word list includes '{word}'")
        ni += 1

    if save_option.upper()[0] == 'Y':
        save_to_json("periodle_words", prd_list)


if __name__ == '__main__':
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    run_periodle()
    exit()
