"""
This module contains tests (and consequently, example usages) 
of all the methods within the native package. These tests ensure
that performance is good and the functions continue working as
expected.
"""

import numpy as np
from reduction.quant import native

def test_grid_snapping_interface( ):
    """
    This function tests the interface to the function
    and ensures that it behaves appropriately.
    """

    xs = np.random.rand( 10_000_000 ) * 100
    xs_dup = np.copy( xs )
    xs_snapped = native.snap_to_grid( grid_start=0.5, grid_scale=1.1, data=xs )

    # Input array should not be changed
    assert np.all( xs == xs_dup )

    # Output should be different from input
    assert np.all( xs_snapped != xs )

def test_grid_snapping( ):
    """
    This function tests the output of snap_to_grid and
    ensures that the function operates correctly
    """
    xs = np.arange( 10.0 )
    xs_snapped = native.snap_to_grid( grid_start=0.5, grid_scale=0.5, data=xs )
    assert np.all( xs_snapped == np.array( [ 0.5, 0.5, 2.5, 2.5, 4.5, 4.5, 6.5, 6.5, 8.5, 8.5 ] ) )
