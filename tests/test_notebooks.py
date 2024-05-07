# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright (C) Albert Kottke, 2013-2019
import pathlib

import nbformat
import pytest
from jupyter_client.kernelspec import find_kernel_specs
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

cwd = pathlib.Path(__file__).parent

fpaths = [
    cwd / "../example.ipynb",
    cwd / "../implementation.ipynb",
]

fpaths = sorted(fpaths)

kernel_specs = find_kernel_specs()


def idfn(val):
    if isinstance(val, pathlib.Path):
        return val.name


@pytest.mark.parametrize("fpath", fpaths, ids=idfn)
def test_notebook(fpath):
    """Execute each notebook."""
    # Information on running notebooks is found here
    # https://nbconvert.readthedocs.io/en/latest/execute_api.html
    with fpath.open() as fp:
        nb = nbformat.read(fp, as_version=4)

    # Find which kernel to use. If it matches one installed use it. Otherwise try the
    # first
    if nb["metadata"]["kernelspec"]["name"] in kernel_specs:
        kernel_name = nb["metadata"]["kernelspec"]["name"]
    else:
        kernel_name = list(kernel_specs)[0]

    ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)

    try:
        ep.preprocess(nb, {"metadata": {"path": fpath.parent}})
    except CellExecutionError:
        msg = 'Error executing the notebook "%s".\n\n' % fpath
        msg += 'See notebook "%s" for the traceback.' % fpath
        print(msg)
        raise
    finally:
        with fpath.open(mode="w", encoding="utf-8") as fp:
            nbformat.write(nb, fp)
