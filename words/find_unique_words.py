##############################################################################################################################
# coding=utf-8
#
# find_unique_words.py
#   -- process a list of words to find groups of words of the same length with each having unique letters
# see: https://www.youtube.com/watch?v=c33AZBnRHks
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-10"
__updated__ = "2024-12-08"

import logging
import time
import psutil
from argparse import ArgumentParser
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import json, save_to_json, get_base_filename, get_filename
from mhsLogging import MhsLogger, DEFAULT_LOG_LEVEL

# 3-letter testing
# WORD_FILE = "input/three-letter_test-1.json"
# 5-letter testing
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
MAX_SAVE_COUNT = 2000000

def bin_dsp(p_bin:int, p_name:str= "mask"):
    return p_name + " = {:>010b}; ".format(p_bin)

def memory_check():
    global interim
    lgr.info(f"\n\t\t\t\tINTERIM TIME = {time.perf_counter() - start}")
    lgr.info("solve count = {:,}".format(solve_count))
    lgr.info("group count = {:,}".format(group_count))
    vmp = psutil.virtual_memory().percent
    smp = psutil.swap_memory().percent
    lgr.info(f"% virtual memory = {vmp};  % swap memory = {smp}")
    if vmp > 95.0 and smp > 80.0:
        raise Exception(f">> EXCEEDED memory parameters: v = {vmp} | s = {smp} !!")
    interim = time.perf_counter()

class WordContainer:
    """store word with its mask"""
    def __init__(self, p_word:str, p_mask:int):
        self.word = p_word
        self.mask = p_mask

    def get_word(self):
        return self.word

    def get_mask(self):
        return self.mask

    def get_contents(self):
        return f"{self.word}; " + bin_dsp(self.mask)

def list_display(p_groups:list[WordContainer], p_lev:int=logging.INFO):
    if p_groups:
        for item in p_groups:
            lgr.log(p_lev, item.get_contents())
    else:
        lgr.log(p_lev, "NO groups!")

class SolutionStore:
    def __init__(self):
        self.results = []
        self.count = 0

    def size(self):
        return self.count

    def add(self, p_group:list[WordContainer]):
        copy_list = [_ for _ in p_group]
        self.results.append(copy_list)
        # lgr.info("\n\t\t\t\t>> ADDED a group to SolutionStore:")
        self.count += 1
        # self.display()

    def get(self):
        reply = []
        for lx in self.results:
            grp = []
            for item in lx:
                grp.append(item.get_word())
            reply.append(sorted(grp))
        return [ordered_letters] + sorted(reply)

    def display(self):
        num = self.count
        if num == 0:
            lgr.info(f"NO groups found!")
        else:
            lgr.info("Found {:,} unique groups.".format(num))
        display_count = 32
        lgr.info(f"\n\t\t\t {"" if num <= display_count else "Sample of"} Solutions:")
        cx = 0
        tx = num // display_count
        for lx in self.results:
            cx += 1
            if num <= display_count:
                lgr.info(f"Group #{cx}")
                for item in lx:
                    lgr.info(f"\t{item.get_word()}:{item.get_mask()}")
                lgr.info("\n")
            else:
                if cx % tx == 0:
                    lgr.info(f"Group #{cx}")
                    for item in lx:
                        lgr.info(f"\t{item.get_word()}:{item.get_mask()}")
                    lgr.info("\n")

def display_new(p_lev:int=logging.NOTSET):
    count = 0
    for k in range(word_size-1, num_letters):
        if k in easy_word_pack.keys():
            for lx in easy_word_pack[k]:
                count += 1
                lxwd = lx.get_word()
                lxmk = lx.get_mask()
                lgr.log(p_lev, "{:>4}) ".format(count) + f"{lxwd} = {k} | " + bin_dsp(lxmk))

def get_words_new():
    count = 0
    words = []
    wf = json.load(open(WORD_FILE))
    for word in wf:
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
                count += 1
                words.append(word)
                least = mask.bit_length()-1
                easy_word_pack.setdefault(least, []).append(WordContainer(word, mask))
    lgr.info(f"found {count} uniquely-lettered {word_size}-letter words.")
    # display_easy()
    if save_option and count <= MAX_SAVE_COUNT:
        json_save_name = save_to_json(f"{word_size}-uniq-letts_from-{ordered_letters}_easy-unique-words", [ordered_letters]+sorted(words))
        lgr.info(f"Saved found words list to: {json_save_name}")

def solve_new(p_highbit:int, p_testmask:int, p_progress:list[WordContainer]):
    """RECURSIVE solving algorithm
       >> WARNING: small changes in parameters can lead to massive increases in run time and memory usage!"""
    # loglev = logging.NOTSET
    global solve_count
    solve_count += 1
    # lgr.log(loglev, f"\n\t\t\t\t\t{solve_count}) START: p_hb = {p_highbit}; " + bin_dsp(p_testmask, "p_testmask"))
    # list_display(p_progress, loglev)
    if word_size-1 <= p_highbit < num_letters:
        if time.perf_counter() - interim > 10.0:
            memory_check()
            lgr.info(f"\n\t\t\t\t\tSTART: p_hb = {p_highbit}; " + bin_dsp(p_testmask, "p_testmask"))
            list_display(p_progress)

        for rbit in range(p_highbit, word_size-2, -1):
            if rbit in easy_word_pack.keys():
                for kx in easy_word_pack[rbit]:
                    kxmk = kx.get_mask()
                    # lgr.log(loglev, f"word = {kx.get_word()}: p_hb = {p_highbit}; rbit = {rbit}; " +
                    #          bin_dsp(p_testmask, "p_testmask") +
                    #          bin_dsp(kxmk) + bin_dsp(kxmk & p_testmask, "mask & p_testmask"))
                    if not (kxmk & p_testmask):
                        update = p_progress + [kx]
                        if len(update) == num_words:
                            storage.add(update)
                        else:
                            solve_new(rbit-1, (kxmk | p_testmask), update)
    # else:
    #     lgr.warning(f">> INVALID high bit = {p_highbit}.\n")
    # lgr.log(loglev, f"END SOLVE # {solve_count}\n")

def run():
    """process a list of words to find groups of words of the same length with each having unique letters"""
    lgr.info(f"% virtual memory = {psutil.virtual_memory().percent};  % swap memory = {psutil.swap_memory().percent}")

    get_words_new()
    solve_new(num_letters-1, 0, [])
    lgr.info(f"storage size = {storage.size()}")

    lgr.info(f"% virtual memory = {psutil.virtual_memory().percent};  % swap memory = {psutil.swap_memory().percent}")
    lgr.info("solve count = {:,}".format(solve_count))
    # display some output
    storage.display()

    if save_option and storage.size() <= MAX_SAVE_COUNT:
        lgr.info(f"\nsolve and display elapsed time = {time.perf_counter()-start}")
        json_save_name = save_to_json(f"{word_size}x{num_words}f{num_letters}_easy-unique-words", storage.get())
        lgr.info(f"Saved group results to: {json_save_name}")

def set_args():
    arg_parser = ArgumentParser(description = "get the save-to-file, word size, number of words and number of letters options",
                                prog = f"python3 {get_filename(argv[0])}")
    # optional arguments
    arg_parser.add_argument('-s', '--save', action="store_true", default = False,
                            help = "write the results to a JSON file")
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
    solve_count = 0
    group_count = 0
    word_names = {}
    easy_word_pack = {}
    fast_word_pack = []
    results = {}
    storage = SolutionStore()
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
