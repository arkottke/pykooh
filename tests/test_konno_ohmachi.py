import numpy as np
import pytest

import pykooh

from . import DATA_PATH

try:
    import Cython  # noqa: F401

    has_cython = True
except ImportError:
    has_cython = False

use_cython = (
    [True, False]
    if has_cython
    else [
        False,
    ]
)

# Load test data
data = np.load(str(DATA_PATH / "test_data.npz"))
freqs = data["freqs"]
raw_amps = data["fourier_amps"]
smooth_amps = data["ko_amps"]
b = data["b"]


@pytest.mark.parametrize("use_cython", use_cython)
def test_smooth(use_cython):
    calculated = pykooh.smooth(freqs, freqs, raw_amps, b, use_cython=use_cython)
    np.testing.assert_allclose(calculated, smooth_amps, rtol=1e-3)
