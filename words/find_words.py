##############################################################################################################################
# coding=utf-8
#
# find_words.py -- process a list of words to find groups of words of the same length with each having unique letters
# adapted from: https://github.com/sh1boot/fivewords.git
# see: https://www.youtube.com/watch?v=c33AZBnRHks
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-10"
__updated__ = "2023-12-16"

import array
import json
import time
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
# highest to lowest letter frequencies in Scrabble '5-13 letter' words
ORDERED_LETTERS = "ESIARNOTLCDUPMGHBYFKVWZXQJ"
MAX_NUMLETTERS = len(ORDERED_LETTERS)
MIN_NUM_LETTERS = 12
MAX_WORDSIZE = 15
MIN_WORDSIZE = 5
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

def run_find():
    """process a list of words to find groups of words of the same length with each having unique letters"""
    global word_pack
    extra = num_letters - (word_size * num_words)
    show(f"num extra letters = {extra}\n")
    word_pack = [{} for _ in range(num_letters)]

    wct = 0
    least = 0
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

    show(f"found {wct} words.")
    # DEBUG
    lgr.debug(f"len word_names = {len(word_names)}")
    lgr.debug(f"last 'least' = {least}")
    lgr.debug(f"len word_pack[least] = {len(word_pack[least])}")
    lgr.debug(f"word_pack[least] = {word_pack[least]}")

    initializer = DEFAULT_INITIALIZER
    if num_words == 4:
        initializer = (0, 0, 0, 0)
    elif num_words == 3:
        initializer = (0, 0, 0)
    elif num_words == MIN_NUMWORDS:
        initializer = (0, 0)
    solve( (1 << num_letters) - 1, extra, array.array('L', initializer) )

    # sample some of the output
    show(f"\nsolutions:")
    nx = 0
    for index in output.keys():
        show(output[index])
        nx += 1
        if nx == 32:
            if count > 32:
                show("etc...")
            break
    show(f"total groups = {count}")

    show(f"\nsolve and display elapsed time = {time.perf_counter() - start}")
    if save_option:
        save_to_json(f"{word_size}x{num_words}f{num_letters}_find-words", output)


def process_args():
    arg_parser = ArgumentParser(description="get the save-to-file, word size, number of words and number of letters options", prog="python3.10 find_words.py")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="write the results to a JSON file")
    arg_parser.add_argument('-w', '--wordsize', type=int, default=MIN_WORDSIZE, help="number of letters in each found word")
    arg_parser.add_argument('-n', '--numwords', type=int, default=MAX_NUMWORDS, help="number of words in each found group")
    arg_parser.add_argument('-l', '--numletters', type=int, default=MAX_NUMLETTERS, help="number of possible letters for each word")
    return arg_parser

def prep_find(argl:list) -> (bool, int, int, int):
    args = process_args().parse_args(argl)

    lgr.info("START LOGGING")
    show(f"save option = '{args.save}'")

    show(f"requested word size = {args.wordsize}")
    word_sz = args.wordsize if MIN_WORDSIZE <= args.wordsize <= MAX_WORDSIZE else MIN_WORDSIZE
    show(f"requested number of words = {args.numwords}")
    num_wds = args.numwords if MIN_NUMWORDS <= args.numwords <= MAX_NUMWORDS else MAX_NUMWORDS
    show(f"requested total number of letters = {args.numletters}")
    num_letts = args.numletters if MIN_NUM_LETTERS <= args.numletters <= MAX_NUMLETTERS else MAX_NUMLETTERS

    return args.save, word_sz, num_wds, num_letts


if __name__ == '__main__':
    log_control = MhsLogger(get_base_filename(__file__))
    lgr = log_control.get_logger()
    show = log_control.show

    count = 0
    word_names = {}
    word_pack = []
    output = {}

    save_option, word_size, num_words, num_letters = prep_find(argv[1:])

    ordered_letters = ORDERED_LETTERS[:num_letters]
    show(f"letters to use are: '{ordered_letters}'")
    # make sure the parameters for size of words & number of words and letters are safe and sensible
    if word_size * num_words > num_letters:
        word_size = MIN_WORDSIZE
        num_words = num_letters // word_size
    show(f"Find groups of {num_words} 'uniquely lettered' words each with {word_size} letters.")

    run_find()
    show(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit()
