##############################################################################################################################
# coding=utf-8
#
# find_pangrams.py
#   -- from a SpellingBee results JSON file, find all (non-uppercase) pangrams and make UPPERCASE and save in a copy of the input file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-09-13"
__updated__ = "2024-09-20"

import os
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, FILE_DATETIME_FORMAT, JSON_LABEL, get_current_time, get_base_filename, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

start = time.perf_counter()
DEFAULT_INPUT_FILE    = "input/SpellBeeTest.json"
DEFAULT_OUTPUT_FOLDER = "./output"
ANSWER_KEY = "answers"
END_KEY    = "]"

def is_pangram(p_line:str) -> bool:
    testline = p_line.strip(', \n')
    lgr.debug(f"\ntesting {testline}")
    # check if already uppercase
    if skip and testline == testline.upper():
        return False
    result = ""
    for lett in testline:
        lgr.debug(f"testing '{lett}'")
        if not lett.isalpha():
            continue
        if lett not in result:
            result += lett
    lgr.debug(f"result = '{result}'")
    if len(result) == 7:
        lgr.info(f">> {testline} is a Pangram!")
        return True
    return False

def run():
    """Open a spellingbee results JSON file and find (non-uppercase) pangrams and convert to UPPERCASE and save results to a new file."""
    outfile_name = osp.join(output_folder, "pangrams" + '_' + get_current_time(FILE_DATETIME_FORMAT) + osp.extsep + JSON_LABEL)
    with open(input_file) as file_in:
        with open(outfile_name, 'w') as file_out:
            search_state = False
            for line in file_in:
                lgr.debug(line)
                newline = line
                if END_KEY in line:
                    search_state = False
                if search_state and is_pangram(line):
                    newline = line.upper()
                if save_option:
                    file_out.write(newline)
                if ANSWER_KEY in line:
                    search_state = True
    file_out.close()
    if save_option:
        lgr.info(f"\nSaved results to: {outfile_name}")
    else:
        os.remove(outfile_name)

def set_args():
    arg_parser = ArgumentParser(description = "from a SpellingBee results JSON file, find all (non-uppercase) pangrams "
                                              "and make UPPERCASE and save in a copy of the input file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default = False,
                            help = "Copy the input file to a new file with the newly UPPERCASE pangrams.")
    arg_parser.add_argument('-i', '--input', type=str, default = DEFAULT_INPUT_FILE,
                            help = f"path to a SpellingBee results JSON file with words to check; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    arg_parser.add_argument('-o', '--output', type=str, default = DEFAULT_OUTPUT_FOLDER,
                            help = f"output folder location to store the produced JSON file; DEFAULT = '{DEFAULT_OUTPUT_FOLDER}'.")
    arg_parser.add_argument('-k', '--skip', action="store_false", default = True,
                            help = "Skip over any found words that are already UPPERCASE; DEFAULT = True.")
    return arg_parser

def get_args(argl:list) -> (bool, str, str):
    args = set_args().parse_args(argl)

    loglev = DEFAULT_LOG_LEVEL

    lgr.log(loglev, f"save option = '{args.save}'")

    inputf = args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.log(loglev, f"input file = '{inputf}'")

    outputf = args.output if osp.isfile(args.output) else DEFAULT_OUTPUT_FOLDER
    lgr.log(loglev, f"output folder = '{outputf}'")

    lgr.log(loglev, f"skip option = '{args.skip}'")

    return args.save, inputf, outputf, args.skip


if __name__ == '__main__':
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()

    code = 0
    try:
        save_option, input_file, output_folder, skip = get_args(argv[1:])
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
