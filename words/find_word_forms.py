##############################################################################################################################
# coding=utf-8
#
# find_word_forms.py
#   -- from a words list file, find missing word forms and save to a new file
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2026-03-06"
__updated__ = "2026-03-29"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_FILE = "./input/all_words.txt"
ING_FORM = "ING"
ING_FORM_LEN = len(ING_FORM)
ED_FORM = "ED"
ED_FORM_LEN = len(ED_FORM)
ER_FORM = "ER"
ER_FORM_LEN = len(ER_FORM)
MIN_WORD_LENGTH = 5
MIN_FORM_LENGTH = 3

def run():
    """From a words list file, find missing word forms and save to a new file."""
    first_data = []
    with open(input_file) as file_in:
        for it in file_in:
            item = it.strip('-_",. \n').upper()
            if len(item) >= MIN_WORD_LENGTH:
                first_data.append(item)
    second_data = first_data.copy()
    save_data = []
    for word in second_data:
        if word[-ING_FORM_LEN:] == ING_FORM:
            rootword = word[:-ING_FORM_LEN]
            newform = rootword + ED_FORM
            if newform not in first_data and len(newform) >= MIN_FORM_LENGTH:
                save_data.append(newform)
                lgr.info(f"new word form = {newform}")
        elif word[-ED_FORM_LEN:] == ED_FORM:
            rootword = word[:-ED_FORM_LEN]
            if rootword[-1] != 'E':
                newform = rootword + ING_FORM
                if newform not in first_data and len(newform) >= MIN_FORM_LENGTH:
                    save_data.append(newform)
                    lgr.info(f"new word form = {newform}")

    outfile_name = save_to_json("find_word_forms", save_data)
    lgr.info(f"\nSaved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "from a words list file, find missing word forms and save to a new file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-f', '--file', type = str, metavar = "filePATH", default = DEFAULT_FILE,
                            help = f"path to a word list file with words to get; DEFAULT = '{DEFAULT_FILE}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)
    infile = args.file if osp.isfile(args.file) else DEFAULT_FILE
    lgr.info(f"input file = '{infile}'")
    return infile


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        input_file = get_args(argv[1:])
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
