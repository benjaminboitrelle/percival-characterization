#!/usr/bin/python3

import argparse
import datetime
import json
import math
import multiprocessing
import os
import sys
import time
from collections import defaultdict

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
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


def get_arguments():
    global CONFIG_DIR

    parser = argparse.ArgumentParser(description="P2M job submission tools")
    parser.add_argument("-e", "--email",
                        dest="email",
                        type=str,
                        help="Email address for sending notification")
    parser.add_argument("-t", "--type",
                        dest="run_type",
                        type=str,
                        help="Run type: gather, process")
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

def insert_args_into_config(args, config):

    # general
    if "general" not in config:
#        print(config)
        config = defaultdict(dict)

    c_general = config["general"]

    try:
        c_general["run_type"] = args.run_type or c_general["run_type"]
    except KeyError:
        raise Exception("No run_type specified. Abort.")
        sys.exit(1)

    try:
        c_general["email"] = args.email or c_general["email"]
    except KeyError:
        raise Exception("No run_id specified. Abort.")
        sys.exit(1)


class SubmitJobs(object):
    def __init__(self):
        global CONF_DIR
        global CALIBRATION_DIR
        # Get command line arguments
        args = get_arguments()

        # Load user config file
        config_usr = args.config_file

#        yaml_usr = os.path.join(CONFIG_DIR, "{}".format(config_usr))
        config = dict()
        config = utils.load_config(config_usr)
        insert_args_into_config(args, config)

        print("Configuration:")
        print(json.dumps(config_usr, sort_keys=True, indent=4))
        try:
            self.mail_address = config["general"]["email"]
        except KeyError:
            self.mail_address = None
        print(self.mail_address)


if __name__ == "__main__":

    obj = SubmitJobs()
