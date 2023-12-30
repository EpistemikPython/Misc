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
__updated__ = "2023-12-27"

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
WORD_JSON_FILE = "test3" # "periodle_words"
ELEMENT_JSON_FILE = "periodic_table"
BLANK = '_'
MIN_LETTERS = 5
MAX_LETTERS = MIN_LETTERS * 2

def solve():
    """
        pop each accepted symbol on a stack
        - if reach a failure point: REWIND to the most recent accepted single and try it and the following letter as a digraph
          and resume from there...
    """
    wd_ct = 0
    wdf = json.load( open(word_file) )
    for it in wdf:
        item = it.upper()
        wd_ct += 1
        wd_len = len(item)
        if MAX_LETTERS >= wd_len >= MIN_LETTERS:
            sg_poss = 0
            for lx in item:
                if lx in singles:
                    sg_poss += 1
            sg_reqd = MAX_LETTERS - wd_len
            # quick initial test
            if sg_reqd > sg_poss:
                rejects.append(item)
                continue
            drop = False
            retry = False
            step = 0
            sg_ct = 0
            dg_reqd = wd_len - MIN_LETTERS
            dg_ct = 0
            stack = []
            prev_lett = BLANK
            while step < wd_len and not drop:
                lett = item[step]
                if prev_lett != BLANK:
                    digraph = prev_lett + lett
                    if digraph not in doubles:
                        if step > 1: # beyond the first two letters
                            retry = True
                        else: # first letter NOT in singles or NO solution if used as a single and first digraph NOT in doubles
                            drop = True
                    else:
                        stack.append(digraph)
                        prev_lett = BLANK
                        dg_ct += 1
                        if dg_ct > dg_reqd:
                            # always try singles FIRST, so if reached too many digraphs, current word CANNOT be a solution
                            lgr.debug(f"digraph count violation with '{item}'.")
                            drop = True
                else:
                    if lett in singles:
                        sg_ct += 1
                        if sg_ct > sg_reqd:
                            prev_lett = lett
                            sg_ct -= 1
                        else:
                            stack.append(lett)
                    else:
                        if step == wd_len - 1: # if reach this point, the last letter is REQUIRED to be a single, so...
                            lgr.debug(f"Last letter of '{item}' NOT in singles!")
                            drop = True
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
                if len(stack) != 5: # should NEVER happen, but just in case
                    lgr.error(f"Problem with stack '{stack}' for word '{item}'?!")
                else:
                    solution_list.append(item)
                    stack_dict[wd_ct] = stack
                    lgr.info(stack)
            else:
                rejects.append(item)
    show(f"\n{wd_ct} words in input file.")

def run_periodle():
    """process a words file to find periodle words (5-10 letters using element symbols) and save to a JSON file"""

    solve()
    num_wd = len(solution_list)
    show(f"Found {num_wd} periodle words.\n{len(rejects)} words in rejects file.\nsolve elapsed time = {time.perf_counter() - start}")

    if save_option:
        save_to_json(f"periodle-solutions_f-{get_base_filename(word_file)}", solution_list)
        save_to_json(f"periodle-rejects_f-{get_base_filename(word_file)}", rejects)
        save_to_json(f"periodle-stack_f-{get_base_filename(word_file)}", stack_dict)
    else:
        # display a selection of the output
        show("\nsample solutions:")
        ni = 0
        nli = num_wd // 32 if num_wd > 150 else 12 if num_wd > 30 else 1
        for word in solution_list:
            if ni % nli == 0:
                show(word)
            ni += 1

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

def set_args():
    arg_parser = ArgumentParser(description="get the save-to-file, 'symbols file' name and 'words file' name options", prog="python3 periodle_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-y', '--symbolfile', type=str, default=ELEMENT_JSON_FILE,
                                help= "JSON file name with the symbols to use (.json added to file name)")
    arg_parser.add_argument('-w', '--wordfile', type=str, default=WORD_JSON_FILE,
                                help= "JSON file name with the words to test (.json added to file name)")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

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

    save_option, symbol_file, word_file = prep_args(argv[1:])
    code = 0
    rejects = []
    solution_list = []
    stack_dict = {}
    singles = []
    doubles = []
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
