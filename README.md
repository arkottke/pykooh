# pykooh

[![PyPi Cheese
Shop](https://img.shields.io/pypi/v/pykooh.svg)](https://img.shields.io/pypi/v/pykooh.svg)
[![Build
Status](https://github.com/arkottke/pykooh/actions/workflows/python-app.yml/badge.svg)](https://github.com/arkottke/pykooh/actions/workflows/python-app.yml)
[![Code
Quality](https://app.codacy.com/project/badge/Grade/c8a3110f14e444a598713b002c20f979)](https://www.codacy.com/manual/arkottke/pykooh)
[![Test
Coverage](https://api.codacy.com/project/badge/Coverage/c8a3110f14e444a598713b002c20f979)](https://www.codacy.com/manual/arkottke/pykooh)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
[![DOI](https://zenodo.org/badge/183696586.svg)](https://zenodo.org/badge/latestdoi/183696586)

Konno Ohmachi filter implemented in Numba.

This code implements Konno-Ohmachi spectral smoothing as defined in:

    Konno, K. and Ohmachi, T., 1998. Ground-motion characteristics estimated
    from spectral ratio between horizontal and vertical components of
    microtremor. Bulletin of the Seismological Society of America, 88(1),
    pp.228-241.

This code was originally written for smoothing sub-module in
[gmprocess](https://github.com/usgs/groundmotion-processing/tree/master/gmprocess/smoothing)
by Bruce Worden. Dave Boore has provided
[notes](http://daveboore.com/daves_notes/notes%20on%20smoothing%20over%20logarithmically%20spaced%20freqs.pd)
on this topic, which also may be of interest. Notes regarding the
characteristics of the Konno-Ohmachi filter and the implementation are
provided in the [implementation](implemenation.ipynb) Jupyter Notebook.

# Installation

`pykooh` is available via `pip` and can be installed with:

    pip install pykooh

By default, `pykooh` uses `numba` for the fast implementation of the
filter. Performance can be increased by using `cython`, but this
requires a C complier. If a C compiler is available, install `cython`
required dependencies with:

    pip install pykooh[cython]

# Usage

Smooth a signal using a bandwith of 30.

```python
import pykooh
signal_smooth = pykooh.smooth(freqs, freqs_raw, signal_raw, 30)
```

Additional examples and comparison with `obspy` are provided in
[example](example.ipynb).

# Citation

Please cite this software using the following
[DOI](https://zenodo.org/badge/latestdoi/183696586).
