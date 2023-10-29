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
__updated__ = "2023-10-29"

import time
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from scrabble_words_2019 import scrabble

start = time.perf_counter()
DEFAULT_LENGTH = 5
MIN_LENGTH = 2
MAX_LENGTH = 15

def main_choose(save_option:str):
    print(f"save option = '{save_option}'\n")
    newlist = []
    ix = 0
    for item in scrabble.keys():
        if lower <= len(item) <= upper:
            newlist.append(item)
            ix += 1
    print(f"word count = {ix}\n")

    ni = 0
    nli = ix // 50
    for word in newlist:
        if ni % nli == 0:
            print(f"word list includes '{word}'")
        ni += 1

    print(f"\nelapsed time = {time.perf_counter() - start}")
    save_option = save_option.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json(f"{lower}-{upper}_letter_words", newlist)


if __name__ == '__main__':
    save_opt = 'No'
    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]

    lower = DEFAULT_LENGTH
    upper = DEFAULT_LENGTH
    if len(argv) > 2:
        request = int(argv[2])
        print(f"requested lower word size = {request}")
        if MIN_LENGTH <= request < MAX_LENGTH:
            lower = request
    if len(argv) > 3:
        request = int(argv[3])
        print(f"requested upper word size = {request}")
        if MIN_LENGTH < request <= MAX_LENGTH:
            upper = request
    if lower > upper:
        lower = upper-1
    print(f"lower word size = {lower}")
    print(f"upper word size = {upper}")

    main_choose(save_opt)
    print(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
