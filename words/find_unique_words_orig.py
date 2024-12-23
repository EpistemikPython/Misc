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
__python_version__ = "3.12+"
__created__ = "2023-10-10"
__updated__ = "2024-12-11"

import array
import time
import psutil
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json, get_base_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

# WORD_FILE = "input/words_alpha.txt"
# 5-letter testing
WORD_FILE = "input/five-letter-test.txt"

# highest to lowest letter frequencies in Scrabble '5-13 letter' words
ORDERED_LETTERS = "ESIARNOTLCDUPMGHBYFKVWZXQJ"
MAX_NUMLETTERS = len(ORDERED_LETTERS)
MIN_NUM_LETTERS = 10
MAX_WORDSIZE = 15
MIN_WORDSIZE = 3
MAX_NUMWORDS = 8
MIN_NUMWORDS = 2
DEFAULT_WORDSIZE = 5
DEFAULT_NUMWORDS = 5
MAX_SAVE_COUNT = 4000000

def memory_check():
    global interim
    lgr.info(f"INTERIM TIME = {time.perf_counter() - start}")
    lgr.info("solve count = {:,}".format(solve_count))
    lgr.info("group count = {:,}".format(count))
    vmp = psutil.virtual_memory().percent
    smp = psutil.swap_memory().percent
    lgr.info(f"% virtual memory = {vmp};  % swap memory = {smp}")
    if vmp > 95.0 and smp > 80.0:
        raise Exception(f">> EXCEEDED memory parameters: v = {vmp} | s = {smp} !!")
    interim = time.perf_counter()

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
    global solve_count
    solve_count += 1
    if time.perf_counter() - interim > 10.0:
        memory_check()
    for dx in range(p_extra + 1):
        least = highbit.bit_length() - 1
        for pack in word_pack[least]:
            required = decompress(pack)
            if (highbit & required) == required:
                for mask in word_pack[least][pack]:
                    if (mask & highbit) == mask:
                        progress[depth] = mask
                        if depth >= num_words-1:
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
    with open(WORD_FILE) as wordlist:
        for word in wordlist.read().split():
            if len(word) == word_size:
                mask = 0
                for lett in word:
                    lx = ordered_letters.find(lett.upper())
                    if lx < 0:
                        break
                    bx = 1 << lx
                    if mask & bx:
                        break
                    mask |= bx
                else:
                    wct += 1
                    least = mask.bit_length() - 1
                    pack = compress(mask)
                    word_names.setdefault( mask, set() ).add(word)
                    word_pack[least].setdefault( pack, set() ).add(mask)
    lgr.info("found {:,}".format(wct) + f" 'uniquely-lettered' {word_size}-letter words.")

    initializer = ()
    for _ in range(num_words):
        initializer += (0,)
    solve( (1 << num_letters)-1, extra, array.array('L', initializer) )

    # sample some of the output
    lgr.info("solve count = {:,}".format(solve_count))
    display_count = 32
    lgr.info(f"\n\t\t\t {"" if count <= display_count else "Sample of"} Solutions:")
    cx = 0
    tx = count // display_count
    for index in output.keys():
        if count <= display_count:
            lgr.info(output[index])
        else:
            cx += 1
            if cx % tx == 0:
                lgr.info(f"{cx}: {output[index]}")
    lgr.info("total # of groups = {:,}".format(count))

    if save_option and count <= MAX_SAVE_COUNT:
        lgr.info(f"\nsolve and display elapsed time = {time.perf_counter()-start}")
        save_content = {"input file": f"{WORD_FILE}"} | output
        json_save_name = save_to_json(f"{word_size}x{num_words}f{num_letters}_fast-unique-words", save_content)
        lgr.info(f"Saved results to: {json_save_name}")

def set_args():
    arg_parser = ArgumentParser(description="get the save-to-file, word size, number of words and number of letters options", prog=f"python3 {argv[0]}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default=False, help="write the results to a JSON file")
    arg_parser.add_argument('-w', '--wordsize', type=int, default = DEFAULT_WORDSIZE,
                            help = f"number of letters in each found word; DEFAULT = {DEFAULT_WORDSIZE}")
    arg_parser.add_argument('-n', '--numwords', type=int, default = DEFAULT_NUMWORDS,
                            help = f"number of words in each found group; DEFAULT = {DEFAULT_NUMWORDS}")
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
    interim = start
    count = 0
    solve_count = 0
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
