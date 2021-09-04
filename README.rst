pykooh
======

|PyPi Cheese Shop| |Build Status| |Code Quality| |Test Coverage| |License| |DOI|

Konno Ohmachi filter implemented in Numba.

This code implements Konno-Ohmachi spectral smoothing as defined in::

    Konno, K. and Ohmachi, T., 1998. Ground-motion characteristics estimated
    from spectral ratio between horizontal and vertical components of
    microtremor. Bulletin of the Seismological Society of America, 88(1),
    pp.228-241.

This code was originally written for smoothing sub-module in gmprocess_
by Bruce Worden. Dave Boore has provided notes_
on this topic, which also may be of interest. Notes regarding the
characteristics of the Konno-Ohmachi filter and the implementation are
provided in the implementation_ Jupyter Notebook.

.. _gmprocess: https://github.com/usgs/groundmotion-processing/tree/master/gmprocess/smoothing
.. _notes: http://daveboore.com/daves_notes/notes%20on%20smoothing%20over%20logarithmically%20spaced%20freqs.pd
.. _implementation: implemenation.ipynb

Installation
============

``pykooh`` is available via ``pip`` and can be installed with:

::

   pip install pykooh

By default, ``pykooh`` uses ``numba`` for the fast implementation of the filter.
Performance can be increased by using ``cython``, but this requires a C
complier. If a C compiler is available, install ``cython`` required
dependencies with:

::

   pip install pykooh[cython]

Usage
=====

Smooth a signal using a bandwith of 30.

.. code:: python

   import pykooh
   signal_smooth = pykooh.smooth(freqs, freqs_raw, signal_raw, 30)

Additional examples and comparison with ``obspy`` are provided in example_.

.. _example: example.ipynb

Citation
========

Please cite this software using the following DOI_.

.. _DOI: https://zenodo.org/badge/latestdoi/183696586

.. |PyPi Cheese Shop| image:: https://img.shields.io/pypi/v/pykooh.svg
   :target: https://img.shields.io/pypi/v/pykooh.svg
.. |Build Status| image:: https://github.com/arkottke/pykooh/actions/workflows/python-app.yml/badge.svg
   :target: https://github.com/arkottke/pykooh/actions/workflows/python-app.yml
.. |Code Quality| image:: https://app.codacy.com/project/badge/Grade/c8a3110f14e444a598713b002c20f979
   :target: https://www.codacy.com/manual/arkottke/pykooh
.. |Test Coverage| image:: https://api.codacy.com/project/badge/Coverage/c8a3110f14e444a598713b002c20f979
   :target: https://www.codacy.com/manual/arkottke/pykooh
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
.. |DOI| image:: https://zenodo.org/badge/183696586.svg
   :target: https://zenodo.org/badge/latestdoi/183696586
