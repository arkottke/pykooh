import importlib

import numpy as np
import obspy
import pytest
from obspy.signal.konnoohmachismoothing import konno_ohmachi_smoothing

import pykooh

from . import DATA_PATH

use_cython = [
    False,
]
if importlib.util.find_spec("cython"):
    use_cython.append(True)

# Load test data generated from the example.ipynb notebook.
# The reference is computed by Obspy
trace = obspy.read(DATA_PATH / "example_ts.mseed").traces[0]
fa_raw = trace.stats["delta"] * np.abs(np.fft.rfft(trace.data))
freqs = np.fft.rfftfreq(len(trace), d=trace.stats["delta"])

bw = 40
fa_sm_obspy = konno_ohmachi_smoothing(fa_raw, freqs, bw, normalize=True)


@pytest.mark.parametrize("use_cython", use_cython)
def test_smooth(use_cython):
    calc = pykooh.smooth(freqs, freqs, fa_raw, bw, use_cython=use_cython)
    np.testing.assert_allclose(calc, fa_sm_obspy, rtol=1e-3)


def test_smooth_simpl():
    calc = pykooh.smooth(freqs, freqs, fa_raw, bw, use_cython=False, simplified=True)
    mask = np.isfinite(calc)
    np.testing.assert_allclose(calc[mask], fa_sm_obspy[mask], rtol=0.065)


def test_cached_smoother():
    smoother = pykooh.CachedSmoother(freqs, freqs, bw, normalize=True)
    calc = smoother(fa_raw)
    np.testing.assert_allclose(calc, fa_sm_obspy, rtol=1e-3)


@pytest.mark.parametrize("use_cython", use_cython)
@pytest.mark.parametrize(
    "freqs_sm", [np.linspace(0, 50, num=256), np.geomspace(0.1, 50, num=256)]
)
def test_same_smoothing(use_cython, freqs_sm):
    smoother = pykooh.CachedSmoother(freqs, freqs_sm, bw, normalize=True)
    fa_sm_cache = smoother(fa_raw)

    fa_sm_calc = pykooh.smooth(freqs_sm, freqs, fa_raw, bw, use_cython=use_cython)

    # FIXME: Can we use a tigher tolerance
    np.testing.assert_allclose(fa_sm_cache, fa_sm_calc, rtol=0.025)
