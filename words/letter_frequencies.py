##############################################################################################################################
# coding=utf-8
#
# letter_frequencies.py -- get the frequency of each letter in words of specified lengths from a word file
#
# Copyright (c) 2022 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2023-10-29"
__updated__ = "2023-10-29"

import time
import json
from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json

start = time.perf_counter()
ordered_letters = 'SEAORILTNUDYCPMHGBKFWVZJXQ'
# ordered_letters = ['s','e','a','o','r','i','l','t','n','u','d','y','c','p','m','h','g','b','k','f','w','v','z','j','x','q']
numletters = len(ordered_letters)
freqs = {}
for lett in ordered_letters:
    freqs[lett] = 0
# freqs = [0 for f in range(numletters)]
lower = 5
upper = 9

def main_words(save_option:str):
    print(f"lower word size = {lower}")
    print(f"upper word size = {upper}")
    wct = lct = 0
    scp = json.load(open("scrabble-plus.json"))
    for item in scp:
        if lower <= len(item) <= upper:
            for letter in item:
                freqs[letter] += 1
                lct += 1
            wct += 1

    print(f"word count = {wct}\n")
    print(f"letter count = {lct}\n")
    print(f"letter frequencies:")
    for key in freqs.keys():
        print(f"{key}: {freqs[key]}")

    save_option = save_option.upper()
    if save_option == 'Y' or save_option == 'YES':
        save_to_json("letter_frequencies", freqs)


if __name__ == '__main__':
    save_opt = 'No'
    if len(argv) > 1 and argv[1].isalpha():
        save_opt = argv[1]
    main_words(save_opt)
    print(f"\nelapsed time = {time.perf_counter() - start}")
    exit()
