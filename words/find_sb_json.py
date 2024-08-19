##############################################################################################################################
# coding=utf-8
#
# find_sb_json.py
#   -- open a spellingbee results json file and find the listed words and save to a new file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-06-01"
__updated__ = "2024-08-19"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
WORD_FILE = "/home/marksa/Documents/Words/SpellingBee/SpellBeeWords.json"
WORD_KEY = "answers"
DATA_KEY = "data"

def run():
    """open a spellingbee results json file and find the listed words and save to a new file"""
    word_list = []
    sbd = json.load( open(WORD_FILE) )
    for item in sbd:
        current_dict = sbd[item]
        if WORD_KEY in current_dict.keys():
            words = current_dict[WORD_KEY]
        else:
            words = current_dict[DATA_KEY][WORD_KEY]
        if save_opt == 'DEBUG':
            print(f"{item}: {words}")
        for wd in words:
            lowd = wd.lower()
            if lowd not in word_list:
                word_list.append(lowd)

    save_option = save_opt.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("sb_json", word_list)


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
