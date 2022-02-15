##############################################################################################################################
# coding=utf-8
#
# words.py -- manipulate a words dict
#
# Copyright (c) 2022 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2022-02-15"
__updated__ = "2022-02-15"

from sys import path
path.append("/home/marksa/git/Python/utils")
from mhsUtils import save_to_json
from words_2019 import eng_words

newdict = {}
ie = 0
for item in eng_words:
    newdict[item] = len(item)
    ie += 1

print(f"eng_words count = {ie}\n")

ni = 0
for item in newdict:
    print(f"newdict[{item}] = {newdict[item]}")
    ni += 1
    if ni > 30:
        break

save_to_json("len_words", newdict)
