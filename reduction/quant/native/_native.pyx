#cython: boundscheck=False
cimport numpy as np
cimport libc.math as cmath
import numpy as np

# This function is an O(n) algorithm
def snap_to_grid( double grid_start, double grid_scale, np.ndarray[ np.float64_t, ndim=1 ] values ):
    output_vals = np.zeros( values.shape[ 0 ], dtype=np.double )
    cdef double[:] result_view = output_vals

    for i in range( values.shape[ 0 ] ):
        # Project each point into grid space
        result_view[ i ] = ( values[ i ] - grid_start ) * grid_scale
        
        # Snap onto grid lines
        result_view[ i ] = cmath.round( result_view[ i ] )
        
        # Project back into original space
        result_view[ i ] = grid_start + ( result_view[ i ] / grid_scale )

    return output_vals