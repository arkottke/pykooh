# cyko

[![PyPi Cheese Shop](https://img.shields.io/pypi/v/cyko.svg)](https://img.shields.io/pypi/v/cyko.svg)
[![Build Status](https://travis-ci.org/arkottke/cyko.svg?branch=master)](https://travis-ci.org/arkottke/cyko)
[![Test Coverage](https://coveralls.io/repos/github/arkottke/cyko/badge.svg?branch=master)](https://coveralls.io/github/arkottke/cyko?branch=master)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![DOI Information](https://zenodo.org/badge/21452/arkottke/cyko.svg)](https://zenodo.org/badge/latestdoi/21452/arkottke/cyko)

Konno Omachi filter implemented in Cython.

# Usage

Smooth a signal using a bandwith of 30.

```Python
import cyko
signal_smooth = cyko.smooth(freqs, freqs_raw, signal_raw, 30)
```

# Citation

Please cite this software using the following DOI:  