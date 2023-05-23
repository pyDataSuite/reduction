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

def test_bounds_reduce_algorithm( ):
    """
    This function tests the interface to the bound-rduce function and
    ensures that the output it creates matches expectations.
    """

    # Generate data
    x = np.array( [2, 2.5, 3, 3.5, 4 ] )
    y1 = np.sin( x )
    y2 = np.cos( x )
    y3 = np.tan( x )
    original_data = np.array( [ x, y1, y2, y3 ] )

    # Generate bounds
    lower_bounds = [ native.Bounds( 0, -1 ), native.Bounds( 1, 20 ) ]
    upper_bounds = [ native.Bounds( 0, 1 ), native.Bounds( 1, 80 ) ]

    # Perform reduction
    rx, rl, ru = native._native.bounds_reduce( [x, x, x], [y1, y2, y3], lower_bounds, upper_bounds, 2, np.array( [2.0,3.0] ), 2, 4 )
    
    # Ensure inputs are the same
    assert np.all( original_data[ 0 ] == x )
    assert np.all( original_data[ 1 ] == y1 )
    assert np.all( original_data[ 2 ] == y2 )
    assert np.all( original_data[ 3 ] == y3 )

    # Ensure outputs are as expected
    assert np.all( x == rx )

    # Sigma data
    mean_vals = np.mean( original_data[1:], axis=0 )
    sigma_vals = np.std( original_data[1:], axis=0 )
    lower_sigma = mean_vals - sigma_vals
    upper_sigma = mean_vals + sigma_vals
    lower_diffs = np.abs( rl[ 0 ] - lower_sigma )
    upper_diffs = np.abs( ru[ 0 ] - upper_sigma )
    assert np.all( lower_diffs < 1e-9 )
    assert np.all( upper_diffs < 1e-9 )

    # Percentile data
    lower_percentiles = np.percentile( original_data[1:], 20, axis=1 )
    upper_percentiles = np.percentile( original_data[1:], 80, axis=1 )
    lower_diffs = np.abs( rl[ 1 ] - lower_percentiles )
    upper_diffs = np.abs( ru[ 1 ] - upper_percentiles )
    import pdb; pdb.set_trace()
    assert np.all( lower_diffs < 1e-9 )
    assert np.all( upper_diffs < 1e-9 )