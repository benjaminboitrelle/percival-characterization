#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import copy
import json
import multiprocessing
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
print("BASE_PATH:", BASE_PATH)
SRC_PATH = os.path.join(BASE_PATH, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0I, SRC_PATH)

from analyse import Analyse


class StartAnalyse(oject):
    def __init__(self):
        pass


if __name__ == "__main__":
    StartAnalyse()
