##############################################################################################################################
# coding=utf-8
#
# find_unique_words.py
#   -- process a list of words to find groups of words of the same length with each having unique letters
# adapted from: https://github.com/sh1boot/fivewords.git
# see: https://www.youtube.com/watch?v=c33AZBnRHks
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-10"
__updated__ = "2024-11-28"

import array
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import json, save_to_json, get_base_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

WORD_FILE = "input/scrabble-plus.json"
# five-letter testing
# WORD_FILE = "input/five-letter_test.json"
# highest to lowest letter frequencies in Scrabble '5-13 letter' words
ORDERED_LETTERS = "ESIARNOTLCDUPMGHBYFKVWZXQJ"
# highest to lowest letter frequencies in Scrabble 7-letter words
# ORDERED_LETTERS = "ESAIRNOTLDUCGPMHBYKFWVZXJQ"
MAX_NUMLETTERS = len(ORDERED_LETTERS)
MIN_NUM_LETTERS = 10
MAX_WORDSIZE = 15
MIN_WORDSIZE = 3
DEFAULT_INITIALIZER = (0, 0, 0, 0, 0)
MAX_NUMWORDS = len(DEFAULT_INITIALIZER)
MIN_NUMWORDS = 2

def compress(cmask:int):
    return (cmask ^ (cmask - 1)).bit_length() - 1

def decompress(dpack:int):
    return 1 << dpack

def store(group:array):
    global count
    group = sorted( next(iter(word_names[wmask])) for wmask in group )
    output[count] = group
    count += 1

def solve(highbit:int, p_extra:int, progress:array, depth:int=0):
    depth_limit = num_words - 1
    for dx in range(p_extra + 1):
        least = highbit.bit_length() - 1
        for pack in word_pack[least]:
            required = decompress(pack)
            if (highbit & required) == required:
                for mask in word_pack[least][pack]:
                    if (mask & highbit) == mask:
                        progress[depth] = mask
                        if depth >= depth_limit:
                            store(progress)
                        else:
                            solve(highbit & ~mask, p_extra - dx, progress, depth + 1)
        highbit ^= 1 << least

def run():
    """process a list of words to find groups of words of the same length with each having unique letters"""
    global word_pack
    extra = num_letters - (word_size * num_words)
    lgr.info(f"num extra letters = {extra}")
    word_pack = [{} for _ in range(num_letters)]

    wct = 0
    wf = json.load( open(WORD_FILE) )
    for word in wf:
        if len(word) == word_size:
            wct += 1
            mask = 0
            for lett in word:
                lx = ordered_letters.find(lett)
                if lx < 0 or lx >= num_letters:
                    break
                bx = 1 << lx
                if mask & bx:
                    break
                mask |= bx
            else:
                least = mask.bit_length() - 1
                pack = compress(mask)
                word_names.setdefault( mask, set() ).add(word)
                word_pack[least].setdefault( pack, set() ).add(mask)
    lgr.info(f"found {wct} words.")

    initializer = DEFAULT_INITIALIZER
    if num_words == 4:
        initializer = (0, 0, 0, 0)
    elif num_words == 3:
        initializer = (0, 0, 0)
    elif num_words == MIN_NUMWORDS:
        initializer = (0, 0)
    solve( (1 << num_letters) - 1, extra, array.array('L', initializer) )

    # sample some of the output
    lgr.info(f"\n\t\t\t Solutions:")
    nx = 0
    for index in output.keys():
        lgr.info(output[index])
        nx += 1
        if nx == 32:
            if count > 32:
                lgr.info("etc...")
            break
    lgr.info(f"total groups = {count}")

    lgr.info(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        json_save_name = save_to_json(f"{word_size}x{num_words}from{num_letters}_find-unique-words", output)
        lgr.info(f"Saved results to: {json_save_name}")


def set_args():
    arg_parser = ArgumentParser(description="get the save-to-file, word size, number of words and number of letters options", prog=f"python3 {argv[0]}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="write the results to a JSON file")
    arg_parser.add_argument('-w', '--wordsize', type=int, default = MIN_WORDSIZE,
                            help = f"number of letters in each found word; DEFAULT = {MIN_WORDSIZE}")
    arg_parser.add_argument('-n', '--numwords', type=int, default = MAX_NUMWORDS,
                            help = f"number of words in each found group; DEFAULT = {MAX_NUMWORDS}")
    arg_parser.add_argument('-l', '--numletters', type=int, default = MAX_NUMLETTERS,
                            help = f"number of possible letters for each word; DEFAULT = {MAX_NUMLETTERS}")
    return arg_parser

def prep_args(argl:list):
    args = set_args().parse_args(argl)
    lgr.info(f"save option = '{args.save}'")
    word_sz = args.wordsize if MIN_WORDSIZE <= args.wordsize <= MAX_WORDSIZE else MIN_WORDSIZE
    lgr.info(f"using word size = {word_sz}")
    num_wds = args.numwords if MIN_NUMWORDS <= args.numwords <= MAX_NUMWORDS else MAX_NUMWORDS
    lgr.info(f"using number of words = {num_wds}")
    num_letts = args.numletters if MIN_NUM_LETTERS <= args.numletters <= MAX_NUMLETTERS else MAX_NUMLETTERS
    lgr.info(f"using total number of letters = {num_letts}")
    return args.save, word_sz, num_wds, num_letts


if __name__ == '__main__':
    start = time.perf_counter()
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    count = 0
    word_names = {}
    word_pack = []
    output = {}
    code = 0
    try:
        save_option, word_size, num_words, num_letters = prep_args(argv[1:])
        ordered_letters = ORDERED_LETTERS[:num_letters]
        lgr.info(f"letters being used: '{ordered_letters}'")
        # make sure the parameters for size of words & number of words and letters are safe and sensible
        if word_size*num_words > num_letters:
            word_size = MIN_WORDSIZE
            num_words = num_letters//word_size
        lgr.info(f"Find groups of {num_words} 'uniquely lettered' words each with {word_size} letters.")
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
    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
