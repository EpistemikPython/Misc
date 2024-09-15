###################################################################################################################################################
# coding=utf-8
#
# solve_wordle.py
#   -- solve a wordle game with information about the fixed, hindered and excluded symbols
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-09-14"
__updated__ = "2024-09-15"

import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, osp
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

start = time.perf_counter()
DEFAULT_WORD_FILE = "input/five-letter_words.json"
BLANK = '_'
DEFAULT_WORD_LENGTH = 7
WORD_LENGTH = 5

def solve():
    """
    A simple and fast 'brute force' method.
    Check all the possible five-letter words:
      for fixed symbols in the proper positions
      for the presence of hindered symbols but NOT in the hindered positions
      for the absence of excluded symbols
      - and retain the words that fulfill all these criteria
    """
    wdf = json.load( open(input_file) )
    for it in wdf:
        if len(it) == WORD_LENGTH:
            item = it.upper()
            drop = False
            for itl in range(WORD_LENGTH):
                if fixed_form[itl] and item[itl] != fixed_form[itl]:
                    lgr.debug(f"MISSING fixed symbol '{fixed_form[itl]}' in '{item}' at position: {itl}!")
                    drop = True
                    break
                if hindered_form[itl]:
                    for hl in hindered_form[itl]:
                        if hl not in item or item[itl] == hl:
                            lgr.debug(f"hindered symbol '{hl}' not in '{item}' or at forbidden position '{itl}'!")
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
    """solve a wordle game with information about the fixed, hindered and excluded symbols"""
    solve()
    num_wd = len(solution_list)
    lgr.info(f"\nFound {num_wd} septle solutions.\n")
    # display a selection of the output
    skip = 10 if num_wd > 150 else 5 if num_wd > 30 else 1
    lgr.info(f"{'Sample' if skip >= 5 else 'All'} solutions:")
    ni = 0
    for word in solution_list:
        ni += 1
        if ni % skip == 0:
            lgr.info(word)

    lgr.info(f"\nSolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        fixstr = fixed_form.replace(',') if fixed_form else '0'
        lgr.debug(f"fixstr = {fixstr}")
        hindstr = hindered_form.replace(',') if hindered_form else '0'
        lgr.debug(f"hindstr = {hindstr}")
        exstr = excluded if excluded else '0'
        lgr.debug(f"exstr = {exstr}")
        save_name = f"wordle-solutions_f-{fixstr}_h-{hindstr}_x-{exstr}"
        save_to_json(save_name, solution_list)
        lgr.info(f"Saved output to file '{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="solve a septle-type game with information about the fixed, required and excluded symbols",
                                prog="python3 solve_septle.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-w', '--words', type=str, default = DEFAULT_WORD_FILE,
                            help = f"path to JSON file with list of all acceptable words; DEFAULT = '{DEFAULT_WORD_FILE}'")
    arg_parser.add_argument('-f', '--fixed', type=str,
                            help="csv list of location and letter where the position and value are KNOWN, i.e green letters, e.g. 1f,3p")
    arg_parser.add_argument('-h', '--hindered', type=str,
                            help="csv list of location and letter where the letter is in the soluton "
                                 "but HINDERED at one or more positions, i.e. yellow letters, e.g. 1t,4ue")
    arg_parser.add_argument('-x', '--exclude', type=str, help="letters that DO NOT appear in the soluton, e.g. iveyws")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    lgr.info(f"save option = '{args.save}'")

    fform = []
    fixed = args.fixed.upper().split(sep=',') if args.fixed else []
    lgr.info(f"fixed = {fixed}")
    if fixed:
        for fi in fixed:
            if fi[0].isnumeric():
                posn = int(fi[0])-1
                if posn < WORD_LENGTH:
                    lett = fi[1]
                    if lett.isalpha():
                        fform.append(lett)
        lgr.info(f"fixed form = {fform}")

    hform = [ [] for _ in range(WORD_LENGTH) ]
    hindered = args.hindered.upper().split(sep=',') if args.hindered else []
    lgr.info(f"hindered = {hindered}")
    if hindered:
        for hi in hindered:
            if hi[0].isnumeric():
                posn = int(hi[0])-1
                if posn < WORD_LENGTH:
                    for lett in hi:
                        if lett.isalpha():
                            hform[posn].append(lett)
        lgr.info(f"hindered form = {hform}")

    exclude = args.exclude.upper() if args.exclude else ""
    lgr.info(f"excluded = {exclude}")

    return args.save, args.words, fform, hform, exclude


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()

    code = 0
    solution_list = []
    try:
        save_option, words_file, fixed_form, hindered_form, excluded = get_args(argv[1:])
        input_file = words_file if osp.isfile(words_file) else DEFAULT_WORD_FILE
        run()
    except KeyboardInterrupt:
        lgr.info(">> User interruption.")
        code = 13
    except Exception as ex:
        lgr.info(f"Problem = '{repr(ex)}'")
        code = 66

    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
