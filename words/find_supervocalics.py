##############################################################################################################################
# coding=utf-8
#
# find_supervocalics.py -- from a word list file, find all the supervocalics
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-06-25"
__updated__ = "2024-06-25"

import time
import json
from argparse import ArgumentParser
import os.path as osp
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, get_current_date
from mhsLogging import MhsLogger

start = time.perf_counter()
WORD_FILE = "input/scrabble-plus.json"
VOWELS = "AEIOU"
MIN_WORD_SIZE = 6
MAX_PRINT = 30

def run():
    """from a word list file, find all the supervocalics"""
    solutions = []
    wdf = json.load( open(file_name) )
    for item in wdf:
        if len(item) >= MIN_WORD_SIZE:
            for vowel in VOWELS:
                if item.count(vowel) != 1:
                    break
            else:
                solutions.append(item)

    num_solns = len(solutions)
    show(f"solution count = {num_solns}")
    # print some of the solutions
    skip = 1 if num_solns <= MAX_PRINT else num_solns // MAX_PRINT + 1
    show(f"skip = {skip}")
    ct = 0
    show(f"{'Sample of' if skip > 1 else 'ALL'} solutions:")
    for val in solutions:
        ct += 1
        if ct % skip == 0:
            show(f"\t{val}")

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_dict = {f"{dict_name}":solutions}
        save_name = save_to_json("Supervocalics", save_dict)
        show(f"Saved output to file '{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="from a word list file, find all the supervocalics", prog="python3 find_supervocalics.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-n', '--name', type=str, default=get_current_date(),
                            help="if saving results to a file, optional name for list of results")
    arg_parser.add_argument('-f', '--file', type=str, default=WORD_FILE,
                            help=f"path to file with list of all acceptable words; DEFAULT = '{WORD_FILE}'")
    return arg_parser

def prep_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = {args.save}")
    if args.save:
        show(f"saved results dictionary name = {args.name}")

    if not osp.isfile(args.file):
        raise Exception(f"File path '{args.file}' does not exist.")
    show(f"using word file '{args.file}'")

    return args.save, args.name, args.file


if __name__ == '__main__':
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    code = 0
    try:
        save_option, dict_name, file_name = prep_args(argv[1:])
        run()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem: {repr(ex)}.")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
