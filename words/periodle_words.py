##############################################################################################################################
# coding=utf-8
#
# periodle_words.py -- process a words file to find periodle (5-10 letters made up of 5 element symbols) words and save to a separate file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-12-18"
__updated__ = "2023-12-20"

import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

WORD_FILE = "test1.json" # "scrabble-plus.json"
ELEMENT_FILE = "periodic_table.json"
BLANK = '_'

def solve_periodle():
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        wd_len = len(item)
        if 10 >= wd_len >= 5:
            drop = False
            sg_num = 10 - wd_len
            sg_ct = 0
            dg_num = wd_len - 5
            dg_ct = 0
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

def solve_p2():
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        wd_len = len(item)
        if 10 >= wd_len >= 5:
            drop = False
            # pop all the accepted symbols on a stack
            # if reach an end: REWIND to the most recent single and use it and the next letter as a double
            # and continue from there...
            sg_locs = []
            for lx in range(wd_len):
                if item[lx] in singles:
                    sg_locs.append(lx)
            print(f"single locations = {sg_locs}")
            sg_poss = len(sg_locs)
            sg_reqd = 10 - wd_len
            if sg_poss < sg_reqd:
                continue
            retry = False
            stack = []
            step = 0
            sg_ct = 0
            dg_reqd = wd_len - 5
            dg_ct = 0
            prev_lett = BLANK
            while step < wd_len:
                lett = item[step]
                if dg_ct > dg_reqd or sg_ct > sg_reqd:
                    # drop = True
                    continue # break
                if prev_lett != BLANK:
                    digraph = prev_lett + lett
                    if digraph not in doubles:
                        if step > 1:
                            retry = True
                        else:
                            drop = True
                            break
                    else:
                        stack.append(digraph)
                        dg_ct += 1
                        prev_lett = BLANK
                else:
                    if lett in singles:
                        sg_ct += 1
                        if sg_ct > sg_reqd:
                            prev_lett = lett
                            sg_ct -= 1
                        else:
                            stack.append(lett)
                        # continue
                    else:
                        prev_lett = lett
                if retry:
                    retry = False
                    step -= 1
                    while len(stack) > 0 and len(stack[-1]) == 2:
                        stack.pop()
                        dg_ct -= 1
                        step -= 2
                    if len(stack) > 0:
                        prev_lett = stack.pop()
                        sg_ct -= 1
                    else:
                        drop = True
                        # break
                else:
                    step += 1
            if not drop:
                prd_list.append(item)

def run_periodle():
    """process a words file to find periodle (5-10 letter) words and save to a separate file"""
    print(f"save option = '{save_option}'\n")

    solve_p2()
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

def get_symbols():
    elf = json.load( open(ELEMENT_FILE) )
    for sect in elf:
        print(sect)
        if sect == "single":
            for symbol in elf[sect]:
                singles.append(symbol)
        elif sect == "double":
            for symbol in elf[sect]:
                doubles.append(symbol.upper())
    print(f"singles = {singles}")
    print(f"doubles = {doubles}")


if __name__ == '__main__':
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    code = 0
    try:
        singles = []
        doubles = []
        get_symbols()

        prd_list = []
        possibles = []
        run_periodle()
    except KeyboardInterrupt:
        print(">> User interruption.")
    except Exception as ex:
        print(f"Problem = '{repr(ex)}'")
        code = 66

    exit(code)
