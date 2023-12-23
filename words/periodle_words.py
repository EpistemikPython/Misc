###################################################################################################################################################
# coding=utf-8
#
# periodle_words.py -- process a words file to find periodle words (5-10 letters using element symbols) and optionally save results to a JSON file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-12-18"
__updated__ = "2023-12-23"

import os
import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, JSON_LABEL
from mhsLogging import MhsLogger

start = time.perf_counter()
INPUT_FOLDER = "input"
WORD_JSON_FILE = "test2" # "periodle_words"
ELEMENT_JSON_FILE = "periodic_table"
BLANK = '_'
MIN_LETTERS = 5
MAX_LETTERS = MIN_LETTERS * 2

def solve():
    wd_ct = 0
    wdf = json.load( open(word_file) )
    for item in wdf:
        wd_ct += 1
        wd_len = len(item)
        if MAX_LETTERS >= wd_len >= MIN_LETTERS:
            drop = False
            sg_poss = 0
            for lx in item:
                if lx.upper() in singles:
                    sg_poss += 1
            sg_reqd = MAX_LETTERS - wd_len
            if sg_reqd > sg_poss:
                continue
            retry = False
            stack = []
            step = 0
            sg_ct = 0
            dg_reqd = wd_len - MIN_LETTERS
            dg_ct = 0
            prev_lett = BLANK
            # pop each accepted symbol on a stack
            # if reach a failure point: REWIND to the most recent single and use it and the next letter as a double
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
                lgr.info(stack)
    show(f"{wd_ct} words in word file.")

def run_periodle():
    """process a words file to find periodle words (5-10 letters using element symbols) and save to a JSON file"""

    solve()
    num_wd = len(prd_list)
    show(f"periodle word count = {num_wd}\n")

    ni = 0
    nli = num_wd // 32 if num_wd > 150 else 12 if num_wd > 30 else 1
    # display a selection of the output
    show("sample solutions:")
    for word in prd_list:
        if ni % nli == 0:
            show(word)
        ni += 1

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"periodle-words_f-{get_base_filename(word_file)}", prd_list)

def get_symbols():
    symf = json.load( open(symbol_file) )
    for sect in symf:
        if sect == "single":
            for symbol in symf[sect]:
                singles.append(symbol.upper())
        elif sect == "double":
            for symbol in symf[sect]:
                doubles.append(symbol.upper())
    lgr.debug(f"singles = {singles}")
    lgr.debug(f"doubles = {doubles}")

def process_args():
    arg_parser = ArgumentParser(description="get the save-to-file, 'symbols file' name and 'words file' name options", prog="python3.11 periodle_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-y', '--symbolfile', type=str, default=ELEMENT_JSON_FILE,
                                help= "JSON file name with the symbols to use (.json added to file name)")
    arg_parser.add_argument('-w', '--wordfile', type=str, default=WORD_JSON_FILE,
                                help= "JSON file name with the words to test (.json added to file name)")
    return arg_parser

def prep_sb(argl:list) -> (bool, str, str):
    args = process_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    symbols = args.symbolfile if args.symbolfile.isprintable() else ELEMENT_JSON_FILE
    symbols = INPUT_FOLDER + os.sep + symbols + os.extsep + JSON_LABEL
    show(f"symbol file = {symbols}")

    words = args.wordfile if args.wordfile.isprintable() else WORD_JSON_FILE
    words = INPUT_FOLDER + os.sep + words + os.extsep + JSON_LABEL
    show(f"word file = {words}")

    return args.save, symbols, words


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__) )
    lgr = log_control.get_logger()
    show = log_control.show

    save_option, symbol_file, word_file = prep_sb(argv[1:])
    code = 0
    singles = []
    doubles = []
    prd_list = []
    try:
        get_symbols()
        run_periodle()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem = '{repr(ex)}'")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
