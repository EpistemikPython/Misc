##############################################################################################################################
# coding=utf-8
#
# get_spellbee_pangrams.py
#   -- from a spelling-bee words file, get pangrams and save to a JSON file
#
# Copyright (c) 2025 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2025-08-19"
__updated__ = "2025-11-29"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, save_to_json, get_base_filename, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_INPUT_FILE = "input/spellbee_words.json"
TEST_INPUT_FILE    = "input/spellbee_words_test.json"
MIN_SPELLBEE_LENGTH = 4
MIN_PANGRAM_LENGTH = 7

def is_pangram(test_word:str) -> bool:
    # eliminate simple plurals
    if test_word == previous_word + 'S' or test_word == previous_word + "ES":
        return False
    unique = ""
    for lett in test_word:
        if not lett.isalpha():
            return False
        if lett not in unique:
            unique += lett
    # lgr.debug(f"unique = '{unique}'")
    if len(unique) == MIN_PANGRAM_LENGTH:
        lgr.debug(f">> {test_word} is a Pangram!")
        return True
    return False

def run():
    """From a spelling-bee words file, get regular pangrams and save to a JSON file."""
    global previous_word
    base_words = []
    pangrams = []
    with open(input_file) as file_in:
        for line in file_in:
            # lgr.debug(line)
            testword = line.strip('-_", \n').upper()
            if len(testword) >= MIN_SPELLBEE_LENGTH:
                base_words.append(testword)
            if is_pangram(testword):
                pangrams.append(testword)
            previous_word = testword
    # find and remove other plurals and simple past and 'ing'
    remove_words = []
    for word in pangrams:
        if word[-3:] == "IES" or word[-3:] == "ING":
            remove_words.append(word)
            continue
        if word[-1] == 'S':
            rootword = word[:-1]
            if rootword in base_words:
                remove_words.append(word)
                continue
            if rootword[-1] == 'E':
                nextrootword = rootword[:-1]
                if nextrootword in base_words:
                    remove_words.append(word)
                    continue
        if word[-2:] == "ED":
            rootword = word[:-1]
            if rootword in base_words:
                remove_words.append(word)
                continue
            rootword = word[:-2]
            if rootword in base_words:
                remove_words.append(word)

    for item in remove_words:
        if item in pangrams:
            pangrams.remove(item)

    if save_option:
        outfile_name = save_to_json(f"pangrams{test}", pangrams)
        lgr.info(f"\nSaved all pangrams to: {outfile_name}")
        outfile_name = save_to_json(f"all_spellbee_words{test}", base_words)
        lgr.info(f"\nSaved ALL spellbee words to: {outfile_name}")
        outfile_name = save_to_json(f"remove_words{test}", remove_words)
        lgr.info(f"\nSaved all remove words to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "from a spelling-bee words file, get all pangrams and save to a JSON file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default = False,
                            help = "Save the found pangrams to a new file; DEFAULT = 'False'")
    arg_parser.add_argument('-t', '--test', action="store_true", default = False,
                            help = f"Use the test input file; DEFAULT = 'False'; TEST input file = '{TEST_INPUT_FILE}'.")
    arg_parser.add_argument('-i', '--input', type=str, default = DEFAULT_INPUT_FILE,
                            help = f"path to an ALTERNATE SpellingBee JSON input file; DEFAULT input file = '{DEFAULT_INPUT_FILE}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)

    loglev = DEFAULT_LOG_LEVEL

    lgr.log(loglev, f"save option = '{args.save}'")

    inputf = TEST_INPUT_FILE if args.test else args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.log(loglev, f"input file = '{inputf}'")

    return args.save, inputf, "_test" if args.test else ""


log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )

if __name__ == '__main__':
    start = time.perf_counter()
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_file, test = get_args(argv[1:])
        previous_word = ""
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
    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start} seconds")
    exit(code)
