##############################################################################################################################
# coding=utf-8
#
# compare_word_lists.py
#   -- search for words in a list that are NOT in a target word list
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.11+"
__created__ = "2026-03-08"
__updated__ = "2026-07-08"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_SEARCH_FILE = "./input/new_pangrams.txt"
DEFAULT_TARGET_FILE = "./input/all_words.txt"

def run():
    """Search for words in a list that are NOT in a target word list."""
    srch_name = get_filename(search_file)
    targ_name = get_filename(target_file)
    lgr.info(f"Find words in '{srch_name}' that are NOT in '{targ_name}'.")
    search_data = []
    target_data = []
    sf = open(search_file)
    wsf = json.load(sf) if search_file.endswith(".json") else sf
    for item in wsf:
        cword = get_clean_word(item)
        search_data.append(cword)
    tf = open(target_file)
    wtf = json.load(tf) if target_file.endswith(".json") else tf
    for item in wtf:
        cword = get_clean_word(item)
        target_data.append(cword)
    save_data = []
    for word in search_data:
        if word not in target_data:
            save_data.append(word)

    if save_option:
        outfile_name = save_to_json( "compare_word_lists", save_data)
        lgr.info(f"Saved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "find words in a 'search' list that are NOT in a 'target' word list",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_true", default = False,
                            help = "Write the results to a JSON file.")
    arg_parser.add_argument('-i', '--input', type = str, metavar = "searchPATH", default = DEFAULT_SEARCH_FILE,
                            help = f"path to the file to search for words not in the target file; DEFAULT = '{DEFAULT_SEARCH_FILE}'.")
    arg_parser.add_argument('-t', '--target', type = str, metavar = "targetPATH", default = DEFAULT_TARGET_FILE,
                            help = f"path to the target file; DEFAULT = '{DEFAULT_TARGET_FILE}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)
    srchfile = args.input if osp.isfile(args.input) else DEFAULT_SEARCH_FILE
    lgr.info(f"search file = '{srchfile}'")
    targfile = args.target if osp.isfile(args.target) else DEFAULT_TARGET_FILE
    lgr.info(f"target file = '{targfile}'")
    return args.save, srchfile, targfile


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, search_file, target_file = get_args(argv[1:])
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
