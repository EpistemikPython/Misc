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
__updated__ = "2023-12-22"

import json
import time
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
WORD_FILE = "test2.json" # "periodle_words.json"
ELEMENT_FILE = "periodic_table.json"
BLANK = '_'

def solve():
    print(f"Word file = {WORD_FILE}")
    wd_ct = 0
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        wd_ct += 1
        wd_len = len(item)
        if 10 >= wd_len >= 5:
            drop = False
            sg_poss = 0
            for lx in item:
                if lx.upper() in singles:
                    sg_poss += 1
            sg_reqd = 10 - wd_len
            if sg_reqd > sg_poss:
                continue
            retry = False
            stack = []
            step = 0
            sg_ct = 0
            dg_reqd = wd_len - 5
            dg_ct = 0
            prev_lett = BLANK
            # pop all the accepted symbols on a stack
            # if reach an end: REWIND to the most recent single and use it and the next letter as a double
            # and resume from there...
            while step < wd_len and not drop:
                lett = item[step].upper()
                if dg_ct > dg_reqd or sg_ct > sg_reqd:
                    drop = True
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
                    else:
                        if step == wd_len - 1: # at the last letter
                            step += 1 # correct for the decrement in retry
                            retry = True
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
                else:
                    step += 1
            if not drop:
                prd_list.append(item.upper())
                print(stack)
    print(f"{wd_ct} words in word file.")

def run_periodle():
    """process a words file to find periodle (5-10 letter) words and save to a separate file"""
    print(f"save option = '{save_option}'\n")

    solve()

    num_wd = len(prd_list)
    print(f"periodle word count = {num_wd}\n")
    ni = 0
    nli = num_wd // 11 if num_wd > 150 else 5 if num_wd > 30 else 1
    # display a selection of the output
    print("sample output:")
    for word in prd_list:
        if ni % nli == 0:
            print(word)
        ni += 1

    print(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json("periodle_words", prd_list)

def get_symbols():
    elf = json.load( open(ELEMENT_FILE) )
    for sect in elf:
        if sect == "single":
            for symbol in elf[sect]:
                singles.append(symbol)
        elif sect == "double":
            for symbol in elf[sect]:
                doubles.append(symbol.upper())
    print(f"singles = {singles}")
    print(f"doubles = {doubles}")


if __name__ == '__main__':
    # logging
    # ArgParser
    
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]

    code = 0
    try:
        singles = []
        doubles = []
        get_symbols()

        prd_list = []
        run_periodle()
    except KeyboardInterrupt:
        print(">> User interruption.")
    except Exception as ex:
        print(f"Problem = '{repr(ex)}'")
        code = 66

    print(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
