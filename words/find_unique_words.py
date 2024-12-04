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
__updated__ = "2024-12-04"

import array
import time
import psutil
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import json, save_to_json, get_base_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

# five-letter testing
# WORD_FILE = "input/five-letter_test.json"
WORD_FILE = "input/scrabble-plus.json"
# highest to lowest letter frequencies in Scrabble '[5-13]-letter' words
ORDERED_LETTERS = "ESIARNOTLCDUPMGHBYFKVWZXQJ"
# highest to lowest letter frequencies in Scrabble 7-letter words
# ORDERED_LETTERS = "ESAIRNOTLDUCGPMHBYKFWVZXJQ"
MAX_NUMLETTERS = len(ORDERED_LETTERS)
DEFAULT_WORDSIZE = 5
MAX_WORDSIZE = 13
MIN_WORDSIZE = 3
DEFAULT_NUMWORDS = 5
MAX_NUMWORDS = 8
MIN_NUMWORDS = 2
MAX_SAVE_COUNT = 40000

def memory_check():
    global interim
    lgr.info(f"INTERIM TIME = {time.perf_counter() - start}")
    lgr.info("solve count = {:,}".format(solve_count))
    lgr.info("group count = {:,}".format(group_count))
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
    global group_count
    # lgr.debug(f"found group '{group}'")
    group = sorted( next(iter(word_names[wmask])) for wmask in group )
    results[group_count] = group
    group_count += 1

def easy_solve(p_highbit:int, p_extra:int, p_progress:array, p_depth:int=0):
    """RECURSIVE solving algorithm
       >> WARNING: small changes in parameters can lead to massive increases in run time and memory usage!"""
    global solve_count
    solve_count += 1
    if time.perf_counter() - interim > 10.0:
        memory_check()

    depth_limit = num_words - 1
    for dx in range(p_extra + 1):
        least = p_highbit.bit_length()-1
        for pack in word_pack[least]:
            required = decompress(pack)
            if (p_highbit & required) == required:
                for mask in word_pack[least][pack]:
                    if (mask & p_highbit) == mask:
                        p_progress[p_depth] = mask
                        if p_depth >= depth_limit:
                            store(p_progress)
                        else:
                            easy_solve(p_highbit & ~mask, p_extra-dx, p_progress, p_depth+1)
        p_highbit ^= 1 << least

def fast_solve(p_highbit:int, p_extra:int, p_progress:array, p_depth:int=0):
    """RECURSIVE solving algorithm
       >> WARNING: small changes in parameters can lead to massive increases in run time and memory usage!"""
    global solve_count
    solve_count += 1
    if time.perf_counter() - interim > 10.0:
        memory_check()

    depth_limit = num_words - 1
    for dx in range(p_extra + 1):
        least = p_highbit.bit_length()-1
        for pack in word_pack[least]:
            required = decompress(pack)
            if (p_highbit & required) == required:
                for mask in word_pack[least][pack]:
                    if (mask & p_highbit) == mask:
                        p_progress[p_depth] = mask
                        if p_depth >= depth_limit:
                            store(p_progress)
                        else:
                            fast_solve(p_highbit & ~mask, p_extra-dx, p_progress, p_depth+1)
        p_highbit ^= 1 << least

def run():
    """process a list of words to find groups of words of the same length with each having unique letters"""
    global word_pack
    word_pack = [{} for _ in range(num_letters)]
    extra = num_letters - (word_size * num_words)
    lgr.info(f"num extra letters = {extra}")

    words = []
    wf = json.load( open(WORD_FILE) )
    for word in wf:
        if len(word) == word_size:
            mask = 0
            for lett in word:
                lx = ordered_letters.find(lett)
                if lx < 0:
                    break
                bx = 1 << lx
                if mask & bx:
                    break
                mask |= bx
            else:
                words.append(word)
                word_names.setdefault( mask, [] ).append(word)
                least = mask.bit_length() - 1
                pack = compress(mask)
                word_pack[least].setdefault( pack, set() ).add(mask)
    lgr.info(f"found {len(words)} uniquely-lettered {word_size}-letter words.")
    if save_option and len(words) <= MAX_SAVE_COUNT:
        save_to_json(f"{word_size}-lett-from{num_letters}_find-unique-words", words)

    initializer = ()
    for _ in range(num_words):
        initializer += (0,)
    lgr.info(f"% virtual memory = {psutil.virtual_memory().percent};  % swap memory = {psutil.swap_memory().percent}")
    solve( (1 << num_letters) - 1, p_extra = extra, p_progress = array.array('L', initializer) )
    lgr.info("solve count = {:,}".format(solve_count))

    # display some output
    display_count = 32
    lgr.info(f"\n\t\t\t {"" if group_count <= display_count else "Sample of"} Solutions:")
    cx = 0
    tx = group_count // display_count
    for index in results.keys():
        if group_count <= display_count:
            lgr.info(results[index])
        else:
            cx += 1
            if cx % tx == 0:
                lgr.info(f"{cx}: {results[index]}")
    lgr.info("total # of groups = {:,}".format(group_count))

    if save_option and group_count <= MAX_SAVE_COUNT:
        lgr.info(f"\nsolve and display elapsed time = {time.perf_counter()-start}")
        json_save_name = save_to_json(f"{word_size}x{num_words}f{num_letters}_find-unique-words", results)
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
    word_sz = args.wordsize if MIN_WORDSIZE <= args.wordsize <= MAX_WORDSIZE else DEFAULT_WORDSIZE
    lgr.info(f"find words of {word_sz} letters.")
    num_wds = args.numwords if MIN_NUMWORDS <= args.numwords <= MAX_NUMWORDS else DEFAULT_NUMWORDS
    lgr.info(f"find {num_wds} words.")
    if word_sz * num_wds > MAX_NUMLETTERS:
        raise Exception(f">> INVALID wordsize [{word_sz}] & numwords [{num_wds}] combination!")
    num_letts = args.numletters if (word_sz * num_wds) <= args.numletters <= MAX_NUMLETTERS else min((word_sz * num_wds + 2), MAX_NUMLETTERS)
    lgr.info(f"total number of letters = {num_letts}")
    return args.save, word_sz, num_wds, num_letts


if __name__ == '__main__':
    start = time.perf_counter()
    interim = start
    log_control = MhsLogger( get_base_filename(__file__), con_level = DEFAULT_LOG_LEVEL )
    lgr = log_control.get_logger()
    solve = fast_solve
    solve_count = 0
    group_count = 0
    word_names = {}
    word_pack = []
    results = {}
    code = 0
    try:
        save_option, word_size, num_words, num_letters = prep_args(argv[1:])
        ordered_letters = ORDERED_LETTERS[:num_letters]
        lgr.info(f"letters being used: '{ordered_letters}'")
        lgr.info(f"Find groups of {num_words} 'uniquely-lettered' {word_size}-letter words.")
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
    lgr.info(f"% virtual memory = {psutil.virtual_memory().percent};  % swap memory = {psutil.swap_memory().percent}")
    lgr.info(f"\nfinal elapsed time = {time.perf_counter() - start}")
    exit(code)
