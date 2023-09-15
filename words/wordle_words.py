##############################################################################################################################
# coding=utf-8
#
# wordle_words.py -- process a words dict to find wordle (5-letter) words and save to a separate file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-09-15"
__updated__ = "2023-09-15"

from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from scrabble_words_2019 import scrabble

def main_wordle(save_option:str):
    print(f"save option = '{save_option}'\n")
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

    save_option = save_option.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("wordle_words", newlist)


if __name__ == '__main__':
    save_opt = 'No'
    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]
    main_wordle(save_opt)
    exit()
