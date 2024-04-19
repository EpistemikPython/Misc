##############################################################################################################################
# coding=utf-8
#
# sound_test.py -- play a brief sound every 12 minutes
#
# Copyright (c) 2024 Mark Sattolo <epistemik@gmail.com>

__author__ = "Mark Sattolo"
__author_email__ = "epistemik@gmail.com"
__python_version__ = "3.6+"
__created__ = "2024-04-19"
__updated__ = "2024-04-19"

from playsound import playsound
import time

while True:
    # play a brief sound every 13 minutes
    playsound('/home/marksa/Music/track77.mp3')
    time.sleep(779)
