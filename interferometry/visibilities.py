import numpy as np

from astropy.io import fits


def convert(array):

    if array.shape[-1] == 2:
        array_complex = np.empty(
            shape=array.shape[:-1],
            dtype=np.complex128
        )
        array_complex.real = array[..., 0]
        array_complex.imag = array[..., 1]
    else:
        raise ValueError(
            "The input array shape {} is not supported. Must be (N1 x N2 x ... x 2)".format(array.shape)
        )

    return array_complex


class AbstractVisibilities(np.ndarray):

    def __new__(cls, array, n_antennas=None, *args, **kwargs):

        if array.shape[-1] == 2:
            obj = array.view(cls)

            obj.complex = convert(
                array=array
            )

        else:
            raise ValueError(
                "This is not implemented yet."
            )

        obj.shape = array.shape

        # if len(obj.shape) == 3:
        #     obj.averaged = np.averaged(a=array, axis=0)

        obj.n_antennas = n_antennas
        if n_antennas is not None:
            obj.n_baselines = int(n_antennas * (n_antennas - 1) / 2)
        else:
            obj.n_baselines = None

        # ...
        if obj.n_baselines is not None:
            obj.reshaped = array.reshape(
                (int(array.shape[0] / n_baselines), n_baselines, ) + array.shape[1:]
            )
        else:
            obj.reshaped = None

        return obj

    @property
    def as_complex(self):
        return self.complex

    @property
    def real(self):
        return self[..., 0]

    @property
    def imag(self):
        return self[..., 1]

    @property
    def phases(self):
        return np.arctan2(
            self.imag,
            self.real
        )

    @property
    def amplitudes(self):
        return np.hypot(
            self.real,
            self.imag
        )

    # @property
    # def averaged(self):
    #     print(self.shape)


class Visibilities(AbstractVisibilities):

    def __init__(self, array):

        # if array.shape[-1] == 2:
        #     if len(array.shape) == 2:
        #         self.array = array
        #     if len(array.shape) == 3:
        #         raise ValueError("Not implemented")
        #     if len(array.shape) == 4:
        #         raise ValueError("Not implemented")
        #     else:
        #         raise ValueError("invalid")
        # else:
        #     raise ValueError("...")

        self.array = array

    @classmethod
    def manual(cls, array):

        if type(array) is list:
            array = np.asarray(array)

        return Visibilities(array=array)

    @classmethod
    def from_fits(cls, filename):

        array = fits.getdata(filename=filename)

        return cls.manual(array=array)


if __name__ == "__main__":

    directory = '/Users/ccbh87/Desktop/ALMA_data/2015.1.01362.S/science_goal.uid___A001_X2d6_X224/group.uid___A001_X2d6_X225/member.uid___A001_X2d6_X226/calibrated/CASA_4.7.0/width_1'

    spw = "0"

    visibilities = Visibilities.from_fits(
        filename="{}/visibilities_spw_{}.fits".format(
            directory,
            spw
        )
    )
    #print(visibilities.real.shape)

    print(visibilities.as_complex)
