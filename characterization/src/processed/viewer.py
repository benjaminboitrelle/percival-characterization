from viewer_base import ViewerBase
import matplotlib
# Generate images without having a window appear:
# this prevents sending remote data to locale PC for rendering
matplotlib.use('Agg')  # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt  # noqa E402

import __init__  # noqa E402


class Viewer(ViewerBase):
    def __init__(self, **kwargs):  # noqa F401
        super().__init__(**kwargs)

    def _generate_single_plot(self,
                              x,
                              plot_title,
                              label,
                              out_fname):

        fig, axs = plt.subplots(nrows=1, sharex=True)

#        Reorder the input data to plot it in a 2D histogram
        x = x.transpose(0, 2, 1)
        x = x.reshape(7*212, 1440)
        plt.imshow(x)
        plt.colorbar()

#       Inversion of axis for corresponding to the output of the sensor
        axs.invert_xaxis()
        axs.invert_yaxis()
        plt.xlabel("Columns")
        plt.ylabel("Rows")

        fig.suptitle(plot_title)
        fig.savefig(out_fname)

        fig.clf()
        plt.close(fig)
