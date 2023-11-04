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
__updated__ = "2023-11-03"

import array
import json
import time
from sys import argv
from mhsUtils import save_to_json

start = time.perf_counter()
WORD_FILE = "scrabble-plus.json"
# highest to lowest letter frequencies in Scrabble '5-13 letter' words
ORDERED_LETTERS = "ESIARNOTLCDUPMGHBYFKVWZXQJ"
DEFAULT_NUMLETTERS = len(ORDERED_LETTERS)
MIN_NUM_LETTERS = 12
MAX_WORDSIZE = 15
DEFAULT_WORDSIZE = 5
DEFAULT_INITIALIZER = (0, 0, 0, 0, 0)
MAX_NUMWORDS = len(DEFAULT_INITIALIZER)
MIN_NUMWORDS = 2

# global vars
count = 0
wordnames = {}
output = {}

def compress(cmask:int):
    return (cmask^(cmask - 1)).bit_length() - 1

def decompress(dpack:int):
    return 1<<dpack

def store(group:array):
    global count
    group = sorted( next(iter(wordnames[wmask])) for wmask in group )
    output[count] = group
    count += 1

def solve(highbit:int, p_extra:int, progress:array, depth:int=0):
    depth_limit = num_words - 1
    for dx in range(p_extra + 1):
        least = highbit.bit_length() - 1
        for pack in lc_letter[least]:
            required = decompress(pack)
            if(highbit & required) == required:
                for mask in lc_letter[least][pack]:
                    if(mask & highbit) == mask:
                        progress[depth] = mask
                        if depth >= depth_limit:
                            store(progress)
                        else:
                            solve(highbit & ~mask, p_extra - dx, progress, depth + 1)
        highbit ^= 1<<least

def main_find():
    """process a list of words to find groups of words of the same length with each having unique letters"""
    ct = 0
    least = 0
    wf = json.load( open(WORD_FILE) )
    for word in wf:
        if len(word) == word_size:
            ct += 1
            mask = 0
            for lett in word:
                lx = ordered_letters.find(lett)
                if 0 > lx >= num_letters:
                    break
                bx = 1<<lx
                if mask & bx:
                    break
                mask |= bx
            else:
                least = mask.bit_length() - 1
                pack = compress(mask)
                wordnames.setdefault( mask, set() ).add(word)
                lc_letter[least].setdefault(pack, set()).add(mask)

    # DEBUG
    print(f"found {ct} words.")
    print(f"len wordnames = {len(wordnames)}")
    print(f"last 'least' = {least}")
    print(f"len lc_letter[least] = {len(lc_letter[least])}")
    print(f"lc_letter[least] = {lc_letter[least]}")

    initializer = DEFAULT_INITIALIZER
    if num_words == 4:
        initializer = (0, 0, 0, 0)
    elif num_words == 3:
        initializer = (0, 0, 0)
    elif num_words == MIN_NUMWORDS:
        initializer = (0, 0)
    solve((1<<num_letters) - 1, extra, array.array('L', initializer))

    # sample some of the output
    print(f"\nsolutions:")
    nx = 0
    for index in output.keys():
        print(output[index])
        nx += 1
        if nx > 30:
            break
    print(f"total groups = {count}")

    print(f"\nelapsed time = {time.perf_counter() - start}")
    if save_option.upper()[0] == 'Y' and len(save_option) <= 4:
        save_to_json(f"{word_size}x{num_words}f{num_letters}_words", output)


if __name__ == '__main__':
    print(f"argv = {argv}")
    save_option = "No"
    if len(argv) > 1 and argv[1].isalpha():
        save_option = argv[1]
    print(f"save option = '{save_option}'")

    word_size = DEFAULT_WORDSIZE
    if len(argv) > 2:
        request = int(argv[2])
        if MAX_WORDSIZE >= request > DEFAULT_WORDSIZE:
            print(f"requested word size = {request}")
            word_size = request
    num_words = MAX_NUMWORDS
    if len(argv) > 3:
        request = int(argv[3])
        print(f"number of words requested = {request}")
        if MAX_NUMWORDS > request >= MIN_NUMWORDS:
            num_words = request
    ordered_letters = ORDERED_LETTERS
    if len(argv) > 4:
        request = int(argv[4])
        print(f"number of letters requested = {request}")
        if MIN_NUM_LETTERS <= request < DEFAULT_NUMLETTERS:
            ordered_letters = ORDERED_LETTERS[:request]

    # make sure the parameters for size of words & number of words and letters are safe and sensible
    num_letters = len(ordered_letters)
    print(f"letters to use are: '{ordered_letters}'")
    if word_size * num_words > num_letters:
        word_size = DEFAULT_WORDSIZE
        num_words = num_letters // DEFAULT_WORDSIZE
    print(f"find {num_words} 'uniquely lettered' words each with {word_size} letters.")
    extra = num_letters - (word_size * num_words)
    print(f"num extra letters = {extra}\n")
    lc_letter = [{} for f in range(num_letters)]

    main_find()
    print(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
