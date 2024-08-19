###################################################################################################################################################
# coding=utf-8
#
# get_periodle_words.py
#   -- process a words file to find periodle words (5-10 letters using element symbols) and optionally save results to a JSON file
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-12-18"
__updated__ = "2024-08-19"

import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from mhsLogging import *

start = time.perf_counter()
WORD_JSON_FILE = "input/test3.json" # "periodle_words"
ELEMENT_JSON_FILE = "input/periodic_table.json"
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
                            lgr.logl(f"digraph count violation with '{item}'.", logging.DEBUG)
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
                            lgr.logl(f"Last letter of '{item}' NOT in singles!", logging.DEBUG)
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
                    lgr.logl(f"Problem with stack '{stack}' for word '{item}'?!", logging.ERROR)
                else:
                    solution_list.append(item)
                    stack_dict[wd_ct] = stack
                    lgr.logl(repr(stack))
            else:
                rejects.append(item)
    show(f"\n{wd_ct} words in input file.")

def run():
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
    lgr.logl(f"singles = {singles}", logging.DEBUG)
    lgr.logl(f"doubles = {doubles}", logging.DEBUG)

def set_args():
    arg_parser = ArgumentParser(description="get the save-to-file, 'symbols file' name and 'words file' name options",
                                prog=f"python3 {argv[0]}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-y', '--symbolfile', type=str, default = ELEMENT_JSON_FILE,
                            help = f"JSON file name with the symbols to use; DEFAULT = {ELEMENT_JSON_FILE}")
    arg_parser.add_argument('-w', '--wordfile', type=str, default = WORD_JSON_FILE,
                            help = f"JSON file name with the words to test; DEFAULT = {WORD_JSON_FILE}")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.logl("START LOGGING")
    show(f"save option = '{args.save}'")

    if not osp.isfile(args.symbolfile):
        raise Exception(f"File path '{args.symbolfile}' does not exist.")
    show(f"Using symbols file '{args.symbolfile}'")

    if not osp.isfile(args.wordfile):
        raise Exception(f"File path '{args.wordfile}' does not exist.")
    show(f"Using word file '{args.wordfile}'")

    return args.save, args.symbolfile, args.wordfile


if __name__ == '__main__':
    lgr = MhsLogger( get_base_filename(__file__) )
    show = lgr.show

    code = 0
    rejects = []
    solution_list = []
    stack_dict = {}
    singles = []
    doubles = []
    try:
        save_option, symbol_file, word_file = prep_args(argv[1:])
        get_symbols()
        run()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem = '{repr(ex)}'")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
