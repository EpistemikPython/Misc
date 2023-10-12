##############################################################################################################################
# coding=utf-8
#
# find_words.py -- process a scrabble words dict to record the score of each word
# adapted from: https://github.com/sh1boot/fivewords.git
#
# Copyright (c) 2023 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-10"
__updated__ = "2023-10-11"

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
    return 'aesiorunltycdhmpgkbwfvzjxq'.find(clb)
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

def solve(alphabet, num_wds, grace = 1, progress = array.array('L', (0, 0, 0, 0, 0)), depth=0):
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

def main_find(save_option, word_sz=5, num_wds=5):
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
    solve(alphabet, num_wds)
    # print(output)
    for index in output.keys():
        print(output[index])
    print(f"total groups = {count}")
    print(f"\nelapsed time = {time.perf_counter() - start}")

    save_option = save_option.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json(f"{word_sz}x{num_wds}_words", output)


if __name__ == '__main__':
    save_opt = 'No'
    word_size = 5
    num_words = 5
    print(f"argv = {argv}")
    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]
    if len(argv) > 2 and argv[2].isalpha():
        word_size = int(argv[2])
    if len(argv) > 3 and argv[3].isalpha():
        num_words = int(argv[3])
    main_find(save_opt, word_size, num_words)
    exit()
