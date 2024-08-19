##############################################################################################################################
# coding=utf-8
#
# find_length_words.py
#   -- process a list of words to find words of the specified lengths and optionally save to a JSON file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2024-08-18"

import time
import json
import os.path as osp
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, JSON_LABEL, get_base_filename
from mhsLogging import MhsLogger

start = time.perf_counter()
DEFAULT_WORD_FILE = "input/scrabble-plus.json"
DEFAULT_LENGTH = 5
MIN_LENGTH = 2
MAX_LENGTH = 15

def run():
    """process a list of words to find words of the specified lengths and optionally save to a JSON file"""
    newlist = []
    wdf = json.load( open(file_name) )
    for item in wdf:
        if lower <= len(item) <= upper:
            newlist.append(item)
    show(f"word count = {len(newlist)}\n")

    show("sample output:")
    ni = 0
    nli = len(newlist) // 30
    for word in newlist:
        if ni % nli == 0:
            show(f'"{word}",')
        ni += 1

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_name = f"{lower}-{upper}_letter_words" if lower != upper else f"{lower}-letter_words"
        save_to_json(save_name, newlist)
        show(f"Save output to file '{JSON_LABEL}{osp.sep}{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="process a list of words to find words of the specified lengths", prog=f"python3 {argv[0]}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-f', '--file', type=str, default = DEFAULT_WORD_FILE,
                            help = f"path to alternate file with list of all acceptable words; DEFAULT = {DEFAULT_WORD_FILE}.")
    arg_parser.add_argument('-l', '--lower', type=int, default = DEFAULT_LENGTH,
                            help = f"minimum number of letters in the words; DEFAULT = {DEFAULT_LENGTH}; MIN = {MIN_LENGTH}")
    arg_parser.add_argument('-u', '--upper', type=int, default = MAX_LENGTH,
                            help = f"maximum number of letters in the words; DEFAULT = {MAX_LENGTH}; MAX = {MAX_LENGTH}")
    return arg_parser

def prep_args(argl:list) -> (bool, int, int):
    args = set_args().parse_args(argl)

    lgr.logl("START LOGGING")
    show(f"save option = '{args.save}'")

    if not osp.isfile(args.file):
        raise Exception(f"File path '{args.file}' does not exist.")
    show(f"Using word file '{args.file}'")

    low = args.lower if MIN_LENGTH <= args.lower <= MAX_LENGTH else DEFAULT_LENGTH
    show(f"lower limit = {low}")

    up = args.upper if low <= args.upper <= MAX_LENGTH else MAX_LENGTH
    show(f"upper limit = {up}")

    return args.save, args.file, low, up


if __name__ == '__main__':
    lgr = MhsLogger( get_base_filename(__file__) )
    show = lgr.show

    save_option, file_name, lower, upper = prep_args(argv[1:])
    run()
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
