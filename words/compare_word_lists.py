##############################################################################################################################
# coding=utf-8
#
# compare_word_lists.py
#   -- compare word lists and optionally add one to, or subtract one from the other and save results to a new file
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2026-03-08"
__updated__ = "2026-03-31"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_INPUT_FILE  = "./input/new_pangrams.txt"
DEFAULT_TARGET_FILE = "./input/all_words.txt"

def run():
    """Compare word lists and optionally add one to, or subtract one from the other and save results to a new file."""
    input_data = []
    target_data = []
    with open(input_file) as file_in:
        for it in file_in:
            item = it.strip('-_",. \n').upper()
            input_data.append(item)
    with open(target_file) as file_targ:
        for it in file_targ:
            item = it.strip('-_",. \n').upper()
            target_data.append(item)
    if subtract_option:
        # go through target words: add target word to the save file IF it is not in input words
        save_data = []
        for word in target_data:
            if word not in input_data:
                save_data.append(word)
    else:
        # Add: go through input words: add any missing input words to the save file
        save_data = target_data.copy()
        for word in input_data:
            if word not in save_data:
                save_data.append(word)

    outfile_name = save_to_json( "compare_words_" + ("subtract" if subtract_option else "add"), save_data)
    lgr.info(f"\nSaved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "compare word lists and add or subtract one to the other and save results to a new file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--subtract', action = "store_true", default = False,
                            help = "SUBTRACT the input words from the target list; Default = ADD.")
    arg_parser.add_argument('-i', '--input', type = str, metavar = "inPATH", default = DEFAULT_INPUT_FILE,
                            help = f"path to the file with words to add or subtract re the target list; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    arg_parser.add_argument('-t', '--target', type = str, metavar = "targetPATH", default = DEFAULT_TARGET_FILE,
                            help = f"path to the target file; DEFAULT = '{DEFAULT_TARGET_FILE}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)
    subtract_opt = args.subtract
    lgr.info(f"subtract option = '{subtract_opt}'")
    infile = args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.info(f"input file = '{infile}'")
    targfile = args.target if osp.isfile(args.target) else DEFAULT_TARGET_FILE
    lgr.info(f"target file = '{targfile}'")
    return subtract_opt, infile, targfile


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        subtract_option, input_file, target_file = get_args(argv[1:])
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
    lgr.info(f"\nElapsed time = {time.perf_counter() - start} seconds")
    exit(code)
