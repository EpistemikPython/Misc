##############################################################################################################################
# coding=utf-8
#
# get_wordle_words.py
#   -- process a words dict to find wordle (5-letter) words and save to a separate file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-09-15"
__updated__ = "2024-08-19"

from sys import path, argv
import time
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
path.append("./input")
from scrabble_words_2019 import scrabble

start = time.perf_counter()

def run():
    newlist = []
    ix = 0
    for item in scrabble.keys():
        if len(item) == 5:
            newlist.append(item)
            ix += 1

    print(f"wordle count = {ix}\n")

    ni = 0
    nli = ix // 50
    for word in newlist:
        if ni % nli == 0:
            print(f"newlist includes {word}")
        ni += 1

    save_option = save_opt.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("wordle_words", newlist)


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
