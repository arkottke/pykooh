#!/usr/bin/env python

import importlib

from setuptools import Extension, setup

if importlib.util.find_spec("cython"):
    import numpy as np

    ext_modules = [
        Extension(
            "pykooh.smooth_cython",
            ["pykooh/smooth_cython.pyx", "pykooh/smoothing.c"],
            libraries=["m"],
            include_dirs=[np.get_include()],
            extra_compile_args=["-Ofast"],
        ),
    ]
else:
    ext_modules = []

if __name__ == "__main__":
    setup(
        name="pyKOOH",  # Required
        # A list of compiler Directives is available at
        # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#compiler-directives
        # external to be compiled
        ext_modules=ext_modules,
    )
