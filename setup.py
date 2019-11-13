from setuptools import setup, find_packages, Extension

import numpy as np


with open('README.rst') as fp:
    readme = fp.read()

with open('HISTORY.rst') as fp:
    history = fp.read()


setup(
    name='cyko',
    version='0.2.5.2',
    description='Konno Omachi filter implemented in Cython.',
    long_description=readme + '\n\n' + history,
    author='Albert Kottke',
    author_email='albert.kottke@gmail.com',
    url='https://github.com/arkottke/cyko',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        'setuptools>=18.0',
        'cython',
        'numpy'
    ],
    tests_require=[
        'pytest',
        'pytest-runner',
    ],
    ext_modules=[
        Extension(
            'cyko.konno_ohmachi',
            ['cyko/konno_ohmachi.pyx', 'cyko/smoothing.c'],
            libraries=['m'],
            include_dirs=[np.get_include()],
            extra_compile_args=['-Ofast']),
    ],
    zip_safe=False,
)
