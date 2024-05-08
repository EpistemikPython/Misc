##############################################################################################################################
# coding=utf-8
#
# sound_test.py -- play a sound file every n minutes
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-04-19"
__updated__ = "2024-05-08"

import sys
import time
import os.path as osp
import playsound as ps

DEFAULT_TRACK = "/home/marksa/Music/track77.mp3"
DEFAULT_TIME = 793

def run(filename:str, interval:int):
    while True:
        # play a brief sound every 13 minutes
        ps.playsound(filename)
        time.sleep(interval)


if __name__ == '__main__':
    ival = DEFAULT_TIME
    sdfn = DEFAULT_TRACK
    code = 0
    posn = 1
    try:
        if len(sys.argv) > posn and sys.argv[posn].isnumeric():
            ival = int(sys.argv[posn])
        posn = 2
        if len(sys.argv) > posn and osp.isfile(sys.argv[posn]):
            sdfn = sys.argv[posn]
        run(sdfn, ival)
    except KeyboardInterrupt:
        code = 13
    except Exception as ex:
        code = 66
    exit(code)
