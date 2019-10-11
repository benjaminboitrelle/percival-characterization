#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime
import copy
import json
import multiprocessing
import os
import sys
import time
import math

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


if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
sys.path.append(SRC_DIR)
from analyse import Analyse

if SHARED_DIR not in sys.path:
    sys.path.insert(0, SHARED_DIR)


class StartAnalyse(object):
    def __init__(self):
        print(CURRENT_DIR)

        self.in_base_dir = "/Volumes/LACIE_SHARE/Percival/Data_lab_october18/Coarse_scan"
        self.out_base_dir = "/Volumes/LACIE_SHARE/Percival/Data_lab_october18/Coarse_scan"

        self.create_outdir = None
        self.n_rows_total = 1484
        self.n_cols_total = 1440
        self.n_cols = 32

        self.n_rows = self.n_rows_total

        self.n_parts = self.n_cols_total // self.n_cols
        self.n_processes = 45

        self.run_id = "DLSraw"
        self.run_type = "gather"

        self.measurement = "adccal"
        self.method = "file_per_vin_and_register_file"
        self.method_properties = None

        self._set_job_sets()
        self.run()

    def _set_job_sets(self):
        all_jobs = range(self.n_parts)
        self.n_job_sets = math.ceil(self.n_parts / float(self.n_processes))

        self.job_sets = []
        for i in range(self.n_job_sets):
            start = i*self.n_processes
            stop = (i+1)*self.n_processes
            self.job_sets.append(all_jobs[start:stop])

    def run(self):
        """ Drive the muliprocessing of the analaysis.
        """


        jobs = []
        for job_set in self.job_sets:
            jobs = []
            for p in job_set:
                print(p)

                print(args)
                proc = multiprocessing.Process(target=Analyse,
                                               args=(self.in_base_dir,
                                                     self.out_base_dir,
                                                     self.create_outdir,
                                                     self.run_id,
                                                     self.run_type,
                                                     self.measurement,
                                                     self.n_cols,
                                                     self.method,
                                                     self.method_properties,
                                                     self.n_processes,
                                                     p,))
                jobs.append(proc)
                proc.start()

            for job in jobs:
                job.join()


if __name__ == "__main__":
    StartAnalyse()
