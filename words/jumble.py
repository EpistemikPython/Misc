##############################################################################################################################
# coding=utf-8
#
# jumble.py
#   -- find all the letter permutations from a submitted word
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author_name__    = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-10-27"
__updated__ = "2024-11-03"

import logging
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import get_base_filename, get_filename, save_to_json
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL, get_level, get_simple_logger

DEFAULT_INPUT_WORD = "help"

def run():
    results = []
    jumbler(input_word, results)
    lgr.info(f"Number of jumbled words = '{len(results)}'")
    results.sort()
    for item in results:
        lgr.log(log_lev, item)
    if save_option:
        outfile_name = save_to_json(f"{input_word.upper()}-{get_base_filename(__file__)}", results)
        lgr.info(f"Saved results to: {outfile_name}")

def jumbler(letts:str, storage:list):
    lgr.log(log_lev, f"letters arriving: '{letts}'")
    if len(letts) == 1:
        storage.append(letts)
        lgr.log(log_lev, f"added '{letts}' to results.")
    else:
        head = letts[0]
        # recursive call
        jumbler(letts[1:], storage)
        insert(head, storage)

def insert(head:str, storage:list):
    lgr.log(log_lev, f"head = '{head}'; results = {repr(storage)}")
    temp_storage = []
    for item in storage:
        ilen = len(item)
        for posn in range(ilen):
            temp_storage.append(item[:posn] + head + item[posn:])
            lgr.log(log_lev, f"added '{item[:posn] + head + item[posn:]}' to results.")
        temp_storage.append(item+head)
        lgr.log(log_lev, f"added '{item+head}' to results.")
    temp_storage.append(head)
    lgr.log(log_lev, f"added '{head}' to results.")
    storage += temp_storage

def set_args():
    arg_parser = ArgumentParser(description = "find all the letter permutations from a submitted word",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_true", default = False,
                            help = "Save the output to a JSON file; DEFAULT = False.")
    arg_parser.add_argument('-l', '--loglevel', type = str, default = logging.getLevelName(DEFAULT_LOG_LEVEL),
                            help = f"level for optional logging; DEFAULT = '{logging.getLevelName(DEFAULT_LOG_LEVEL)}'.")
    arg_parser.add_argument('-i', '--input', type = str, default = DEFAULT_INPUT_WORD,
                            help = f"word to jumble; DEFAULT = '{DEFAULT_INPUT_WORD}'.")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)
    glv = get_level(args.loglevel)
    inputw = args.input if args.input.isalpha() else DEFAULT_INPUT_WORD
    return args.save, glv if glv else DEFAULT_LOG_LEVEL, inputw


if __name__ == '__main__':
    start = time.perf_counter()
    basename = get_base_filename(__file__)
    lgr = get_simple_logger(f"simple_{basename}", file_handling = False)
    code = 0
    try:
        save_option, log_lev, input_word = get_args(argv[1:])
        log_control = MhsLogger(basename, con_level = DEFAULT_LOG_LEVEL)
        lgr = log_control.get_logger()
        lgr.info(f"save option = '{save_option}'; log level = '{logging.getLevelName(log_lev)}'; input word = '{input_word}'")
        run()
    except KeyboardInterrupt as mki:
        lgr.exception(mki)
        code = 13
    except ValueError as mve:
        lgr.exception(mve)
        code = 27
    except Exception as mex:
        lgr.exception(mex)
        code = 66

    lgr.info(f"Elapsed time = {time.perf_counter() - start} seconds")
    exit(code)
