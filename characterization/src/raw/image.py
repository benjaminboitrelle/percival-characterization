import copy
import matplotlib
# Generate images without having a window appear:
# this prevents sending remote data to locale PC for rendering
matplotlib.use('TkAgg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt  # noqa E402

from plot_base import PlotBase  # noqa E402


class Plot(PlotBase):
    def __init__(self, **kwargs):  # noqa F401
        # overwrite the configured col and row indices
        new_kwargs = copy.deepcopy(kwargs)
        new_kwargs["col"] = None
        new_kwargs["row"] = None
        new_kwargs["dims_overwritten"] = True

        super().__init__(**new_kwargs)

    def _check_dimension(self, data):
        if data.shape[0] != 1:
            raise("Plot method one image can only show one image at the time.")

    def _generate_single_plot(self, data, plot_title, label, out_fname):

        fig, axs = plt.subplots(nrows=1, sharex=True)

        plt.imshow(data)
        cbar = plt.colorbar()
        cbar.ax.set_ylabel("ADU", rotation=270, labelpad=15)
        axs.invert_xaxis()

        plt.xlabel("Columns")
        plt.ylabel("Rows")

        fig.suptitle(plot_title)
        fig.savefig(out_fname)

        if self._interactive:
            plt.show()

        fig.clf()
        plt.close(fig)
