import numpy as np
cimport numpy as np

def snap_to_grid( float grid_start, float grid_scale, np.ndarray[ np.float64_t, ndim=1 ] values ):
    # Project the values into grid coordinates
    #cdef np.ndarray[ np.float64_t, ndim=1 ] grid_values 
    
    cdef Py_ssize_t i, n = values.shape[ 0 ]

    for i in range( n ):
        values[ i ] = ( values[ i ] - grid_start ) * grid_scale
    # values = ( values - grid_start ) * grid_scale
    
    return values