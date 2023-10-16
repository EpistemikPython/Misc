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
__updated__ = "2023-10-16"

import array
import time
from sys import argv
from mhsUtils import save_to_json
from scrabble_words_2019 import scrabble

# highest to lowest letter frequencies in Scrabble 5-letter words
ordered_letters = 'seaoriltnudycpmhgbkfwvzjxq'
default_num_letts = len(ordered_letters)
min_num_letts = 12
wordnames = {}
output = {}
count = 0
default_wordsize = 5
default_initializer = (0, 0, 0, 0, 0)
default_numwords = len(default_initializer)
min_numwords = 2

def compress(cword:int):
    return (cword ^ (cword - 1)).bit_length() - 1

def decompress(dpack:int):
    return 1<<dpack

def store(group:array):
    global count
    group = sorted( next(iter(wordnames[word])) for word in group )
    output[count] = group
    count += 1

def solve(alphabet:int, num_wrds:int, grace:int, progress:array, depth:int=0):
    depth_limit = num_wrds - 1
    for drop in range(grace + 1):
        first = alphabet.bit_length() - 1
        for pack in firstletter[first]:
            required = decompress(pack)
            if( alphabet & required ) == required:
                for mask in firstletter[first][pack]:
                    if( mask & alphabet ) == mask:
                        progress[depth] = mask
                        if depth >= depth_limit:
                            store(progress)
                        else:
                            solve(alphabet & ~mask, num_wrds, grace - drop, progress, depth + 1)
        alphabet ^= 1<<first

def main_find(save_option:str, word_sz:int, num_wds:int):
    print(f"letters to use are: '{ordered_letters}'")
    print(f"find {num_wds} 'uniquely lettered' words each with {word_sz} letters.")
    print(f"save option = '{save_option}'")
    start = time.perf_counter()

    for word in scrabble.keys():
        if len(word) == word_sz:
            mask = 0
            word = word.lower()
            for lett in word:
                i = ordered_letters.find(lett)
                if not(0 <= i < num_letts):
                    break
                b = 1<<i
                if mask & b:
                    break
                mask |= b
            else:
                first = mask.bit_length() - 1
                pack = compress(mask)
                wordnames.setdefault( mask, set() ).add(word)
                firstletter[first].setdefault( pack, set() ).add(mask)

    alphabet = (1<<num_letts) - 1
    initializer = default_initializer
    if num_wds == 4:
        initializer = (0, 0, 0, 0)
    elif num_wds == 3:
        initializer = (0, 0, 0)
    elif num_wds == min_numwords:
        initializer = (0, 0)
    grace = num_letts - (word_sz * num_wds)
    if grace < 0:
        print(f"BAD grace = {grace}!")
        exit(grace)
    print(f"grace = {grace}\n")
    solve(alphabet, num_wds, grace, array.array('L', initializer))

    # sample some of the output
    nx = 0
    for index in output.keys():
        print(output[index])
        nx += 1
        if nx > 30:
            break
    print(f"total groups = {count}")
    print(f"\nelapsed time = {time.perf_counter() - start}")

    save_option = save_option.upper()
    if save_option[0] == 'Y' and len(save_option) <= 4:
        save_to_json(f"{word_sz}x{num_wds}f{num_letts}_words", output)
        print(f"\nelapsed time = {time.perf_counter() - start}")


if __name__ == '__main__':
    save_opt = 'No'
    word_size = default_wordsize
    num_words = default_numwords
    num_letters_to_use = default_num_letts
    print(f"argv = {argv}")

    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]
    if len(argv) > 2:
        word_size = int(argv[2])
        print(f"requested word size = {word_size}")
    if len(argv) > 3:
        num_words = int(argv[3])
        print(f"number of words requested = {num_words}")
    if len(argv) > 4:
        num_letters_to_use = int(argv[4])
        print(f"number of letters requested = {num_letters_to_use}")

    # make sure all the parameters regarding size of words and number of words and letters are safe and sensible
    if default_numwords < num_words < min_numwords:
        num_words = default_numwords
    if min_num_letts <= num_letters_to_use < default_num_letts:
        ordered_letters = ordered_letters[:num_letters_to_use]
    if word_size * num_words > num_letters_to_use:
        word_size = default_wordsize
        num_words = num_letters_to_use // default_wordsize
    num_letts = len(ordered_letters)
    print(f"using {num_letts} letters")
    firstletter = [{} for f in range(num_letts)]

    main_find(save_opt, word_size, num_words)
    exit()
