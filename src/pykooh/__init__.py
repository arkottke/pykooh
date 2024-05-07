"""pykooh - Efficient implementatins of the Konno Omachi filter in Python."""

from importlib.metadata import version

import numpy as np

try:
    from . import smooth_cython

    has_cython = True
except ImportError:
    has_cython = False
    smooth_cython = None

from . import smooth_numba

__author__ = "Albert Kottke"
__copyright__ = "Copyright 2019-2024 Albert Kottke"
__license__ = "MIT"
__title__ = "pyKOOH"
__version__ = version("pyKOOH")


def smooth(ko_freqs, freqs, spectrum, b, use_cython=True):
    # Only work on the absolute value
    spectrum = np.abs(spectrum)

    if has_cython and use_cython:
        smoothed = smooth_cython.smooth(ko_freqs, freqs, spectrum, b)
    else:
        smoothed = smooth_numba.smooth(ko_freqs, freqs, spectrum, b)

    return smoothed


def effective_ampl(
    freqs, fourier_amps_h1, fourier_amps_h2, freqs_ea=None, missing="zero"
):
    """
    Compute the effective amplitude spectrum (EAS) as defined in Kottke et al.
    (2018).

    Parameters
    ----------
    freqs: `array_like`
        Frequencies of the Fourier amplitude spectra
    fourier_amps_h1: `array_like`
        Fourier amplitude spectrum of the first horizontal component.
    fourier_amps_h2: `array_like`
        Fourier amplitude spectrum of the second horizontal component.
    freqs_ea: `array_like` (optional)
        Frequencies at which the EAS should be computed. If *None*, the
        frequencies of the EAS will be computed based on the provided frequency
        range. The resulting frequencies are log-space with 100 points per
        decade and start at the start of the decade.
    missing: str (optional)
        Treatment of missing values. Options are:
            'zero' - use 0 for missing values (default)
            'nan' - use `np.nan` for missing values
            'trim' - only provide EAS over the range of continuous values
    Returns
    -------
    freqs_ea: :class:`np.ndarray`
        Frequency of the spectrum
    effect_amp: :class:`np.ndarray`
        Effective amplitude spectrum.

    """

    # Calculate the average power of the two components
    avg = np.abs(
        np.sqrt(0.5 * (np.abs(fourier_amps_h1) ** 2 + np.abs(fourier_amps_h2) ** 2))
    )

    if freqs_ea is None:
        # Frequency range is 100 points per decades
        start = 1 if np.isclose(freqs[0], 0) else 0
        left = np.floor(np.log10(freqs[start])).astype(int)
        right = np.ceil(np.log10(freqs[-1])).astype(int)
        ndecades = right - left
        freqs_ea = np.logspace(left, right, num=(1 + 100 * ndecades))

        # Only compute over the known frequency range. This process is done
        # such that the freqs_ko are exact at the start of the decade (e.g.,
        # 0.1 1, 10, etc.)
        mask = (freqs[start] < freqs_ea) & (freqs_ea < freqs[-1])
        freqs_ea = freqs_ea[mask]

    # Smooth the average spectrum using b of 188.5, which provides a smoothing
    # operator with a bandwidth of 1/30 of a decade
    smoothed = smooth(freqs_ea, freqs, avg, 188.5)

    if missing == "nan":
        smoothed[np.isclose(smoothed, 0)] = np.nan
    elif missing == "trim":
        # First index with continuously defined values
        first = np.where(np.isclose(smoothed, 0))[0][-1] + 1
        freqs_ea = freqs_ea[first:]
        smoothed = smoothed[first:]
    elif missing == "zero":
        # Default behavior
        pass
    else:
        raise NotImplementedError

    return freqs_ea, smoothed
