##############################################################################################################################
# coding=utf-8
#
# mhsLogging.py -- custom logging
#
# Copyright (c) 2021 Mark Sattolo <epistemik@gmail.com>

__author__       = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__created__ = "2021-05-03"
__updated__ = "2021-05-03"

import logging
import os.path as osp
from datetime import datetime as dt

JSON = "json"
FXN_TIME_STR:str  = "%H:%M:%S:%f"
CELL_TIME_STR:str = "%H:%M:%S"
CELL_DATE_STR:str = "%Y-%m-%d"
FILE_DATE_STR:str = "D%Y-%m-%d"
FILE_TIME_STR:str = "T%Hh%M"
FILE_DATETIME_FORMAT = FILE_DATE_STR + FILE_TIME_STR
RUN_DATETIME_FORMAT  = CELL_DATE_STR + '_' + FXN_TIME_STR

now_dt:dt  = dt.now()
run_ts:str = now_dt.strftime(RUN_DATETIME_FORMAT)
# print(F"{__file__}: run_ts = {run_ts}")
file_ts:str = now_dt.strftime(FILE_DATETIME_FORMAT)
# print(F"{__file__}: file_ts = {file_ts}")

SIMPLE_FORMAT:str  = "%(levelname)-8s - %(filename)s[%(lineno)s]: %(message)s"
COMPLEX_FORMAT:str = "%(levelname)-8s | %(filename)s:%(funcName)-16s[l.%(lineno)s]  %(message)s"

FILE_LEVEL    = logging.DEBUG
CONSOLE_LEVEL = logging.WARNING

# set up logging to file
logging.basicConfig( level = FILE_LEVEL,
                     format = COMPLEX_FORMAT,
                     datefmt = RUN_DATETIME_FORMAT,
                     filename = F"logs/asm_{file_ts}.log",
                     filemode = 'w')

# define a Handler which writes messages to sys.stderr
console = logging.StreamHandler()
console.setLevel(CONSOLE_LEVEL)

# set a format which is simpler for console use
formatter = logging.Formatter(SIMPLE_FORMAT)

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)


def get_base_filename(p_name:str, file_div:str=osp.sep, sfx_div:str=osp.extsep) -> str:
    spl1 = p_name.split(file_div)
    if spl1 and isinstance(spl1, list):
        spl2 = spl1[-1].split(sfx_div)
        if spl2 and isinstance(spl2, list):
            return spl2[0]
    return ""