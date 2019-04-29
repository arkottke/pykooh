"""cyko - Cython implementation of the Konno Ohmachi."""

from pkg_resources import get_distribution

__author__ = 'Albert Kottke'
__copyright__ = 'Copyright 2019 Albert Kottke'
__license__ = 'MIT'
__title__ = 'cyko'
__version__ = get_distribution('cyko').version
del get_distribution

from .konno_ohmachi import smooth


