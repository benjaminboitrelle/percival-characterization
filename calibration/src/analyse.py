#!/usr/bin/python3

import argparse
import os
import sys
import datetime
import time

import utils

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
CONFIG_DIR = os.path.join(BASE_DIR, "conf")
SRC_DIR = os.path.join(BASE_DIR, "src")

PROCESS_DIR = os.path.join(SRC_DIR, "process")
ADCCAL_METHOD_DIR = os.path.join(PROCESS_DIR, "adccal", "methods")
PTCCAL_METHOD_DIR = os.path.join(PROCESS_DIR, "ptccal", "methods")

if ADCCAL_METHOD_DIR not in sys.path:
    sys.path.insert(0, ADCCAL_METHOD_DIR)


class Analyse(object):
    def __init__(self,
                 in_base_dir,
                 out_base_dir,
                 run_id,
                 run_type,
                 measurement,
                 n_cols,
                 method):

        self.in_base_dir = in_base_dir
        self.out_base_dir = out_base_dir

        self._n_rows_total = 1484
        self._n_cols_total = 1440

        self._n_rows = self._n_rows_total
        if n_cols is None:
            self._n_cols = self._n_cols_total
        else:
            self._n_cols = n_cols

        self._n_parts = self._n_cols_total // self._n_cols

        self._run_id = run_id
        self.run_type = run_type

        self.measurement = measurement
        self.method = method

    def run(self):
        print("\nStarted at", str(datetime.datetime.now()))
        t = time.time()

        if self.run_type == "gather":
            self.run_gather()
        elif self.run_type == "process":
            self.run_process()
        else:
            print("Unsupported argument: run_type {}".format(self.run_type))

        print("\nFinished at", str(datetime.datetime.now()))
        print("took time: ", time.time() - t)

    def generate_raw_path(self, base_dir):
        return base_dir, "{run}_" + "{}.h5".format(self._run_id)

    def generate_metadata_path(self, base_dir):
        return base_dir, "file.dat"

    def generate_gather_path(self, base_dir):
        return base_dir, "col{col_start}-{col_stop}_gathered.h5"

    def generate_process_path(self, base_dir):
        return base_dir, "col{col_start}-{col_stop}_processed.h5"

    def run_gather(self):
        if self.measurement == "adccal":
            from gather.gather_adccal import Gather
        elif self.measurement == "ptccal":
            from gather.gather_base import GatherBase as Gather
        else:
            print("Unsupported type.")

        # define input files
        in_dir, in_file_name = self.generate_raw_path(self.in_base_dir)
        in_fname = os.path.join(in_dir, in_file_name)

        # define metadata file
        meta_dir, meta_file_name = (
            self.generate_metadata_path(self.in_base_dir)
        )
        meta_fname = os.path.join(meta_dir, meta_file_name)

        # define output files
        out_dir, out_file_name = self.generate_gather_path(self.out_base_dir)
        out_fname = os.path.join(out_dir, out_file_name)

        for p in range(self._n_parts):
            col_start = p * self._n_cols
            col_stop = (p+1) * self._n_cols

            out_f = out_fname.format(col_start=col_start, col_stop=col_stop)

#            if os.path.exists(out_f):
#                print("output filename = {}".format(out_f))
#                print("WARNING: output file already exist. Skipping gather.")
#            else:
            utils.create_dir(out_dir)

            obj = Gather(in_fname=in_fname,
                         out_fname=out_f,
                         meta_fname=meta_fname,
                         n_rows=self._n_rows,
                         n_cols=self._n_cols,
                         part=p)
            obj.run()

    def run_process(self):
        self.process_m = __import__(self.method).Process

        # define input files
        # the input files for process is the output from gather
        in_dir, in_file_name = self.generate_gather_path(self.in_base_dir)
        in_fname = os.path.join(in_dir, in_file_name)

        # define output files
        out_dir, out_file_name = self.generate_process_path(self.out_base_dir)
        out_fname = os.path.join(out_dir, out_file_name)

        for p in range(1):
            col_start = p * self._n_cols
            col_stop = (p+1) * self._n_cols

            in_f = in_fname.format(col_start=col_start,
                                   col_stop=col_stop)
            out_f = out_fname.format(col_start=col_start,
                                     col_stop=col_stop)

