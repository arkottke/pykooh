# Revision History

## v0.4.0

- Change to pyproject-based build

## v0.3.3

- Fix: Force the absolute value on the FAS in the EAS calculation. If
  the complex value is provided, then EAS becomes a \*\* 2 + b
  \*\* 2 + 2i \* (a \* b) instead of the a \*\* 2 + b \*\* 2.

## v0.3.2

- Change setup.py to install numpy prior to import.

## v0.3.1

- Rename to pykooh

## v0.3.0

- Rename to pykoom
- Add support for numba
- Make cython an optonal dependency

## v0.2.5

- Packaging is hard. MANIFEST is fixed now.

## v0.2.4

- Added History to MANIFEST.

## v0.2.3

- Updated badges.
- Added tests for example and implemenation notebooks.

## v0.2.2

- Moved Cython to a setup_requires

## v0.2.1

- Fixed packaging issue

## v0.2

- Added calculation of effective amplitude spectrum

## v0.1.2

- Initial release
