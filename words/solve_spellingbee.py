##############################################################################################################################
# coding=utf-8
#
# solve_spellingbee.py
#   -- from a word list file, find all words that fulfill the specified SpellingBee requirements
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2024-10-31"

import logging
import time
import json
from argparse import ArgumentParser
import os.path as osp
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, get_current_date, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_WORD_FILE = "input/spellbee_words.json"
NUM_OUTERS = 6
MIN_WORD_SIZE = 4
MAX_PRINT = 30
MAX_RANGE = 12 # possible word sizes from 4 to 15

def run(p_loglev:int):
    """from a word list file, find all words that fulfill the specified SpellingBee requirements"""
    solutions = [ [] for _ in range(MAX_RANGE) ]
    num_solns = 0
    wdf = json.load( open(file_name) )
    for item in wdf:
        leng = len(item)
        if leng >= MAX_RANGE + MIN_WORD_SIZE:
            lgr.warning(f"Word size = {leng} >> GREATER than acceptable MAX!")
        elif leng >= MIN_WORD_SIZE:
            for letter in item:
                if letter not in outers + required:
                    break
            else:
                if required in item:
                    solutions[leng - MIN_WORD_SIZE].append(item)
                    num_solns += 1

    lgr.log(p_loglev, f"solution count = {num_solns}")
    # check for pangrams and print the solutions
    skip = 1 if num_solns <= MAX_PRINT else num_solns // MAX_PRINT + 1
    lgr.log(p_loglev, f"skip = {skip}")
    ct = 0
    pgct = 0
    lgr.log(p_loglev, f"{'Sample of' if skip > 1 else 'ALL'} solutions:")
    for idx in range(MAX_RANGE):
        for val in solutions[idx]:
            pg = True
            for lett in outers:
                if lett not in val:
                    pg = False
                    break
            if pg:
                lgr.info(f"\t{val} : Pangram!")
                pgct += 1
            else:
                ct += 1
                if ct % skip == 0:
                    lgr.log(p_loglev, f"\t{val}")
    lgr.log(p_loglev, f">> {pgct if pgct > 0 else 'NO'} Pangram{'' if pgct == 1 else 's'}{'!' * pgct}")

    lgr.info(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_dict = {f"{dict_name}":solutions}
        save_name = save_to_json(f"{required}-{outers}_spellbee-words", save_dict)
        lgr.info(f"Save output to file '{save_name}'.")

def set_args():
    arg_parser = ArgumentParser(description="from a word list file, find all words that fulfill the specified SpellingBee requirements",
                                prog=f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="Write the results to a JSON file")
    arg_parser.add_argument('-n', '--name', type=str, default = get_current_date(),
                            help = "if saving, optional name of key for dictionary of results")
    arg_parser.add_argument('-f', '--file', type=str, default = DEFAULT_WORD_FILE,
                            help = f"path to file with list of all acceptable words; DEFAULT = '{DEFAULT_WORD_FILE}'")
    arg_parser.add_argument('-c', '-r', '--central', type=str, required=True, help="this ONE letter MUST be in each word")
    arg_parser.add_argument('-o', '-p', '--outer', type=str, required=True, help="SIX other POSSIBLE letters in the words")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)

    loglev = logging.INFO

    lgr.log(loglev, f"save option = '{args.save}'")
    if args.save:
        lgr.log(loglev, f"saved results dictionary name = {args.name}")

    if not osp.isfile(args.file):
        raise Exception(f"File path '{args.file}' does not exist.")
    lgr.log(loglev, f"using word file '{args.file}'")

    central = args.central.upper()
    if central.isalpha() and len(central) == 1:
        lgr.log(loglev, f"central letter = {central}")
    else:
        raise Exception(f"INVALID central letter: {central}.")

    outer = args.outer.upper()
    if outer.isalpha():
        if len(outer) == NUM_OUTERS:
            if central in outer:
                raise Exception(f"INVALID outer letters '{outer}'. REQUIRED letter '{central}' CANNOT be in outers.")
            else:
                # make sure all the outer letters are different
                test = args.outer
                while test:
                    lett = test[0]
                    test = test.removeprefix(lett)
                    if lett in test:
                        raise Exception(f"Duplicate letter '{lett}' in outer letters.")
                lgr.log(loglev, f"outer letters = {outer}")
        else:
            raise Exception(f"Invalid NUMBER of outer letters: {len(outer)}.")
    else:
        raise Exception(f"NON-LETTER in outer letters: {outer}.")

    return args.save, args.name, args.file, central, outer


if __name__ == '__main__':
    start = time.perf_counter()
    log_control = MhsLogger(get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL)
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, dict_name, file_name, required, outers = get_args(argv[1:])
        run(DEFAULT_LOG_LEVEL)
    except KeyboardInterrupt:
        lgr.exception(">> User interruption.")
        code = 13
    except ValueError:
        lgr.exception(">> Value Error.")
        code = 27
    except Exception as mex:
        lgr.exception(f"Problem: {repr(mex)}.")
        code = 66

    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
