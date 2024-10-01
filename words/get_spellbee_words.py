##############################################################################################################################
# coding=utf-8
#
# get_spellbee_words.py
#   -- from a SpellingBee results JSON file, get all answers and save to a new JSON file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-09-30"
__updated__ = "2024-10-01"

import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, get_base_filename, get_filename, save_to_json
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_INPUT_FILE    = "/home/marksa/Documents/Words/SpellingBee/SpellBeeWords.json"
DEFAULT_OUTPUT_FOLDER = "./output"
ANSWER_KEY = "answers"
END_KEY    = "]"

def run():
    """Open a SpellingBee results JSON file and get answers and save results to a new JSON file."""
    results = []
    with open(input_file) as file_in:
        search_state = False
        for line in file_in:
            if ANSWER_KEY in line:
                search_state = True
            elif END_KEY in line:
                search_state = False
            elif search_state:
                ansline = line.strip('," \n')
                if ansline not in results:
                    lgr.debug(f"add word '{ansline}' to results.")
                    results.append(ansline)
    if save_option:
        outfile_name = save_to_json(get_base_filename(__file__), results)
        lgr.info(f"\nSaved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "from a SpellingBee results JSON file, get all answers and save to a new JSON file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_false", default = True,
                            help = "Save the output to a new JSON file; DEFAULT = True.")
    arg_parser.add_argument('-i', '--input', type = str, default = DEFAULT_INPUT_FILE,
                            help = f"path to a SpellingBee results JSON file with words to get; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    loglev = DEFAULT_LOG_LEVEL

    lgr.log(loglev, f"save option = '{args.save}'")

    inputf = args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.log(loglev, f"input file = '{inputf}'")

    return args.save, inputf


if __name__ == '__main__':
    start = time.perf_counter()
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_file = get_args(argv[1:])
        run()
    except KeyboardInterrupt:
        lgr.exception(">> User interruption.")
        code = 13
    except ValueError:
        lgr.exception(">> Value Error.")
        code = 27
    except Exception as mex:
        lgr.exception(f">> PROBLEM: {repr(mex)}")
        code = 66

    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start} seconds")
    exit(code)
