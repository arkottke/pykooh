import numpy as np
import pytest

import pyko

from . import DATA_PATH


def read_at2(fname):
    with open(fname) as fp:
        for _ in range(3):
            next(fp)
        time_step = float(next(fp).split()[3])
        accels = np.array([p for l in fp for p in l.split()]).astype(float)
    return time_step, accels


@pytest.fixture()
def fourier_spectra():
    time_step, accels_h1 = read_at2(DATA_PATH / 'RSN4863_CHUETSU_65036EW.AT2')
    accels_h2 = read_at2(DATA_PATH / 'RSN4863_CHUETSU_65036NS.AT2')[1]
    accels = np.c_[accels_h1, accels_h2]

    fourier_amps = np.fft.rfft(accels, axis=0)
    freqs = np.fft.rfftfreq(accels.shape[0], d=time_step)

    return freqs, fourier_amps


@pytest.mark.parametrize('missing', ['zero', 'nan', 'trim'])
def test_effective_ampl(missing, fourier_spectra):
    freqs, fourier_amps = fourier_spectra
    # FIXME Add test
    freqs_ea, eff_ampl = pyko.effective_ampl(
        freqs, fourier_amps[:, 0], fourier_amps[:, 1], missing=missing)
