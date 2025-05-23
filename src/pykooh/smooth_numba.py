"""Numba implementation."""

import numba
import numpy as np


@numba.jit()
def smooth(ko_freqs, freqs, spectrum, bw, normalize=True, simplified=True):
    # Minimum step
    eps = np.finfo(freqs.dtype).eps

    # Frequency range of significance
    max_ratio = pow(10, 3 / bw)
    min_ratio = 1 / max_ratio

    ko_smooth = np.empty_like(ko_freqs)

    for i, fc in enumerate(ko_freqs):
        if fc < eps:
            # Near zero use 1
            ko_smooth[i] = spectrum[0]
            continue

        total = 0
        window_total = 0
        for j, freq in enumerate(freqs):
            frat = freq / fc
            if simplified and (frat < min_ratio or max_ratio < frat):
                continue

            if freq < eps:
                # Skip values outside the range
                continue
            elif np.abs(freq - fc) < eps:
                # Avoid division by zero
                window = 1.0
            else:
                x = bw * np.log10(frat)
                window = (np.sin(x) / x) ** 4

            total += window * spectrum[j]
            window_total += window

            if simplified and max_ratio < frat:
                break
        # Only save the results in the window picked up meaningful amount of
        # values. If this isn't done, then the normalization increases the
        # values with low window_total.
        if window_total > 0.3:
            if normalize:
                ko_smooth[i] = total / window_total
            else:
                ko_smooth[i] = total
        else:
            # Fill missing entries with nan
            ko_smooth[i] = np.nan

    return ko_smooth
