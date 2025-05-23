"""Numba implementation."""
# cython: language_level=3

import cython

import numpy as np
cimport numpy as np


cdef extern from "smoothing.h":
    void konno_ohmachi_c(double *spec, double *freqs, int ns,
                         double *ko_freqs, double *ko_smooth, int nks,
                         double b, bool normalize);


@cython.embedsignature(True)
def smooth(
        np.ndarray[double, ndim=1, mode='c']ko_freqs,
        np.ndarray[double, ndim=1, mode='c']freqs,
        np.ndarray[double, ndim=1, mode='c']spec,
        bw,
        normalize

):
    """
    Parameters
    ----------
    ko_freqs: :class:`numpy.ndarray`
        Frequencies at which the smoothed values are provided.
    freqs: :class:`numpy.ndarray`
        Frequencies of the original spectrum
    spec: :class:`numpy.ndarray`
        Original spectrum
    bw: float
        _bw_ parameter of the filter window, controls bandwidth.
    normalize: bool
        The Konno-Ohmachi smoothing window is normalized on a logarithmic
        scale. Set this parameter to True to normalize it on a normal scale.
        Default to False.
    Returns
    -------
    smoothed: :class:`numpy.ndarray`
        Smoothed spectrum.
    """
    cdef int ns = spec.shape[0]
    cdef int nks = ko_freqs.shape[0]
    cdef np.ndarray[double, ndim=1, mode='c'] ko_smooth = np.empty(nks, dtype=np.float64)

    konno_ohmachi_c(
        <double *>spec.data, <double *>freqs.data, ns,
        <double *>ko_freqs.data, <double *>ko_smooth.data, nks,
        bw
    )

    return ko_smooth
