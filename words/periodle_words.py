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
__updated__ = "2023-12-19"

import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

WORD_FILE = "test.json" # "scrabble-plus.json"
ELEMENT_FILE = "periodic_table.json"
BLANK = '_'

def solve_periodle(singles:list, doubles:list):
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        wd_len = len(item)
        if 10 >= wd_len >= 5:
            drop = False
            dg_num = wd_len - 5
            dg_ct = 0
            sg_num = 5 - dg_num
            sg_ct = 0
            # scan the entire word and find all the indices of singles,
            # then find all the combinations of the required number of singles with the rest as dg's
            # i.e. KERATINS = 8 letters, = 3 dg + 2 sg, and has sg's at [0,5,6,7]
            # so try sg's at [0,5], ([0,6] NOT possible!) [0,7], ([5,6],[5,7] NOT possible!) and [6,7]
            # i.e. the letter groups around and between the singles ALL have to be even-numbered.
            prev_lett = BLANK
            for lett in item:
                if dg_ct > dg_num or sg_ct > sg_num:
                    drop = True
                    break
                if prev_lett != BLANK:
                    digraph = prev_lett + lett
                    if digraph not in doubles:
                        drop = True
                        break
                    else:
                        dg_ct += 1
                        prev_lett = BLANK
                else:
                    if lett in singles:
                        sg_ct += 1
                        if sg_ct > sg_num:
                            prev_lett = lett
                            sg_ct -= 1
                        continue
                    else:
                        prev_lett = lett
            if not drop:
                prd_list.append(item)
            else:
                first_lett = item[0]
                second_lett = item[1]
                first_dg = item[:2]
                if first_lett in singles and second_lett in singles and first_dg in doubles:
                    possibles.append(item)

def run_periodle():
    """process a words file to find periodle (5-10 letter) words and save to a separate file"""
    print(f"save option = '{save_option}'\n")

    single = []
    double = []
    elf = json.load( open(ELEMENT_FILE) )
    for sect in elf:
        print(sect)
        if sect == "single":
            for symbol in elf[sect]:
                single.append(symbol)
        elif sect == "double":
            for symbol in elf[sect]:
                double.append(symbol.upper())
    print(f"singles = {single}")
    print(f"doubles = {double}")

    solve_periodle(single, double)
    print(f"possibles = {possibles}")

    num_wd = len(prd_list)
    print(f"periodle word count = {num_wd}\n")
    ni = 0
    nli = num_wd // 11 if num_wd > 150 else 5
    # display a selection of the output
    print("sample output:")
    for word in prd_list:
        if ni % nli == 0:
            print(word)
        ni += 1

    if save_option.upper()[0] == 'Y':
        save_to_json("periodle_words", prd_list)


if __name__ == '__main__':
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]

    prd_list = []
    possibles = []
    run_periodle()
    exit()
