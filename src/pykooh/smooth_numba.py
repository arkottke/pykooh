"""Numba implementation."""

import numba
import numpy as np


@numba.jit()
def smooth(ko_freqs, freqs, spectrum, b):
    # Minimum step
    eps = np.finfo(freqs.dtype).eps

    # Frequency range of significance
    max_ratio = pow(10, 3 / b)
    min_ratio = 1 / max_ratio

    ko_smooth = np.empty_like(ko_freqs)

    for i, fc in enumerate(ko_freqs):
        # Check if we need a frequency near zero
        if fc < eps:
            if freqs[i] < eps:
                ko_smooth[i] = spectrum[0]
            else:
                raise ValueError
            continue

        total = 0
        window_total = 0
        for j, freq in enumerate(freqs):
            frat = freq / fc

            if freq < eps or frat < min_ratio or max_ratio < frat:
                # Skip values outside the range
                continue
            elif np.abs(freq - fc) < eps:
                window = 1.0
            else:
                x = b * np.log10(frat)
                window = (np.sin(x) / x) ** 4

            total += window * spectrum[j]
            window_total += window

        if window_total > 0:
            ko_smooth[i] = total / window_total
        else:
            # Fill missing entries with nan
            ko_smooth[i] = np.nan

    return ko_smooth
