##############################################################################################################################
# coding=utf-8
#
# get_spellbee_pangrams.py
#   -- from a spelling-bee words file, get all pangrams and save to a new JSON file
#
# Copyright (c) 2025 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2025-08-19"
__updated__ = "2025-08-19"

import os
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import osp, FILE_DATETIME_FORMAT, JSON_LABEL, get_current_time, get_base_filename, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

DEFAULT_INPUT_FILE    = "input/spellbee_words_test.json"
DEFAULT_OUTPUT_FOLDER = "./output"

def is_pangram(p_line:str) -> bool:
    testline = p_line.strip('", \n')
    # lgr.debug(f"testing {testline}")
    result = ""
    for lett in testline:
        # lgr.debug(f"testing '{lett}'")
        if not lett.isalpha():
            continue
        if lett not in result:
            result += lett
    lgr.debug(f"result = '{result}'")
    if len(result) == 7:
        lgr.debug(f">> {testline} is a Pangram!")
        return True
    return False

def run():
    """from a spelling-bee words file, get all pangrams and save to a new JSON file."""
    outfile_name = osp.join(output_folder, "pangrams" + '_' + get_current_time(FILE_DATETIME_FORMAT) + osp.extsep + JSON_LABEL)
    with open(input_file) as file_in:
        with open(outfile_name, 'w') as file_out:
            for line in file_in:
                # lgr.debug(line)
                newline = line
                if is_pangram(line) and save_option:
                    file_out.write(newline)
    file_out.close()
    if save_option:
        lgr.info(f"\nSaved results to: {outfile_name}")
    else:
        os.remove(outfile_name)

def set_args():
    arg_parser = ArgumentParser(description = "from a spelling-bee words file, get all pangrams and save to a new JSON file",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default = False,
                            help = "Copy the found pangrams to a new file; DEFAULT = 'False'")
    arg_parser.add_argument('-i', '--input', type=str, default = DEFAULT_INPUT_FILE,
                            help = f"path to a SpellingBee JSON file with words to check; DEFAULT = '{DEFAULT_INPUT_FILE}'.")
    arg_parser.add_argument('-o', '--output', type=str, default = DEFAULT_OUTPUT_FOLDER,
                            help = f"output folder to store the produced JSON file; DEFAULT = '{DEFAULT_OUTPUT_FOLDER}'.")
    return arg_parser

def get_args(argl:list):
    args = set_args().parse_args(argl)

    loglev = DEFAULT_LOG_LEVEL

    lgr.log(loglev, f"save option = '{args.save}'")

    inputf = args.input if osp.isfile(args.input) else DEFAULT_INPUT_FILE
    lgr.log(loglev, f"input file = '{inputf}'")

    outputf = args.output if osp.isfile(args.output) else DEFAULT_OUTPUT_FOLDER
    if args.save:
        lgr.log(loglev, f"output folder = '{outputf}'")

    return args.save, inputf, outputf


if __name__ == '__main__':
    start = time.perf_counter()
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    code = 0
    try:
        save_option, input_file, output_folder = get_args(argv[1:])
        run()
    except KeyboardInterrupt:
        lgr.exception(">> User Interrupt.")
        code = 13
    except ValueError:
        lgr.exception(">> Value Error.")
        code = 27
    except Exception as mex:
        lgr.exception(f">> PROBLEM: {repr(mex)}")
        code = 66

    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start} seconds")
    exit(code)
