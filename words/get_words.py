##############################################################################################################################
# coding=utf-8
#
# get_words.py
#   -- from a words list file, get specified words and save to a new file
#
# Copyright (c) 2025 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2025-09-12"
__updated__ = "2025-09-14"

import re
import time
from argparse import ArgumentParser
from os.path import basename
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, get_base_filename, get_filename, get_filetype, save_to_json
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

HTML_TYPE = "htm"
DEFAULT_HTML_FILE = "./input/Wiktionary-37k.htm"
TEST_HTML_FILE    = "./input/Wiktionary-test.htm"
TEXT_TYPE = "txt"
DEFAULT_TEXT_FILE = "./input/combined-wordlist-all_sort-uniq.txt"
TEST_TEXT_FILE    = "./input/wordlist-test.txt"

def run():
    if input_type == HTML_TYPE:
        run_html()
    elif input_type == TEXT_TYPE:
        run_text()
    else:
        lgr.info("do nothing...")

def run_text():
    first_data = []
    with open(input_file) as file_in:
        for it in file_in:
            item = it.strip('-_",. \n').upper()
            if 3 < len(item) < 22:
                first_data.append(item)
    second_data = first_data.copy()
    third_data = []
    # find and remove simple plurals
    for word in second_data:
        if word[-1] == 'S':
            rootword = word[:-1]
            if rootword in first_data:
                continue
            if rootword[-1] == 'E':
                nextrootword = rootword[:-1]
                if nextrootword in first_data:
                    continue
        third_data.append(word)

    if save_option:
        outfile_name = save_to_json("get_words_text", third_data)
        lgr.info(f"\nSaved results to: {outfile_name}")

def run_html():
    """From a words list file, get specified words and save to a new file."""
    out_data = []
    with open(input_file) as file_in:
        for line in file_in:
            re_word = re.compile(r"<td><a.*>(\w*)</a></td>")
            re_match = re.match(re_word, line)
            if re_match:
                match_word = re_match.group(1)
                # lgr.info(f"Matched and get word = '{match_word}'!")
                out_data.append(match_word)

    if save_option:
        outfile_name = save_to_json("get_words_html", out_data)
        lgr.info(f"\nSaved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "from a words list file, get specified words and save to a new file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-n', '--nosave', action = "store_true", default = False,
                            help = "DO NOT save the output to a new JSON file; DEFAULT = False.")
    arg_parser.add_argument('-i', '--input', type = str, metavar = "inPATH", default = DEFAULT_TEXT_FILE,
                            help = f"path to a word list file with words to get; DEFAULT = '{DEFAULT_TEXT_FILE}'.")
    return arg_parser

def get_args(argl:list) -> tuple[bool, str, str]:
    args = set_args().parse_args(argl)
    save_opt = not args.nosave
    lgr.info(f"save option = '{save_opt}'")
    itype = get_filetype(args.input).strip('.')
    infile = args.input if osp.isfile(args.input) else TEST_TEXT_FILE
    lgr.info(f"input file = '{infile}'")
    return save_opt, itype, infile


if __name__ == '__main__':
    start = time.perf_counter()
    basename = get_base_filename(__file__)
    log_control = MhsLogger(basename, con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_type, input_file = get_args(argv[1:])
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
