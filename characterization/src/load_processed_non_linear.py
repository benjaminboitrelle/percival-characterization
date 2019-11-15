import glob
import h5py
import os


class LoadProcessed():
    def __init__(self, input_fname_templ, output_dir, adc, row, col):

        self._input_fname_templ = input_fname_templ
        self._output_dir = os.path.normpath(output_dir)
        self._adc = adc
        self._col = col
        self._row = row

        self._data_type = "processed"

        # self._input_fname = self._get_input_fname(self._input_fname_templ)
        self._input_fname, self._col_offset = self._get_input_fname(
            self._input_fname_templ,
            self._col
        )
        self._paths = {

            "s_fine": {
                "slope": "sample/fine/slope",
                "offset": "sample/fine/offset",
                "poly_2": "sample/fine/poly_2",
                "s_roi": "sample/fine/roi"
            },
            "r_fine": {
                "r_parameters": "reset/fine/parameters",
                "roi": "reset/fine/roi"
            }
        }
        self._metadata_paths = {
            "fn_gathered": "collection/gathered_directory_fine"
        }

    def _get_input_fname(self, input_fname_templ, col):

        input_fname = input_fname_templ.format(data_type=self._data_type,
                                               col_start="*",
                                               col_stop="*")
        print(input_fname_templ)
        files = glob.glob(input_fname)

        # TODO do not use file name but "collections/columns_used" entry in
        # files
        prefix, middle = input_fname_templ.split("{col_start}")
        middle, suffix = middle.split("{col_stop}")

        prefix = prefix.format(data_type=self._data_type)
        middle = middle.format(data_type=self._data_type)
        suffix = suffix.format(data_type=self._data_type)
#        print("prefix", prefix)
#        print("middle", middle)
#        print("suffix", suffix)

        searched_file = None
        for f in files:
            cols = f[len(prefix):-len(suffix)]
            cols = map(int, cols.split(middle))
            # convert str into int
            cols = list(map(int, cols))

            if cols[0] <= col and col <= cols[1]:
                searched_file = f
                col_offset = cols[0]
                break

        if searched_file is None:
            print("input templates:", input_fname_templ)
            print("input_fname", input_fname)
            raise Exception("No files found which contains column {}."
                            .format(col))

        return searched_file, col_offset

    def load_data(self):
        col = self._col - self._col_offset

        data = {}
        with h5py.File(self._input_fname, "r") as f:

            for key in self._paths:
                data[key] = {}
                for subkey, path in self._paths[key].items():
                    data[key][subkey] = f[path][self._adc, col, self._row]

        return data

    def load_metadata(self):
        ''' For a defined input fine, give dictionaries of the region of
            interest used during fitting procedure of coarse and fine.
        '''

        metadata = {}
        with h5py.File(self._input_fname, "r") as f:
            for key in self._metadata_paths:
                metadata[key] = f[self._metadata_paths[key]][()]

        return metadata
