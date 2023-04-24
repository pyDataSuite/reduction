"""
This module contains tests (and consequently, example usages) 
of all the methods within the native package. These tests ensure
that performance is good and the functions continue working as
expected.
"""

import numpy as np
from reduction.quant import native
from reduction import Boundary
import matplotlib.pyplot as plt

def test_line_reduce_algorithm( ):
    """
    This function tests the interface to the function and
    ensures that it behaves appropriately.
    """

    # Generate data
    x = np.linspace( 0, 2 * np.pi, 200_000 )
    y = np.sin( x )
    data = np.array( [ x, y ] )
    data1_backup = np.copy( data )

    # Perform reduction
    reduced1 = native.line_reduce( raw_data=data, dpi=100, gridsize=np.array( [ 6.4, 4.8 ] ), bounds=Boundary( 0, 2, -2, 2 ) )
    assert np.all( data == data1_backup )

    # Generate higher-resolution data
    x = np.linspace( 0, 2 * np.pi, 250_000 )
    y = np.sin( x )
    data = np.array( [ x, y ] )
    data2_backup = np.copy( data )

    # Perform reduction
    reduced2 = native.line_reduce( raw_data=data, dpi=100, gridsize=np.array( [ 6.4, 4.8 ] ), bounds=Boundary( 0, 2, -2, 2 ) )
    assert np.all( data == data2_backup )

    # Ensure outputs are the same
    assert np.all( reduced1 == reduced2 )