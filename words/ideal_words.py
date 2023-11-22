##############################################################################################################################
# coding=utf-8
#
# ideal_words.py -- from a word list find all the words of the specified length that contain only the specified letters
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-11-22"
__updated__ = "2023-11-22"

import time
import json
from sys import path, argv
from argparse import ArgumentParser
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename, get_filename
from mhsLogging import MhsLogger

log_control = MhsLogger(get_base_filename(__file__))
lgr = log_control.get_logger()
lgr.warning("START LOGGING")
show = log_control.show

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
DEFAULT_EXTRA_LETTERS = "NDWPGHVJKXQZ"
DEFAULT_REQUIRED_LETTERS = "AEO"
DEFAULT_WORD_SIZE = 7

def run_ideal(save_option, required, group):
    """from a word list find all the words that contain only the specified letters"""

    solutions = []
    sct = 0
    wdf = json.load( open(WORD_FILE) )
    for item in wdf:
        if len(item) == DEFAULT_WORD_SIZE:
            # good = True
            for letter in item:
                if letter not in group + required:
                    break
            else:
                for lt in required:
                    if lt not in item:
                        # good = False
                        break
                else:
                    solutions.append(item)
                    sct += 1

    show(f"solution count = {sct}")
    # check for pangrams and print the solutions
    pgct = 0
    show(f"solutions:")
    for val in solutions:
        pg = True
        for lett in group:
            if lett not in val:
                pg = False
                break
        if pg:
            show(f"\t{val} : Pangram!")
            pgct += 1
        else:
            show(f"\t{val}")
    show(f">> {pgct} Pangram{'' if pgct == 1 else 's'}{'!' * pgct}")

    show(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y':
        save_to_json(f"{required}-{group}_spellbee_words", solutions)


def process_args():
    arg_parser = ArgumentParser(description="Process Monarch or JSON input data to obtain Gnucash transactions",
                                prog="parseMonarchCopyRep.py")
    # required arguments
    required = arg_parser.add_argument_group("REQUIRED")
    required.add_argument('-i', '--inputfile', required=True, help="path & name of the Monarch or JSON input file")
    # required if PROD
    subparsers = arg_parser.add_subparsers(help="with gnc option: MUST specify -g FILENAME and -t TX_TYPE")
    gnc_parser = subparsers.add_parser("gnc", help="Insert the parsed trade and/or price transactions to a Gnucash file")
    gnc_parser.add_argument('-g', '--gncfile', required=True, help="path & name of the Gnucash file")
    gnc_parser.add_argument('-t', '--type', required=True, choices=[TRADE, PRICE, BOTH],
                            help="type of transaction to record: {} or {} or {}".format(TRADE, PRICE, BOTH))
    # optional arguments
    arg_parser.add_argument('-l', '--level', type=int, default=lg.INFO, help="set LEVEL of logging output")
    arg_parser.add_argument('--json',  action="store_true", help="Write the parsed Monarch data to a JSON file")

    return arg_parser


def process_input_parameters(argx:list):
    args = process_args().parse_args(argx)
    info = [F"args = {args}"]

    if not osp.isfile(args.inputfile):
        raise Exception(F"File path '{args.inputfile}' does not exist! Exiting...")
    info.append(F"Input file = {args.inputfile}")

    mode = TEST
    domain = BOTH
    gnc_file = None
    if "gncfile" in args:
        if not osp.isfile(args.gncfile):
            raise Exception(F"File path '{args.gncfile}' does not exist. Exiting...")
        gnc_file = args.gncfile
        info.append(F"writing to Gnucash file = {gnc_file}")
        mode = SEND
        domain = args.type
        info.append(F"Inserting '{domain}' transaction types to Gnucash.")
    else:
        info.append("mode = TEST")

    return args.inputfile, args.json, args.level, mode, gnc_file, domain, info


def main_ideal(args:list):
    in_file, save_monarch, level, mode, gnc_file, domain, parse_info = process_input_parameters(args)

    if len(argv) <= 1:
        show(f"Usage: Python3.n[6+] {get_filename(argv[0])} save-option[Yes|No] required-letters[e.g. AMO] other-letters[e.g. NXUPHSRD]")
        exit(66)

    show(f"word file = '{WORD_FILE}'")
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    show(f"save option = '{save_option}'")

    required = DEFAULT_REQUIRED_LETTERS
    if len(argv) > 2:
        request = argv[2]
        if len(request) == 1 and request.isalpha():
            show(f"requested mandatory letters = {request}")
            required = request.upper()
    show(f"required letters = {required}")
    # make sure the required letter is not among the outer letters?
    group = DEFAULT_EXTRA_LETTERS
    if len(argv) > 3:
        request = argv[3]
        if request.isalpha():
            # make sure all the letters are different?
            show(f"requested other letters = {request}")
            group = request.upper()
    show(f"outer letters = {group}")

    run_ideal(save_option, required, group)


if __name__ == '__main__':
    main_ideal(argv[1:])
    show(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
