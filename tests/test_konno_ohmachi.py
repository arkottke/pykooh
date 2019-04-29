import pathlib

import numpy as np

import cyko

DATA_PATH = pathlib.Path(__file__).parent / 'data'

# Load test data
data = np.load(str(DATA_PATH / 'test_data.npz'))
freqs = data['freqs']
raw_amps = data['fourier_amps']
smooth_amps = data['ko_amps']
bandwidth = data['bandwidth']


def test_smooth():
    calculated = cyko.smooth(freqs, freqs, raw_amps, bandwidth)
    np.testing.assert_allclose(calculated, smooth_amps, rtol=1E-3)
