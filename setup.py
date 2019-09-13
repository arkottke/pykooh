from setuptools import setup, find_packages, Extension

from Cython.Build import cythonize

import numpy as np


with open('README.rst') as fp:
    readme = fp.read()

with open('HISTORY.rst') as fp:
    history = fp.read()


setup(
    name='cyko',
    version='0.2.5a',
    description='Konno Omachi filter implemented in Cython.',
    long_description=readme + '\n\n' + history,
    author='Albert Kottke',
    author_email='albert.kottke@gmail.com',
    url='https://github.com/arkottke/cyko',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'numpy',
    ],
    setup_requires=[
        'cython',
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    ext_modules=cythonize([
        Extension(
            'cyko.konno_ohmachi',
            ['cyko/konno_ohmachi.pyx', 'cyko/smoothing.c'],
            libraries=['m'],
            include_dirs=[np.get_include()],
            extra_compile_args=['-Ofast']),
    ]),
    zip_safe=False,
)
