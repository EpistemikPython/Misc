##############################################################################################################################
# coding=utf-8
#
# words.py -- get the length of each item in a words dict
#
# Copyright (c) 2022 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2022-02-15"
__updated__ = "2023-01-12"

from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from words_2019 import eng_words

def main_words(save_option:str):
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

    save_option = save_option.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("len_words", newdict)


if __name__ == '__main__':
    save_opt = 'No'
    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]
    main_words(save_opt)
    exit()
