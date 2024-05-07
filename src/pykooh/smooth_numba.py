"""Numba implementation."""

import numba
import numpy as np


@numba.jit(nopython=True)
def smooth(ko_freqs, freqs, spectrum, b):
    max_ratio = pow(10.0, (3.0 / b))
    min_ratio = 1.0 / max_ratio

    total = 0
    window_total = 0

    ko_smooth = np.empty_like(ko_freqs)
    for i, fc in enumerate(ko_freqs):
        if fc < 1e-6:
            ko_smooth[i] = 0
            continue

        total = 0
        window_total = 0
        for j, freq in enumerate(freqs):
            frat = freq / fc

            if freq < 1e-6 or frat > max_ratio or frat < min_ratio:
                continue
            elif np.abs(freq - fc) < 1e-6:
                window = 1.0
            else:
                x = b * np.log10(frat)
                window = np.sin(x) / x
                window *= window
                window *= window

            total += window * spectrum[j]
            window_total += window

        if window_total > 0:
            ko_smooth[i] = total / window_total
        else:
            ko_smooth[i] = 0

    return ko_smooth
