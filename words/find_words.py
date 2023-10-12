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
__updated__ = "2023-10-12"

from sys import argv
import time
import itertools
import array
from scrabble_words_2019 import scrabble
from mhsUtils import save_to_json

anagrams = False
firstletter = [ {} for f in range(26) ]
wordnames = {}
output = {}
count = 0
default_wordsize = 5
default_numwords = 5
five_words_initializer = (0, 0, 0, 0, 0)
four_words_initializer = (0, 0, 0, 0)
three_words_initializer = (0, 0, 0)
ordered_letters = 'aesiorunltycdhmpgkbwfvzjxq'

# TODO: find the proper balance between these two implementations
#
# def compress(word):
#  shift = (word ^ (word - 1)).bit_length()
#  return ((shift - 1) << 8) | ((word >> shift) & 255)
#
# def decompress(pack):
#  shift = pack >> 8
#  bits = pack & 255
#  return (bits * 2 + 1) << shift

def compress(cword):
    return ( cword^(cword - 1) ).bit_length() - 1

def decompress(dpack):
    return 1<<dpack

def letter_to_bit(clb):
    return ordered_letters.find(clb)
    # return ord(c) - ord('a')

def store(progress):
    global count
    if anagrams:
        for s in itertools.product( *(wordnames[word] for word in progress) ):
            print( *sorted(s) )
            count += 1
    else:
        group = sorted( next( iter(wordnames[word]) ) for word in progress )
        # print(group)
        output[count] = group
        count += 1

def solve(alphabet, num_wds, grace, progress, depth=0):
    depth_limit = num_wds - 1
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
                            solve( alphabet & ~mask, num_wds, grace - drop, progress, depth + 1 )
        alphabet ^= 1<<first

#TODO: Add an 'exclude' parameter to exclude certain letters from consideration
def main_find(save_option, word_sz, num_wds):
    print(f"find {num_wds} unique words each with {word_sz} letters.")
    print(f"save option = '{save_option}'\n")
    start = time.perf_counter()

    for word in scrabble.keys():
        if len(word) == word_sz:
            mask = 0
            word = word.lower()
            for lett in word:
                i = letter_to_bit(lett)
                if not( 0 <= i < 26 ):
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

    alphabet = (1<<26) - 1
    initializer = five_words_initializer
    if num_wds == 4:
        initializer = four_words_initializer
    elif num_wds == 3:
        initializer = three_words_initializer
    starter = array.array('L', initializer)
    solve(alphabet, num_wds, 1, starter)
    # print(output)
    nx = 0
    for index in output.keys():
        print(output[index])
        nx += 1
        if nx > 25:
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
    print(f"argv = {argv}")
    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]
    if len(argv) > 2:
        word_size = int(argv[2])
    if len(argv) > 3:
        num_words = int(argv[3])
    main_find(save_opt, word_size, num_words)
    exit()
