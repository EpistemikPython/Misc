##############################################################################################################################
# coding=utf-8
#
# json_test.py -- see the dictionary details inside a json file and find the listed words and save to a new file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-06-01"
__updated__ = "2024-06-02"

import time
import json
from sys import path
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
TEST_FILE = "/home/marksa/Documents/Words/SpellBeeWords.json"

def run():
    """see the dictionary details inside a json file and find the listed words and save to a new file"""
    word_list = []
    sbd = json.load( open(TEST_FILE) )
    for item in sbd:
        current_dict = sbd[item]
        if 'answers' in current_dict.keys():
            words = current_dict['answers']
        else:
            words = current_dict['data']['answers']
        print(f"{item}: {words}")
        for wd in words:
            lowd = wd.lower()
            if lowd not in word_list:
                word_list.append(lowd)

    save_to_json("sb_json", word_list)


if __name__ == '__main__':
    code = 0
    try:
        run()
    except KeyboardInterrupt:
        print(">> User interruption.")
        code = 13
    except Exception as ex:
        print(f"Problem: '{repr(ex)}'")
        code = 66

    print(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
