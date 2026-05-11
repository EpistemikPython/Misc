##############################################################################################################################
# coding=utf-8
#
# check_distinct_letters.py
#   -- user can continuously enter a word in a terminal and find out how many distinct letters each has
#
# Copyright (c) 2026 Mark Sattolo <epistemik@gmail.com>

__author__         = "Mark Sattolo"
__author_email__   = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2026-05-07"
__updated__ = "2026-05-08"

from sys import path, argv
path.append("/home/marksa/git/Python/utils")
from mhsUtils import get_filename

def run():
    """User can continuously enter a word in a terminal and find out how many distinct letters each has."""
    while True:
        word = input("Enter a word to check ('EXIT' to quit): ")
        result = ""
        if word == "EXIT":
            print("Bye!\n")
            break
        for it in word:
            if not it.isalpha():
                continue
            lett = it.upper()
            if lett not in result:
                result += lett
        lres = len(result)
        print(f"{lres} distinct letter{'s' if lres > 1 else ''}: [{result}]" if result else "No letters entered!")


if __name__ == '__main__':
    if len(argv) > 1:
        print(f"Usage: python3 {get_filename(argv[0])}\nEnter a word and find out how many distinct letters it has.")
        exit(0)
    code = 0
    try:
        run()
    except KeyboardInterrupt as mki:
        print(mki)
        code = 13
    except ValueError as mve:
        print(mve)
        code = 27
    except Exception as mex:
        print(mex)
        code = 66
    exit(code)
