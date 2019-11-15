# -*- coding: utf-8 -*-
"""Method for non-linear fitting of fine part of ADCs."""
from itertools import product
import numpy as np
import operator
import __init__  # noqa F401
from process_adccal_base import ProcessAdccalBase


class Process(ProcessAdccalBase):

    def _initiate(self):
        shapes = {
            "offset": (self._n_adcs, self._n_cols, self._n_groups),
            "vin_size": (self._n_frames * self._n_groups)
        }

        self._result = {
            "s_offset": {
                "data": np.NaN * np.zeros(shapes["offset"], dtype=np.float64),
                "path": "sample/fine/offset"
            },
            "s_slope": {
                "data": np.NaN * np.zeros(shapes["offset"], dtype=np.float64),
                "path": "sample/fine/slope"
            },
            "s_poly_2": {
                "data": np.NaN * np.zeros(shapes["offset"], dtype=np.float64),
                "path": "sample/fine/poly_2"
            },
            "r_parameters": {
                "data": np.NaN * np.zeros(shapes["offset"]),
                "path": "reset/fine/parameters"
            },
            "s_roi": {
                "data": np.NaN * np.zeros(shapes["offset"]),
                "path": "sample/fine/roi"
            },
            "r_roi": {
                "data": np.NaN * np.zeros(shapes["offset"]),
                "path": "reset/fine/roi"
            }
        }

    def _calculate(self):
        """ Perform non-linear fitting on ADC fine part.
            Parameters of polynomials used are stored in a HDF5 file.
        """

        print("Start loading data from {} ...".format(self._in_fname), end="")
        data = self._load_data(self._in_fname)
        print("Data loaded...")
        # convert (n_adcs, n_cols, n_groups, n_frames)
        #      -> (n_adcs, n_cols, n_groups * n_frames)
        sample_coarse = data["s_coarse"]
#        reset_coarse = data["r_coarse"]
        sample_fine = data["s_fine"]
#        reset_fine = data["r_fine"]
        vin = self._fill_vin_total_frames(data["vin"])
        s_offset = self._result["s_offset"]["data"]
        s_slope = self._result["s_slope"]["data"]
        s_poly2 = self._result["s_poly_2"]["data"]

#        r_parameters = self._result["r_parameters"]["data"]
        s_roi_map = self._result["s_roi"]["data"]
#        r_roi_map = self._result["r_roi"]["data"]

        for adc, col, row in product(range(self._n_adcs),
                                     range(self._n_cols),
                                     range(self._n_groups)):
            adu = sample_fine[adc, col, :, row]
            crs = sample_coarse[adc, col, :, row]
            unique, counts = np.unique(crs, return_counts=True)
            length_values = dict(zip(unique, counts))
            better_coarse = max(length_values.items(),
                                key=operator.itemgetter(1))[0]

            roi = np.where(crs == better_coarse)
            s_roi_map[adc, col, row] = better_coarse
            if np.any(roi):
                fit_coeffs = np.polyfit(vin[roi], adu[roi], 1)
                s_offset[adc, col, row] = tuple(fit_coeffs)
                # s_slope[adc, col, row] = fit_coeffs[1]
                # s_poly2[adc, col, row] = fit_coeffs[2]
                # s_parameters[adc, col, row] = fit_coeffs
        # self._result["s_parameters"]["data"] = s_parameters
