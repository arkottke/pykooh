# cyko

[![PyPi Cheese Shop](https://img.shields.io/pypi/v/cyko.svg)](https://img.shields.io/pypi/v/cyko.svg)
[![Build Status](https://travis-ci.org/arkottke/cyko.svg?branch=master)](https://travis-ci.org/arkottke/cyko)
[![Test Coverage](https://coveralls.io/repos/github/arkottke/cyko/badge.svg?branch=master)](https://coveralls.io/github/arkottke/cyko?branch=master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![DOI Information](https://zenodo.org/badge/21452/arkottke/cyko.svg)](https://zenodo.org/badge/latestdoi/21452/arkottke/cyko)

Konno Omachi filter implemented in Cython.

This code implements Konno-Ohmachi spectral smoothing as defined in: 
> Konno, K. and Ohmachi, T., 1998. Ground-motion characteristics estimated from spectral ratio between horizontal and 
vertical components of microtremor. Bulletin of the Seismological Society of America, 88(1), pp.228-241.

This code was originally written for smoothing sub-module in 
[gmprocess](https://github.com/usgs/groundmotion-processing/tree/master/gmprocess/smoothing) by Bruce Worden. Dave Boore 
has provided 
[notes](http://daveboore.com/daves_notes/notes%20on%20smoothing%20over%20logarithmically%20spaced%20freqs.pdf) 
on this topic, which also may be of interest. 

# Installation

`cyko` is available via `pip` and can be installed with:
```
pip install cyko
```
Note that `cython` and C compiler are required.

# Usage

Smooth a signal using a bandwith of 30.

```Python
import cyko
signal_smooth = cyko.smooth(freqs, freqs_raw, signal_raw, 30)
```

# Citation

Please cite this software using the following DOI:  