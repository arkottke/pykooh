"""pykooh - Efficient implementatins of the Konno Omachi filter in Python."""

from importlib.metadata import version

import numpy as np
import numpy.typing as npt

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


def smooth(
    ko_freqs, freqs, spectrum, bw, use_cython=None, normalize=True, simplified=False
):
    """Smooth a spectrum.
    This function smooths an input spectrum based on specified frequencies,
    employing either a Cython or Numba backend for computation. It operates
    on the absolute value of the input spectrum.
    Parameters
    ----------
    ko_freqs : numpy.ndarray
        Array of frequencies at which the smoothed spectrum is to be evaluated.
    freqs : numpy.ndarray
        Array of frequencies corresponding to the input `spectrum`.
    spectrum : numpy.ndarray
        The input spectrum to be smoothed. The function will use the
        absolute value of this spectrum.
    bw : float
        Smoothing bandwidth parameter.
    use_cython : bool, optional
        If True and the Cython implementation (`smooth_cython`) is available
        (indicated by a global `has_cython` flag), the Cython version is used.
        Otherwise, the Numba implementation (`smooth_numba`) is used.
        Defaults to True.
    normalize : bool, optional
        The Konno-Ohmachi smoothing window is normalized on a logarithmic
        scale. Set this parameter to True to normalize it on a normal scale.
        Default to False.
    Returns
    -------
    numpy.ndarray
        The smoothed spectrum, evaluated at `ko_freqs`.
    Notes
    -----
    - The input `spectrum` is converted to its absolute values
      (i.e., `numpy.abs(spectrum)`) before any smoothing is applied.
    - The selection of the Cython backend is contingent upon the `use_cython`
      parameter and the availability of the Cython compiled module (checked via
      an external `has_cython` variable).
    """

    # Only work on the absolute value
    spectrum = np.abs(spectrum)

    if use_cython:
        if has_cython:
            smoothed = smooth_cython.smooth(ko_freqs, freqs, spectrum, bw, normalize)
        else:
            raise ImportError(
                "Cython implementation not available. "
                "Please install the Cython module or set use_cython=False."
            )
    else:
        smoothed = smooth_numba.smooth(
            ko_freqs, freqs, spectrum, bw, normalize, simplified
        )

    return smoothed


class CachedSmoother:
    """
    Pre-compute the weights of the Konno-Ohmachi window for repeated application.


    Adapted from obspy: https://docs.obspy.org/_modules/obspy/signal/konnoohmachismoothing.html#calculate_smoothing_matrix

    """

    def __init__(
        self,
        freqs_in: npt.ArrayLike,
        freqs_out: npt.ArrayLike,
        bandwidth: float = 40.0,
        normalize: bool = True,
    ):
        self._freqs_in = np.asarray(freqs_in)
        self._freqs_out = np.asarray(freqs_out)

        self._weights = np.empty((len(freqs_in), len(freqs_out)), freqs_in.dtype)
        for i, freq_cent in enumerate(freqs_out):
            self._weights[:, i] = self.window(freqs_in, freq_cent, bandwidth, normalize)

    def freqs_match(self, freqs):
        return len(freqs) == len(self._freqs_in) and np.allclose(freqs, self._freqs_in)

    def __call__(self, signal: npt.ArrayLike, count=1) -> np.ndarray:
        if len(signal) != len(self._freqs_in):
            raise ValueError

        smoothed = np.dot(signal, self._weights)

        for _ in range(count - 1):
            smoothed = np.dot(signal, self._weights)

        return smoothed

    @staticmethod
    def window(
        freqs: npt.ArrayLike,
        freq_cent: float,
        bandwidth: float = 40,
        normalize: bool = False,
    ) -> np.ndarray:
        """Returns the Konno & Ohmachi Smoothing window for every frequency in
        frequencies.

        Returns the smoothing window around the center frequency with one value per
        input frequency defined as follows (see [Konno1998]_)::

            [sin(b * log_10(f/f_c)) / (b * log_10(f/f_c)]^4
                b   = bandwidth
                f   = frequency
                f_c = center frequency

        The bandwidth of the smoothing function is constant on a logarithmic scale.
        A small value will lead to a strong smoothing, while a large value of will
        lead to a low smoothing of the Fourier spectra.
        The default (and generally used) value for the bandwidth is 40. (From the
        `Geopsy documentation <http://www.geopsy.org>`_)

        All parameters need to be positive. This is not checked due to performance
        reasons and therefore any negative parameters might have unexpected
        results.

        Parameters
        ----------
        freqs : npt.ArrayLike
            all frequencies for which the smoothing window will be returned.
        freq_cent : float
            frequency around which the smoothing is performed. Must be greater
            or equal to 0.
        bandwidth : float
            Determines the width of the smoothing peak. Lower values result in a
            broader peak. Must be greater than 0. Defaults to 40.
        normalize : bool
            The Konno-Ohmachi smoothing window is normalized on a logarithmic
            scale. Set this parameter to True to normalize it on a normal scale.
            Default to False.

        Returns
        -------
        np.ndarray
           Calculated weights
        """
        freqs = np.asarray(freqs)

        # If the center_frequency is 0 return an array with zero everywhere except
        # at zero.
        if freq_cent == 0:
            window = np.zeros(len(freqs), dtype=freqs.dtype)
            window[freqs == 0.0] = 1.0
            return window

        # Disable div by zero errors and return zero instead
        with np.errstate(divide="ignore", invalid="ignore"):
            # Calculate the bandwidth*log10(f/f_c)
            window = bandwidth * np.log10(freqs / freq_cent)
            # Just the Konno-Ohmachi formulae.
            window[:] = (np.sin(window) / window) ** 4
        # Check if the center frequency is exactly part of the provided
        # frequencies. This will result in a division by 0. The limit of f->f_c is
        # one.
        window[freqs == freq_cent] = 1.0
        # Also a frequency of zero will result in a logarithm of -inf. The limit of
        # f->0 with f_c!=0 is zero.
        window[freqs == 0.0] = 0.0
        # Normalize to one if wished.
        if normalize:
            window /= window.sum()

        return window


def effective_ampl(
    freqs,
    fourier_amps_h1,
    fourier_amps_h2,
    freqs_ea=None,
    missing="nan",
    bw=188.5,
    simplified=False,
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
            'nan' - use `np.nan` for missing values
            'trim' - only provide EAS over the range of continuous values
    bw: float (optional)
        Bandwidth of the smoothing function. Default is 188.5 as defined in
        Kottke et al. (2018)
    simplified: bool (optional)
        Use the simplified version of the smoothing function. This is
        significantly faster but less accurate. Default is False.
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

    smoothed = smooth(freqs_ea, freqs, avg, bw, simplified=simplified, normalize=True)

    if missing == "nan":
        # Default behavior
        pass
    elif missing == "trim":
        mask = np.isfinite(smoothed)
        freqs_ea = freqs_ea[mask]
        smoothed = smoothed[mask]
    else:
        raise NotImplementedError

    return freqs_ea, smoothed
