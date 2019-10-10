#!/usr/bin/python3

import argparse
import datetime
import json
import math
import multiprocessing
import os
import sys
import time

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CALIBRATION_DIR = os.path.dirname(CURRENT_DIR)
CONFIG_DIR = os.path.join(CALIBRATION_DIR, "conf")
SRC_DIR = os.path.join(CALIBRATION_DIR, "src")

BASE_DIR = os.path.dirname(CALIBRATION_DIR)
SHARED_DIR = os.path.join(BASE_DIR, "shared")

GATHER_DIR = os.path.join(SRC_DIR, "gather")
ADCCAL_GATHER_METHOD_DIR = os.path.join(GATHER_DIR, "adccal", "methods")
PTCCAL_GATHER_METHOD_DIR = os.path.join(GATHER_DIR, "ptccal", "methods")

PROCESS_DIR = os.path.join(SRC_DIR, "process")
ADCCAL_PROCESS_METHOD_DIR = os.path.join(PROCESS_DIR, "adccal", "methods")
PTCCAL_PROCESS_METHOD_DIR = os.path.join(PROCESS_DIR, "ptccal", "methods")

if SHARED_DIR not in sys.path:
    sys.path.insert(0, SHARED_DIR)

import utils  # noqa E402


def get_arguments:
    global CONFIG_DIR

    parser = argparse.ArgumentParser(description="Calibration tools for P2M")
    parser.add_argument("-i", "--input",
                        dest="input",
                        type=str,
                        help=("Path of input directory containing HDF5 files "
                              "to analyse"))
    parser.add_argument("-o", "--output",
                        dest="output",
                        type=str,
                        help="Path of output directory for storing files")
    parser.add_argument("-r", "--run",
                        dest="run_id",
                        type=str,
                        help="Non-changing part of file name")
    parser.add_argument("-m", "--method",
                        dest="method",
                        type=str,
                        help="Method to use during the analysis: "
                             "process_adccal_default, "
                             "None")
    parser.add_argument("-t", "--type",
                        dest="run_type",
                        type=str,
                        help="Run type: gather, process")

    parser.add_argument("--n_cols",
                        help="The number of columns to be used for splitting "
                             "into subsets (to use all, set n_cols to None)")

    parser.add_argument("--config_file",
                        type=str,
                        default="default.yaml",
                        help="The name of the config file.")

    args = parser.parse_args()

    args.config_file = os.path.join(CONFIG_DIR, args.config_file)
    if not os.path.exists(args.config_file):
        msg = ("Configuration file {} does not exist."
               .format(args.config_file))
        parser.error(msg)

    return args

class SubmitJobs(object):
    def __init__(self):




