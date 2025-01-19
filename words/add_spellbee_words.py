##############################################################################################################################
# coding=utf-8
#
# add_spellbee_words.py
#   -- from a SpellingBee results JSON file, get new words and append to an existing JSON file
#
# Copyright (c) 2025 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2025-01-13"
__updated__ = "2025-01-13"

import json
import time
from argparse import ArgumentParser
from os.path import basename
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, get_base_filename, get_filename, save_to_json
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_INPUT_FILE  = "/home/marksa/Documents/Words/SpellingBee/SpellBeeWords_2025.json"
DEFAULT_OUTPUT_FILE = "/home/marksa/Documents/Words/SpellingBee/SpellBee_AllWords.json"
TEST_OUTPUT_FILE    = "./tests/sb_allwords.json"
ANSWER_KEY = "answers"
END_KEY    = "]"

def run():
    """Open a SpellingBee results JSON file and get new words and append to an existing JSON file."""
    with open(output_file, 'r+') as file_out:
        out_data = json.load(file_out)
        with open(input_file) as file_in:
            search_state = False
            for line in file_in:
                if ANSWER_KEY in line:
                    search_state = True
                elif END_KEY in line:
                    search_state = False
                elif search_state:
                    ansline = line.strip('," \n').lower()
                    if ansline not in out_data:
                        lgr.debug(f"add word '{ansline}' to {output_file}.")
                        out_data.append(ansline)
                    # else:
                    #     lgr.info(f"answer line '{ansline}' ALREADY in output!")
        # return to start of file to overwrite the existing data
        file_out.seek(0)
        json.dump(out_data, file_out, indent=4)

    if save_option:
        outfile_name = save_to_json(basename, out_data)
        lgr.info(f"\nSaved results to: {outfile_name}")

def set_args():
    arg_parser = ArgumentParser(description = "from a SpellingBee results JSON file, get new words and append to an existing JSON file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action = "store_true", default = False,
                            help = "ALSO save the output to a new JSON file; DEFAULT = False.")
    arg_parser.add_argument('-t', '--test', action = "store_true", default = False,
                            help = f"USE the TEST output file ['{TEST_OUTPUT_FILE}']; DEFAULT = False.")
    arg_parser.add_argument('-i', '--input', type = str, metavar = "inPATH", default = DEFAULT_INPUT_FILE,
                            help = f"path to a SpellingBee results JSON file with words to get; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    arg_parser.add_argument('-o', '--output', type = str, metavar = "outPATH", default = DEFAULT_OUTPUT_FILE,
                            help = f"path to a SpellingBee results JSON file to update with new words; DEFAULT = '{DEFAULT_OUTPUT_FILE}'.")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)
    lgr.info(f"save option = '{args.save}'")
    infile = args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.info(f"JSON input file = '{infile}'")
    outfile = TEST_OUTPUT_FILE if args.test else args.output if osp.isfile(args.output) else DEFAULT_OUTPUT_FILE
    lgr.info(f"JSON output file = '{outfile}'")
    return args.save, infile, outfile


if __name__ == '__main__':
    start = time.perf_counter()
    basename = get_base_filename(__file__)
    log_control = MhsLogger(basename, con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_file, output_file = get_args(argv[1:])
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
