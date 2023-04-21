"""
The _native package is an interface that wraps around natively-compiled
C libraries. The libraries are generated by Cython when this package is
built.

For a report on the quality of the native code, see [this page](./_native.html)
"""

# This file contains functions that wrap the native libraries, which allows
# type annotations and some prepocessing to be used.

import multiprocessing
import numpy as np
from . import _native

def snap_to_grid( grid_start: float, grid_scale: float, data: np.ndarray ) -> np.ndarray:
    return _native.snap_to_grid( grid_start, grid_scale, data )