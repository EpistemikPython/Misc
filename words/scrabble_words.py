##############################################################################################################################
# coding=utf-8
#
# scrabble_words.py -- process a scrabble words dict to record the score of each word
#
# Copyright (c) 2022 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2022-03-05"
__updated__ = "2022-03-05"

from sys import path
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from scrabble_words_2019 import points, scrabble

newdict = {}
ie = 0
for item in scrabble:
    score = 0
    for i in item:
        score += points[i]
    newdict[item] = score
    ie += 1

print(f"scrabble count = {ie}\n")

ni = 0
for item in newdict:
    print(f"newdict[{item}] = {newdict[item]}")
    ni += 1
    if ni > 30:
        break

save_to_json("scrabble_words", newdict)
