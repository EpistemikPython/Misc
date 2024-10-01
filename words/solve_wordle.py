###################################################################################################################################################
# coding=utf-8
#
# solve_wordle.py
#   -- solve a wordle game with information about the fixed, hindered and excluded letters
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-09-14"
__updated__ = "2024-09-30"

import logging
import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, osp, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_WORD_FILE = "input/five-letter_words.json"
BLANK = '_'
WORD_LENGTH = 5

def solve(p_loglev:int):
    """
    A simple and fast 'brute force' method.
    Check each candidate five-letter word:
      for fixed letters in the proper positions
      for the presence of hindered letters but NOT in the hindered positions
      for the absence of excluded letters
    >> retain the words that fulfill all these criteria
    """
    solution_list = []
    wdf = json.load( open(input_file) )
    for it in wdf:
        if len(it) == WORD_LENGTH:
            item = it.upper()
            lgr.log(p_loglev, f"\n\t\t\t\t\t\ttesting {item}")
            drop = False
            for wpn in range(WORD_LENGTH):
                if not drop and fixed_form[wpn] != BLANK and item[wpn] != fixed_form[wpn]:
                    lgr.log(p_loglev, f"MISSING fixed symbol '{fixed_form[wpn]}' in '{item}' at position: {wpn+1}!")
                    drop = True
                    break
                if not drop and hindered_form[wpn]:
                    for hlt in hindered_form[wpn]:
                        if hlt not in item or item[wpn] == hlt:
                            lgr.log(p_loglev, f"hindered symbol '{hlt}' not in '{item}' or at forbidden position {wpn+1}!")
                            drop = True
                            break
            if not drop and excluded:
                for xi in excluded:
                    if xi in item:
                        lgr.log(p_loglev, f"excluded symbol '{xi}' FOUND in '{item}'!")
                        drop = True
                        break
            if not drop:
                lgr.info(f"{item}: Success!")
                solution_list.append(item)
    return solution_list

def run(p_loglev:int):
    """solve a wordle game with information about the fixed, hindered and excluded letters"""
    solutions = solve(logging.NOTSET)
    num_wd = len(solutions)
    lgr.log(p_loglev, f"\nFound {num_wd} solutions.\n")
    # display a selection of the output
    skip = 10 if num_wd > 150 else 5 if num_wd > 30 else 1
    lgr.log(p_loglev, f"{'Sample' if skip >= 5 else 'All'} solutions:")
    ni = 0
    for word in solutions:
        ni += 1
        if ni % skip == 0:
            lgr.log(p_loglev, word)

    if save_option:
        lgr.info(f"\nSolve and display elapsed time = {time.perf_counter()-start}")
        fixstr = fixed_str.replace(',','')
        hindstr = hindered_str.replace(',','')
        exstr = excluded if excluded else '0'
        lgr.log(p_loglev, f"fixstr = {fixstr}, hindstr = {hindstr}, exstr = {exstr}")
        save_name = f"wordle-solutions_f-{fixstr}_h-{hindstr}_x-{exstr}"
        save_to_json(save_name, solutions)
        lgr.info(f"Saved output to file '{save_name}'.")

def get_forms(p_loglev:int, p_fixed:str, p_hindered:str):
    fform = [ BLANK for _ in range(WORD_LENGTH) ]
    fixed = p_fixed.split(sep=',') if p_fixed else []
    lgr.log(logging.DEBUG, f"fixed = {fixed}")
    if fixed:
        for fi in fixed:
            if fi[0].isnumeric():
                posn = int(fi[0])-1
                if posn < WORD_LENGTH:
                    lett = fi[1]
                    if lett.isalpha():
                        fform[posn] = lett
        lgr.log(p_loglev, f"fixed form = {fform}")

    hform = [ [] for _ in range(WORD_LENGTH) ]
    hindered = p_hindered.split(sep=',') if p_hindered else []
    lgr.log(logging.DEBUG, f"hindered = {hindered}")
    if hindered:
        for hi in hindered:
            if hi[0].isnumeric():
                posn = int(hi[0])-1
                if posn < WORD_LENGTH:
                    for lett in hi:
                        if lett.isalpha():
                            hform[posn].append(lett)
        lgr.log(p_loglev, f"hindered form = {hform}")

    return fform, hform

def set_args():
    arg_parser = ArgumentParser(description="solve a wordle game with information about the fixed, hindered and excluded letters",
                                prog=f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-w', '--wordfile', type=str, default = DEFAULT_WORD_FILE,
                            help = f"path to JSON file with list of all acceptable words; DEFAULT = '{DEFAULT_WORD_FILE}'")
    arg_parser.add_argument('-f', '--fixed', type=str,
                            help="csv list of location & letter where both are KNOWN (i.e. green hilited squares) e.g. '5n' or '1p,3r'")
    arg_parser.add_argument('-d', '--hindered', type=str,
                            help="csv list of location & letter where the letter IS IN the solution "
                                 "but HINDERED at one or more positions (i.e. yellow hilited squares) e.g. '2w,3w' or '1t,4mu'")
    arg_parser.add_argument('-x', '--exclude', type=str, help="letters that ARE NOT in the solution, e.g. 'iveyls'")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    loglev = logging.INFO

    lgr.log(loglev, f"save option = '{args.save}'")

    lgr.log(loglev, f"fixed = {args.fixed}")
    fixed = args.fixed.upper() if args.fixed else ""

    lgr.log(loglev, f"hindered = {args.hindered}")
    hindered = args.hindered.upper() if args.hindered else ""

    lgr.log(loglev, f"excluded = {args.exclude}")
    exclude = args.exclude.upper() if args.exclude else ""

    return args.save, args.wordfile, fixed, hindered, exclude


if __name__ == '__main__':
    start = time.perf_counter()
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, words_file, fixed_str, hindered_str, excluded = get_args(argv[1:])
        input_file = words_file if osp.isfile(words_file) else DEFAULT_WORD_FILE
        fixed_form, hindered_form = get_forms(logging.DEBUG, fixed_str, hindered_str)
        run(logging.INFO)
    except KeyboardInterrupt:
        lgr.exception(">> User interruption.")
        code = 13
    except ValueError:
        lgr.exception(">> Value Error.")
        code = 27
    except Exception as mex:
        lgr.exception(f">> PROBLEM: {repr(mex)}")
        code = 66

    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start} seconds")
    exit(code)