#            if os.path.exists(out_f):
#                print("output filename = {}".format(out_f))
#                print("WARNING: output file already exist. Skipping process.")
#            else:
            utils.create_dir(out_dir)

            # generate out_put
            obj = self.process_m(in_fname=in_f,
                                 out_fname=out_f)

            obj.run()

    def cleanup(self):
        # remove gather dir
        pass


def get_arguments():
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
                        help="The name of the config file.")

    args = parser.parse_args()

    required_arguments_set = (
        args.input
        and args.output
        and args.run_id
        and args.method
        and args.run_type
    )

    if args.config_file is not None:
        args.config_file = os.path.join(CONFIG_DIR, args.config_file)
        if not os.path.exists(args.config_file):
            msg = ("Configuration file {} does not exist."
                   .format(args.config_file))
            parser.error(msg)

    elif not required_arguments_set:
        msg = ("Either specify a config_file or the command line parameters:"
               "-i/--input, -o/--output, -r/--run, -m/--method, -t/--type")
        parser.error(msg)

    return args


def insert_args_into_config(args, config):

    # general

    if "general" not in config:
        config["general"] = dict()

    c_general = config["general"]

    try:
        c_general["run_type"] = args.run_type or c_general["run_type"]
    except:
        raise Exception("No run_type specified. Abort.")
        sys.exit(1)

    try:
        c_general["run"] = args.run_id or c_general["run"]
    except:
        raise Exception("No run_id specified. Abort.")
        sys.exit(1)

    try:
        c_general["n_cols"] = args.n_cols or c_general["n_cols"]
    except:
        raise Exception("No n_cols type specified. Abort.")
        sys.exit(1)

    # run type specific

    run_type = c_general["run_type"]

    if "all" not in config:
        config["all"] = {}

    c_run_type = config[run_type]
    c_all = config["all"]

    try:
        # "all" takes higher priority than the run type specific config
        if "input" in c_all:
            c_run_type["input"] = args.input or c_all["input"]
        else:
            c_run_type["input"] = args.input or c_run_type["input"]
    except KeyError:
        raise Exception("No input specified. Abort.")
        sys.exit(1)

    try:
        # "all" takes higher priority than the run type specific config
        if "output" in c_all:
            c_run_type["output"] = args.output or c_all["output"]
        else:
            c_run_type["output"] = args.output or c_run_type["output"]
    except KeyError:
        raise Exception("No output specified. Abort.")
        sys.exit(1)

    try:
        c_run_type["method"] = args.method or c_run_type["method"]
    except:
        raise Exception("No method type specified. Abort.")
        sys.exit(1)


if __name__ == "__main__":
    args = get_arguments()

    if args.config_file is None:
        config = dict()
    else:
        config = utils.load_config(args.config_file)

    insert_args_into_config(args, config)

    # fix format of command line parameter
    if config["general"]["n_cols"] == "None":
        config["general"]["n_cols"] = None
    else:
        config["general"]["n_cols"] = int(config["general"]["n_cols"])

    for key, value in config.items():
        print(key, value)

    run_type = config["general"]["run_type"]
    run_id = config["general"]["run"]
    measurement = config["general"]["measurement"]
    n_cols = config["general"]["n_cols"]

    out_base_dir = config[run_type]["output"]
    in_base_dir = config[run_type]["input"]
    method = config[run_type]["method"]

    # generate file paths
    if run_type == "gather":
        in_base_dir = in_base_dir
        out_base_dir = os.path.join(out_base_dir,
                                    "{}_gathered".format(run_id))
    else:
        in_base_dir = os.path.join(in_base_dir,
                                   "{}_gathered".format(run_id))
        out_base_dir = os.path.join(out_base_dir,
                                    "{}_processed".format(run_id))

    obj = Analyse(in_base_dir=in_base_dir,
                  out_base_dir=out_base_dir,
                  run_id=run_id,
                  run_type=run_type,
                  measurement=measurement,
                  n_cols=n_cols,
                  method=method)
    obj.run()
