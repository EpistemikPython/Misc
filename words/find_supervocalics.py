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
__updated__ = "2024-08-04"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import MhsLogger

start = time.perf_counter()
INPUT_FILE = "input/scrabble-plus.json"
VOWELS = "AEIOU"
MIN_WORD_SIZE = 6
MAX_PRINT = 30

def run():
    """from a word list file, find all the supervocalics"""
    solutions = [[],[]]
    wdf = json.load( open(file_name) )
    for item in wdf:
        if len(item) >= MIN_WORD_SIZE:
            for vowel in VOWELS:
                if item.count(vowel) != 1:
                    break
            else:
                # save SupervocalickYs separately
                if item.count("Y") == 1:
                    solutions[0].append(item)
                else:
                    solutions[1].append(item)

    num_solys = len(solutions[0])
    num_solns = len(solutions[1])
    total_solns = num_solys + num_solns
    show(f"Total solution count = {total_solns}\nSupervocalickY count = {num_solys}")
    solutions[0].sort()
    solutions[1].sort()

    # display some of the solutions
    yskip = 1 if num_solys <= MAX_PRINT else num_solys // MAX_PRINT + 1
    show(f"yskip = {yskip}")
    yct = 0
    show(f"{'Sample of' if yskip > 1 else 'ALL'} SupervocalickYs:")
    for yval in solutions[0]:
        yct += 1
        if yct % yskip == 0:
            show(f"\t{yval}")
    show(f">> {yct if yct > 0 else 'NO'} SupervocalickY{'' if yct == 1 else 's'}!\n")
    skip = 1 if num_solns <= MAX_PRINT else num_solns // MAX_PRINT + 1
    show(f"skip = {skip}")
    show(f"{'Sample of' if skip > 1 else 'ALL'} solutions:")
    ct = 0
    for val in solutions[1]:
        ct += 1
        if ct % skip == 0:
            show(f"\t{val}")
    show(f"\nsolve, sort and display elapsed time = {time.perf_counter() - start}")

    if save_option:
        save_dict = {f"{list_name}":solutions}
        save_name = save_to_json("Supervocalics", save_dict)
        show(f"Saved output to file '{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="from a word list file, find all the supervocalics and supervocalickYs",
                                prog=f"python3 {get_filename(__file__)}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-n', '--name', type=str, default=get_current_date(),
                            help="if saving results to a file, optional name for the list of results")
    arg_parser.add_argument('-f', '--file', type=str, default=INPUT_FILE,
                            help=f"path to a file with a list of candidate words; DEFAULT = '{INPUT_FILE}'")
    return arg_parser

def prep_args(argl:list):
    args = set_args().parse_args(argl)

    show(f"save option = {args.save}")
    if args.save:
        show(f"saved results list name = '{args.name}'.")

    if not osp.isfile(args.file):
        raise Exception(f"File path '{args.file}' does not exist.")
    show(f"using word file '{args.file}'")

    return args.save, args.name, args.file


if __name__ == '__main__':
    log_control = MhsLogger(get_base_filename(__file__))
    show = log_control.show

    code = 0
    try:
        save_option, list_name, file_name = prep_args(argv[1:])
        run()
    except KeyboardInterrupt:
        show(">> User interruption.")
        code = 13
    except Exception as ex:
        show(f"Problem: {repr(ex)}.")
        code = 66

    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
