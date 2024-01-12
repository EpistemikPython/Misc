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
SIXLETTER_WORD_FILE = "six-letter_words"
SEVENLETTER_WORD_FILE = "seven-letter_words"
DEFAULT_WORD_FILE = "scrabble-plus"
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
    wdf = json.load( open(file_location) )
    for it in wdf:
        if len(it) == word_length:
            item = it.upper()
            drop = False
            # can use a boolean 'have_fixed' to skip this step if no fixed symbols, but doesn't make any noticeable difference to the runtime
            for fr in range(word_length):
                if form[fr] != BLANK and item[fr] != form[fr]:
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
        reqstr = required if required else '0'
        lgr.debug(f"reqstr = {reqstr}")
        exstr = excluded if excluded else '0'
        lgr.debug(f"exstr = {exstr}")
        save_name = f"septle-solutions_f-{fixstr}_r-{reqstr}_x-{exstr}"
        save_to_json(save_name, solution_list)
        show(f"Save output to file '{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="solve a septle-type game with information about the fixed, required and excluded symbols",
                                prog="python3 solve_septle.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-l', '--length', type=int, default=DEFAULT_WORD_LENGTH, help="length of the word to find")
    arg_parser.add_argument('-f', '--fixed', type=str, help="csv list of location and letter where the position and value are KNOWN, e.g. 1f,3p")
    arg_parser.add_argument('-r', '--required', type=str, help="required letters with an unknown position, e.g. cla")
    arg_parser.add_argument('-x', '--exclude', type=str, help="letters that DO NOT appear in the word, eg. iveyws")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    leng = args.length if MIN_WORD_LENGTH <= args.length <= MAX_WORD_LENGTH else DEFAULT_WORD_LENGTH
    argform = dict.fromkeys( (r for r in range(leng)), BLANK )
    show(f"argform = {argform}")

    fixed = args.fixed.upper().split(sep=',') if args.fixed else []
    show(f"fixed = {fixed}")
    if fixed:
        for fi in fixed:
            if fi[0].isnumeric():
                posn = int(fi[0])-1
                if posn < leng:
                    lett = fi[1]
                    if lett.isalpha():
                        argform[posn] = lett
    show(f"fixed form = {argform}")

    require = args.required.upper() if args.required else ""
    show(f"required = {require}")

    exclude = args.exclude.upper() if args.exclude else ""
    show(f"excluded = {exclude}")

    return args.save, argform, require, exclude


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__), file_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    show = log_control.show

    try:
        save_option, form, required, excluded = prep_args(argv[1:])

        word_length = len(form)
        json_word_file = SEVENLETTER_WORD_FILE if word_length == 7 else SIXLETTER_WORD_FILE if word_length == 6 else DEFAULT_WORD_FILE
        file_location = INPUT_FOLDER + os.sep + json_word_file + os.extsep + JSON_LABEL
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
