import numpy as np
import matplotlib.pyplot as plt

from astropy import units
from astropy.io import fits


class AbstractUVcoordinates(np.ndarray):

    def __new__(cls, array, *args, **kwargs):

        obj = array.view(cls)
        return obj

    @property
    def u(self):
        return self[..., 0]

    @property
    def v(self):
        return self[..., 1]

    @property
    def uv_distance(self):
        return np.hypot(
            self.u,
            self.v
        )



class UVcoordinates(AbstractUVcoordinates):

    def __init__(self, array):

        # if len(array.shape) == 2:
        #     if array.shape[-1] == 2:
        #         self.array = array
        #     else:
        #         raise ValueError("...")
        # else:
        #     raise ValueError("...")

        self.array = array

    @classmethod
    def manual_1d(cls, array):

        if type(array) is list:
            array = np.asarray(array)

        return UVcoordinates(array=array)

    @classmethod
    def from_fits(cls, filename):

        array = fits.getdata(filename=filename)

        return cls.manual_1d(array=array)


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        "{}/utils".format(os.environ["GitHub"])
    )
    import random_utils as random_utils

    directory = '/Users/ccbh87/Desktop/ALMA_data/2015.1.01362.S/science_goal.uid___A001_X2d6_X224/group.uid___A001_X2d6_X225/member.uid___A001_X2d6_X226/calibrated/CASA_4.7.0/width_1'

    spws = ["0", "1", "2", "3"]


    frequencies = {}
    for spw in spws:
        frequencies[spw] = fits.getdata(
            filename="{}/frequencies_spw_{}.fits".format(
                directory,
                spw
            )
        )

        plt.plot()


    colors = random_utils.generate_list_of_random_colors(length_of_list=len(spws))
    for i, spw in enumerate(spws):
        frequencies_spw = frequencies[spw]
        print(
            "In spw={} there are n={} channel, where the min/max frequencies are {}/{} (GHz), resulting in a bandwifth of {}".format(
                spw,
                len(frequencies_spw),
                np.min(frequencies_spw) * units.Hz.to(units.GHz),
                np.max(frequencies_spw) * units.Hz.to(units.GHz),
                (np.max(frequencies_spw) - np.min(frequencies_spw)) * units.Hz.to(units.GHz),
            )
        )
        for j, frequency in enumerate(frequencies_spw):
            plt.axvline(frequency, color=colors[i], linewidth=2, label=spw if j==0 else None, alpha=0.75)
    plt.legend()
    plt.show()
