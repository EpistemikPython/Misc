##############################################################################################################################
# coding=utf-8
#
# get_word_length.py
#   -- get the length of each item in a words dict
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2022-02-15"
__updated__ = "2024-08-19"

from sys import path, argv
import time
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
path.append("./input")
from words_2019 import eng_words

start = time.perf_counter()

def run():
    newdict = {}
    ie = 0
    for item in eng_words:
        newdict[item] = len(item)
        ie += 1

    print(f"words count = {ie}\n")

    ni = 0
    np = 0
    for item in newdict:
        ni += 1
        if ni % 1313 == 0:
            # some miscellaneous entries
            print(f"newdict[{item}] = {newdict[item]}")
            np += 1
        if np > 66:
            break

    save_option = save_opt.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("len_words", newdict)


if __name__ == '__main__':
    code = 0
    try:
        save_opt = 'No'
        if len(argv) > 1:
            save_opt = argv[1]
        if save_opt.isalpha():
            run()
            print(f"\nfinal elapsed time = {time.perf_counter()-start}")
        else:
            print(f"usage: python3 {argv[0]} [yes (save results to json file)]")
    except KeyboardInterrupt:
        print(">> User interruption.")
        code = 13
    except Exception as ex:
        print(f"Problem >> '{repr(ex)}'")
        code = 66
    exit(code)
