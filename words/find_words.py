##############################################################################################################################
# coding=utf-8
#
# find_words.py -- process a list of words to find a group of words of the same length with each having unique letters
# adapted from: https://github.com/sh1boot/fivewords.git
# see: https://www.youtube.com/watch?v=c33AZBnRHks
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-10"
__updated__ = "2023-10-15"

import array
import time
from sys import argv
from mhsUtils import save_to_json
from scrabble_words_2019 import scrabble

# highest to lowest letter frequencies in scrabble 5-letter words
ordered_letters = 'seaoriltnudycpmhgbkfwvzjxq'
default_num_letts = len(ordered_letters)
min_num_letts = 12
wordnames = {}
output = {}
count = 0
default_wordsize = 5
five_words_initializer = (0, 0, 0, 0, 0)
default_numwords = len(five_words_initializer)
four_words_initializer = (0, 0, 0, 0)
three_words_initializer = (0, 0, 0)
two_words_initializer = (0, 0)

def compress(cword):
    return (cword ^ (cword - 1)).bit_length() - 1

def decompress(dpack):
    return 1<<dpack

def store(group):
    global count
    group = sorted( next( iter(wordnames[word]) ) for word in group )
    output[count] = group
    count += 1

def solve(alphabet, num_wrds, grace, progress, depth=0):
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

#TODO: Add a parameter to set the number of letters used
def main_find(save_option, word_sz, num_wds):
    print(f"find {num_wds} 'uniquely lettered' words each with {word_sz} letters.")
    print(f"letters to use are: '{ordered_letters}'")
    print(f"save option = '{save_option}'\n")
    start = time.perf_counter()

    for word in scrabble.keys():
        if len(word) == word_sz:
            mask = 0
            word = word.lower()
            for lett in word:
                i = ordered_letters.find(lett)
                if not(0 <= i < lett_range):
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

    alphabet = (1<<lett_range) - 1
    initializer = five_words_initializer
    if num_wds == 4:
        initializer = four_words_initializer
    elif num_wds == 3:
        initializer = three_words_initializer
    elif num_wds == 2:
        initializer = two_words_initializer
    grace = lett_range + 1 - (word_sz * num_wds)
    if grace < 0:
        print(f"BAD grace = {grace}!")
        exit(grace)
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
    if save_option == 'Y' or save_option == 'YES':
        save_to_json(f"{word_sz}x{num_wds}_words", output)
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
    if len(argv) > 3:
        num_words = int(argv[3])
    if len(argv) > 4:
        num_letters_to_use = int(argv[4])

    if min_num_letts <= num_letters_to_use < default_num_letts:
        ordered_letters = ordered_letters[:num_letters_to_use]
    print(f"number of letters to use = '{num_letters_to_use}'")
    if word_size * num_words > num_letters_to_use:
        word_size = default_wordsize
        num_words = num_letters_to_use // default_wordsize
    lett_range = len(ordered_letters)
    firstletter = [{} for f in range(lett_range)]

    main_find(save_opt, word_size, num_words)
    exit()
