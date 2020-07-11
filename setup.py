from setuptools import setup, find_packages, Extension

import numpy as np


with open('README.rst') as fp:
    readme = fp.read()

with open('HISTORY.rst') as fp:
    history = fp.read()

try:
    import cython
    ext_modules = [
        Extension(
            'pykooh.smooth_cython',
            ['pykooh/smooth_cython.pyx', 'pykooh/smoothing.c'],
            libraries=['m'],
            include_dirs=[np.get_include()],
            extra_compile_args=['-Ofast']),
    ]
except ImportError:
    ext_modules = []


setup(
    name='pykooh',
    version='0.3.1',
    description='Efficient implementatins of the Konno Ohmachi filter in Python',
    long_description=readme + '\n\n' + history,
    author='Albert Kottke',
    author_email='albert.kottke@gmail.com',
    url='https://github.com/arkottke/pykooh',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        'setuptools>=18.0',
        'numba',
        'numpy'
    ],
    extra_require={
        'cython': 'cython',
    },
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    ext_modules=ext_modules,
    zip_safe=False,
)
