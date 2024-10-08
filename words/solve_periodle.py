###################################################################################################################################################
# coding=utf-8
#
# solve_periodle.py
#   -- solve a periodle game with information about fixed, required, partial and excluded symbols
# see https://heptaveegesimal.com/periodle/
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-12-29"
__updated__ = "2024-08-19"

import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

start = time.perf_counter()
WORD_JSON_FILE = "input/periodle_words.json"
ELEMENT_JSON_FILE = "input/periodic_table.json"
BLANK = '_'
NUM_SYMBOLS = 5

def solve():
    """
    A simple and fast 'brute force' method (but which does find some words that DO NOT meet the exact criteria).
    Check all the possible periodle words:
      for fixed symbols in the proper positions
      for the presence of required symbols
      for the absence of excluded symbols
      - and retain the words that fulfill all these criteria
    """
    wdf = json.load( open(WORD_JSON_FILE) )
    for it in wdf:
        item = it.upper()
        drop = False
        # can use a boolean 'have_fixed' to skip this step if no fixed symbols, but doesn't make any noticeable difference to the runtime
        for r in range(NUM_SYMBOLS):
            if not drop and form[r] != BLANK:
                # IDEA: keep track of preceding symbols and whether single or double to get a better estimate of possible positions
                drop = True
                # fixed symbols may be in different positions in the word, depending on number of singles or doubles preceding
                for idx in range(r, 2*r+1):
                    if item[idx:idx+len(form[r])] == form[r]:
                        lgr.debug(f"FOUND fixed symbol '{form[r]}' at position#{idx} in '{item}'.")
                        drop = False
                        break
        if not drop and required:
            for ri in required:
                if ri not in item:
                    lgr.debug(f"MISSING required symbol '{ri}' in '{item}'!")
                    drop = True
                    break
        if not drop and excluded:
            for xi in excluded:
                if xi in item:
                    lgr.debug(f"excluded symbol '{xi}' FOUND in '{item}'!")
                    drop = True
                    break
        if not drop:
            solution_list.append(item)

def run():
    """solve a periodle game with information about fixed, required, partial and excluded symbols"""
    get_symbols()
    solve()
    num_wd = len(solution_list)
    show(f"\nFound {num_wd} periodle words.\n")
    # display a selection of the output
    skip = 10 if num_wd > 150 else 5 if num_wd > 30 else 1
    show(f"{'Sample' if skip >= 5 else 'All'} tentative solutions:")
    ni = 0
    for word in solution_list:
        ni += 1
        if ni % skip == 0:
            show(word)

    show(f"\nSolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        formstr = ''.join(map(str, form.values())).replace(BLANK, '')
        fixstr = formstr if formstr.isalpha() else '0'
        lgr.debug(f"fixstr = {fixstr}")
        reqstr = ''.join(map(str, required)) if required else '0'
        lgr.debug(f"reqstr = {reqstr}")
        exstr = ''.join(map(str, excluded)) if excluded else '0'
        lgr.debug(f"exstr = {exstr}")
        save_name = f"periodle-solutions_f-{fixstr}_r-{reqstr}_x-{exstr}"
        save_to_json(save_name, solution_list)
        show(f"Save output to file '{save_name}'.")

def get_symbols():
    """default input is the periodic table JSON file"""
    symf = json.load( open(ELEMENT_JSON_FILE) )
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
    arg_parser = ArgumentParser(description="solve a periodle game with information about fixed, required, partial and excluded symbols",
                                prog=f"python3 {argv[0]}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help = "Write the results to a JSON file")
    arg_parser.add_argument('-f', '--fixed', type=str, help = "csv list of location and symbol where the position and value are KNOWN, e.g. 1fe,3p")
    arg_parser.add_argument('-r', '--required', type=str, help = "csv list of required symbols with an unknown position, e.g. c,la")
    arg_parser.add_argument('-p', '--partial', type=str, help = "csv list of partial symbols, e.g. ar,h")
    arg_parser.add_argument('-x', '--exclude', type=str, help = "csv list of symbols that DO NOT appear in the game, e.g. i,v,er,y,w,se")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    fixed = args.fixed.upper().split(sep=',') if args.fixed else []
    show(f"fixed = {fixed}")
    if fixed:
        for fi in fixed:
            if fi[0].isnumeric():
                posn = int(fi[0])-1
                if posn < NUM_SYMBOLS:
                    sym = fi[1:]
                    if sym in singles or sym in doubles:
                        form[posn] = sym
    show(f"form = {form}")

    require = args.required.upper().split(sep=',') if args.required else []
    # IDEA: keep separate track of partial and check before and after symbols in the solve loop to make sure actually 'partial'
    partial = args.partial.upper().split(sep=',') if args.partial else []
    require = require + partial
    show(f"required + partial = {require}")
    # find any adjacent fixed symbols that can be concatenated and added to the required symbols
    concat3 = BLANK
    span = NUM_SYMBOLS-1
    for r in range(span):
        if form[r] != BLANK and form[r+1] != BLANK:
            if r < span-1 and form[r+2] != BLANK:
                concat3 = form[r] + form[r+1] + form[r+2]
                require.append(concat3)
                show(f"appended '{concat3}' to required = {require}")
            else:
                concat2 = form[r] + form[r+1]
                if concat2 not in concat3:
                    require.append(concat2)
                    show(f"appended '{concat2}' to required = {require}")

    exclude = args.exclude.upper().split(sep=',') if args.exclude else []
    show(f"exclude = {exclude}")

    return args.save, require, exclude


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__), file_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    show = log_control.show

    code = 0
    solution_list = []
    singles = []
    doubles = []
    try:
        form = dict.fromkeys((r for r in range(NUM_SYMBOLS)), BLANK)
        save_option, required, excluded = prep_args(argv[1:])
        run()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem = '{repr(ex)}'")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
