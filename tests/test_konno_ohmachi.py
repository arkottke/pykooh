import numpy as np

import cyko

from . import DATA_PATH

# Load test data
data = np.load(str(DATA_PATH / 'test_data.npz'))
freqs = data['freqs']
raw_amps = data['fourier_amps']
smooth_amps = data['ko_amps']
b = data['b']


def test_smooth():
    calculated = cyko.smooth(freqs, freqs, raw_amps, b)
    np.testing.assert_allclose(calculated, smooth_amps, rtol=1E-3)
