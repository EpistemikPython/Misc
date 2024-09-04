##############################################################################################################################
# coding=utf-8
#
# sound_test.py
#   -- play a sound file every n seconds
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-04-19"
__updated__ = "2024-09-02"

from sys import argv
import time
import os.path as osp
import playsound as ps

DEFAULT_TRACK = "/home/marksa/Music/track77.mp3"
DEFAULT_TIME = 793
MIN_TIME = 9
MAX_TIME = 9999

def run():
    while True:
        # play a sound file every $interval seconds
        ps.playsound(filename)
        time.sleep(interval)


if __name__ == '__main__':
    interval = DEFAULT_TIME
    filename = DEFAULT_TRACK
    code = 0
    try:
        if len(argv) > 1:
            if argv[1].isnumeric():
                interval = int(argv[1])
                if interval < MIN_TIME or interval > MAX_TIME:
                    interval = DEFAULT_TIME
                if len(argv) > 2 and osp.isfile(argv[2]):
                    filename = argv[2]
            else:
                print(f"Play a sound file every <delay> seconds.\n"
                      f"Usage: python3 {argv[0]} <delay in seconds, {MIN_TIME}..{MAX_TIME}; DEFAULT = {DEFAULT_TIME}> "
                      f"<path to custom sound file; DEFAULT = {DEFAULT_TRACK}>")
                code = 27
        if not code:
            run()
    except KeyboardInterrupt:
        print(">> User interruption.")
        code = 13
    except ValueError:
        print(">> Value error.")
        code = 39
    except Exception as mex:
        print(f"Problem: {repr(mex)}.")
        code = 66
    exit(code)
