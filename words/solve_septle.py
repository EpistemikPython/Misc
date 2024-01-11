###################################################################################################################################################
# coding=utf-8
#
# solve_septle.py -- solve a septle-type game with information about the fixed, required and excluded symbols
# see https://septle.com
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-01-10"
__updated__ = "2024-01-11"

import os
import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, JSON_LABEL
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

start = time.perf_counter()
INPUT_FOLDER = "input"
WORD_JSON_FILE = "seven-letter_words"
BLANK = '_'
DEFAULT_WORD_LENGTH = 7
MIN_WORD_LENGTH = 4
MAX_WORD_LENGTH = 15

def solve():
    """
    A simple and fast 'brute force' method.
    Check all the possible septle words:
      for fixed symbols in the proper positions
      for the presence of required symbols
      for the absence of excluded symbols
      - and retain the words that fulfill all these criteria
    """
    wdf = json.load( open(word_file) )
    for it in wdf:
        item = it.upper()
        drop = False
        # can use a boolean 'have_fixed' to skip this step if no fixed symbols, but doesn't make any noticeable difference to the runtime
        for fr in range( len(form) ):
            if not drop and form[fr] != BLANK:
                if item[fr] != form[fr]:
                    lgr.debug(f"MISSING fixed symbol '{form[fr]}' in '{item}' at position '{fr}'!")
                    drop = True
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
    """solve a septle-type game with information about the fixed, required and excluded symbols"""

    solve()
    num_wd = len(solution_list)
    show(f"\nFound {num_wd} septle solutions.\n")
    # display a selection of the output
    skip = 10 if num_wd > 150 else 5 if num_wd > 30 else 1
    show(f"{'Sample' if skip >= 5 else 'All'} solutions:")
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
        exstr = ''.join(map(str, excluded)) if required else '0'
        lgr.debug(f"exstr = {exstr}")
        save_to_json(f"septle-solutions_f-{fixstr}_r-{reqstr}_x-{exstr}", solution_list)

def set_args():
    arg_parser = ArgumentParser(description="solve a septle-type game with information about the fixed, required and excluded symbols",
                                prog="python3 solve_septle.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-l', '--length', type=int, default=DEFAULT_WORD_LENGTH, help= "length of the word to find")
    arg_parser.add_argument('-f', '--fixed', type=str, help= "csv list of location and letter where the position and value are KNOWN, e.g. 1f,3p")
    arg_parser.add_argument('-r', '--required', type=str, help= "csv list of required letters with an unknown position, e.g. c,l,a")
    arg_parser.add_argument('-x', '--exclude', type=str, help= "csv list of symbols that DO NOT appear in the game, eg. i,v,e,y,w,s")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    leng = args.length if MIN_WORD_LENGTH <= args.length <= MAX_WORD_LENGTH else DEFAULT_WORD_LENGTH
    argform = dict.fromkeys( (r for r in range(leng)), BLANK)
    show(f"argform = {argform}")

    fixed = args.fixed.upper().split(sep=',') if args.fixed else []
    show(f"fixed = {fixed}")
    if fixed:
        for fi in fixed:
            if fi[0].isnumeric():
                posn = int(fi[0])-1
                if posn < DEFAULT_WORD_LENGTH:
                    lett = fi[1:]
                    if lett.isalphabetic():
                        argform[posn] = lett
    show(f"form = {argform}")

    require = args.required.upper().split(sep=',') if args.required else []
    show(f"required = {require}")

    exclude = args.exclude.upper().split(sep=',') if args.exclude else []
    show(f"excluded = {exclude}")

    return args.save, argform, require, exclude


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__), file_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    show = log_control.show

    try:
        save_option, form, required, excluded = prep_args(argv[1:])

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
