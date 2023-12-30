###################################################################################################################################################
# coding=utf-8
#
# periodle_solve.py -- solve a periodle game
# see https://heptaveegesimal.com/periodle/
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-12-29"
__updated__ = "2023-12-29"

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
WORD_JSON_FILE = "periodle_words"
ELEMENT_JSON_FILE = "periodic_table"
BLANK = '_'
NUM_SYMBOLS = 5
MAX_LETTERS = NUM_SYMBOLS * 2

def solve():
    """
    a simple brute force method:
    check all the possible periodle words:
      for fixed symbols in the proper positions
      for the presence of required symbols
      for the absence of excluded symbols
      - and retain the words that fulfill all the criteria
    """
    wdf = json.load( open(word_file) )
    for item in wdf:
        drop = False
        for r in range(NUM_SYMBOLS):
            if form[r] != BLANK:
                idx = r * 2
                if item[idx:idx+len(form[r])] != form[r]:
                    lgr.debug(f"MISSING fixed symbol '{form[r]}' at position#{idx} in '{item}'!")
                    drop = True
                    break
        if not drop:
            if required:
                for ri in required:
                    if ri.upper() not in item:
                        lgr.debug(f"MISSING required symbol '{ri}' in '{item}'!")
                        drop = True
                        break
        if not drop:
            if excluded:
                for xi in excluded:
                    if xi.upper() in item:
                        lgr.debug(f"excluded symbol '{xi}' FOUND in '{item}'!")
                        drop = True
                        break
        if not drop:
            solution_list.append(item)

def run():
    """process a words file to find periodle words (5-10 letters using element symbols) and save to a JSON file"""

    solve()
    num_wd = len(solution_list)
    show(f"\nFound {num_wd} periodle words.\nsolve elapsed time = {time.perf_counter() - start}")

    if save_option:
        save_to_json(f"periodle-solutions_f-{get_base_filename(word_file)}", solution_list)
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
    symf = json.load( open(INPUT_FOLDER + os.sep + ELEMENT_JSON_FILE + os.extsep + JSON_LABEL) )
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
    arg_parser = ArgumentParser(description="get the save-to-file plus the fixed, required, partial and exclude options", prog="python3 periodle_solve.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-f', '--fixed', type=str, help= "csv list of location and symbol where the position and value are KNOWN, e.g. 1fe,3p")
    arg_parser.add_argument('-r', '--required', type=str, help= "csv list of required symbols with an unknown position, e.g. c,la")
    arg_parser.add_argument('-p', '--partial', type=str, help= "csv list of partial symbols, e.g. ar,h")
    arg_parser.add_argument('-x', '--exclude', type=str, help= "csv list of symbols that DO NOT appear in the game, eg. i,v,er,y,w,se")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    fixed = args.fixed.split(sep=',') if args.fixed else []
    show(f"fixed = {fixed}")
    if fixed:
        for fi in fixed:
            if fi[0].isnumeric():
                posn = int(fi[0])-1
                # show(f"posn = {posn}")
                if posn < NUM_SYMBOLS:
                    sym = fi[1:].upper()
                    # show(f"sym = {sym}")
                    if sym in singles or sym in doubles:
                        form[posn] = sym
    show(f"form = {form}")

    require = args.required.split(sep=',') if args.required else []
    show(f"required = {require}")

    partial = args.partial.split(sep=',') if args.partial else []
    show(f"partial = {partial}")

    require = require + partial
    show(f"required + partial = {require}")

    exclude = args.exclude.split(sep=',') if args.exclude else []
    show(f"exclude = {exclude}")
    # for exi in exclude:
    #     exiu = exi.upper()
    #     if exiu in singles:
    #         singles.remove(exiu)
    #         for item in doubles:
    #             if exiu in item:
    #                 doubles.remove(item)
    #     elif exiu in doubles:
    #         doubles.remove(exiu)
    # show(f"adjusted singles = {singles}")
    # show(f"adjusted doubles = {doubles}")
    # show(f"size adj doubles = {len(doubles)}")

    return args.save, require, exclude


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__) )
    lgr = log_control.get_logger()
    show = log_control.show

    try:
        form = {0:BLANK,1:BLANK,2:BLANK,3:BLANK,4:BLANK}
        singles = []
        doubles = []
        get_symbols()
        save_option, required, excluded = prep_args(argv[1:])
        word_file = INPUT_FOLDER + os.sep + WORD_JSON_FILE + os.extsep + JSON_LABEL

        code = 0
        solution_list = []
        run()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem = '{repr(ex)}'")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
