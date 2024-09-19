##############################################################################################################################
# coding=utf-8
#
# find_pangrams.py
#   -- from a word list file, find all non-uppercase pangrams and make UPPERCASE and save in a copy of the input file
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-09-13"
__updated__ = "2024-09-19"

import time
from sys import path, argv
import os.path as osp
path.append("/home/marksa/git/Python/utils")
from mhsUtils import FILE_DATETIME_FORMAT, JSON_LABEL, get_current_time

start = time.perf_counter()
DEFAULT_INFILE  = "./input/SpellBeeTest.json"
ANSWER_KEY = "answers"
END_KEY    = "]"

outfile_name = osp.join("output", "pangrams" + '_' + get_current_time(FILE_DATETIME_FORMAT) + osp.extsep + JSON_LABEL)

def is_pangram(p_line:str) -> bool:
    testline = p_line.strip(', \n')
    # print(f"\ntesting {testline}", end = None)
    # check if already uppercase
    if testline == testline.upper():
        return False
    result = ""
    for lett in testline:
        # print(f"testing '{lett}'")
        if not lett.isalpha():
            continue
        if lett not in result:
            result += lett
    # print(f"result = '{result}'")
    if len(result) == 7:
        print(f">> {testline} is a Pangram!")
        return True
    return False

def run():
    """Open a spellingbee results json file and find non-uppercase pangrams and convert to UPPERCASE and save results to a new file."""
    with open(infile) as file_in:
        with open(outfile_name, 'w') as file_out:
            search_state = False
            for line in file_in:
                # print(line, end = None)
                newline = line
                if END_KEY in line:
                    search_state = False
                if search_state and is_pangram(line):
                    newline = line.upper()
                file_out.write(newline)
                if ANSWER_KEY in line:
                    search_state = True
    print(f"\nSaved results to: {outfile_name}")


if __name__ == '__main__':
    code = 0
    infile = None
    try:
        if len(argv) == 1:
            infile = DEFAULT_INFILE
        elif len(argv) == 2 and osp.isfile(argv[1]):
            infile = argv[1]
        else:
            print(f"usage: python3 {argv[0]} <input file>")
        if infile:
            run()
            print(f"\nfinal elapsed time = {time.perf_counter()-start}")
    except KeyboardInterrupt:
        print(">> User interruption.")
        code = 13
    except Exception as ex:
        print(f"Problem >> '{repr(ex)}'")
        code = 66
    exit(code)
