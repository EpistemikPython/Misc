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
__updated__ = "2026-04-03"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import *
from mhsLogging import *

DEFAULT_INPUT_FILE = "./input/all_words.txt"
DEFAULT_CHECK_FILE = "./input/scrabble-plus.json"
ING_FORM = "ING"
ING_FORM_LEN = len(ING_FORM)
ED_FORM = "ED"
ED_FORM_LEN = len(ED_FORM)
ER_FORM = "ER"
ER_FORM_LEN = len(ER_FORM)
MIN_WORD_LENGTH = 5
MIN_FORM_LENGTH = 3
DEBUG_PRINTING = True

def run():
    """From a words list file, find missing word forms and save to a new file."""
    with open(check_file) as file_ck:
        for it in file_ck:
            item = it.strip('-_",. \n').upper()
            if len(item) >= MIN_WORD_LENGTH:
                check_data.append(item)
    with open(input_file) as file_in:
        for it in file_in:
            item = it.strip('-_",. \n').upper()
            if len(item) >= MIN_WORD_LENGTH:
                first_data.append(item)
    second_data = first_data.copy()
    for word in second_data:
        check_ing(word)
        check_ed(word)
        check_er(word)
        check_add(word)
    outfile_name = save_to_json("find_word_forms", save_data)
    lgr.info(f"\nSaved results to: {outfile_name}")

def check_ing(word:str):
    """If word is ING form, check for and add if missing ED form."""
    if word[-ING_FORM_LEN:] == ING_FORM:
        rootword = word[:-ING_FORM_LEN]
        newform = rootword + ED_FORM
        if check_form(newform):
            save_data.append(newform)

def check_ed(word:str):
    """If word is ED form, check for and add if missing ING form."""
    if word[-ED_FORM_LEN:] == ED_FORM:
        rootword = word[:-ED_FORM_LEN]
        if rootword[-1] != 'E' and rootword[-1] != 'I':
            newform = rootword + ING_FORM
            if check_form(newform):
                save_data.append(newform)

def check_er(word:str):
    """If word is ER form, check for and add if missing ING and/or ED form."""
    if word[-ER_FORM_LEN:] == ER_FORM:
        rootword = word[:-ER_FORM_LEN]
        if rootword[-1] != 'E':
            newform = rootword + ING_FORM
            if check_form(newform):
                save_data.append(newform)
            newform = rootword + ED_FORM
            if check_form(newform):
                save_data.append(newform)

def check_add(word:str):
    """If word is missing any forms, check for and add if found."""
    if word[-ING_FORM_LEN:] != ING_FORM:
        newform = word + ING_FORM
        if check_form(newform):
            save_data.append(newform)
    if word[-ED_FORM_LEN:] != ED_FORM:
        newform = word + ED_FORM
        if check_form(newform):
            save_data.append(newform)
    if word[-ER_FORM_LEN:] != ER_FORM:
        newform = word + ER_FORM
        if check_form(newform):
            save_data.append(newform)

def check_form(newform:str):
    """See if new form is in check data and not already found."""
    if (len(newform) >= MIN_FORM_LENGTH and newform not in save_data
            and newform not in first_data and newform in check_data):
        if DEBUG_PRINTING:
            lgr.info(f"new word form = {newform}")
        return True
    return False

def set_args():
    arg_parser = ArgumentParser(description = "from a words list file, find missing word forms and save to a new file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-i', '--input', type = str, metavar = "inputfilePATH", default = DEFAULT_INPUT_FILE,
                            help = f"path to a word list file with words to get; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    arg_parser.add_argument('-c', '--check', type = str, metavar = "checkfilePATH", default = DEFAULT_CHECK_FILE,
                            help = f"path to a word list file with words to get; DEFAULT = '{DEFAULT_CHECK_FILE}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)
    infile = args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.info(f"input file = '{infile}'")
    checkfile = args.check if osp.isfile(args.check) else DEFAULT_CHECK_FILE
    lgr.info(f"check file = '{checkfile}'")
    return infile, checkfile


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        input_file, check_file = get_args(argv[1:])
        check_data = []
        first_data = []
        save_data = []
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
