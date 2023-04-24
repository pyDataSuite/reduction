cimport numpy as np
cimport libc.math as cmath
cimport cython
import numpy as np

@cython.boundscheck( False ) # Verified by inspection that this code can't go out of bounds
@cython.wraparound( False )  # This function does not utilize negative indexing
@cython.cdivision( True )    # This function won't divide by zero because the wrapper checks for invalid arguments
def line_reduce( double[:,:] raw_data, double dpi, double[:] gridsize, double xmin, double xmax, double ymin, double ymax, double zmin, double zmax ):
    # Pull python values into c datatypes for speed
    cdef double[ 3 ] mins =  [ xmin, ymin, zmin ]
    cdef double[ 3 ] maxs =  [ xmax, ymax, zmax ]
    cdef double[ 3 ] scale = [ 0.0, 0.0, 0.0 ]
    cdef Py_ssize_t num_dimensions, num_points 
    cdef double grid_points=0.0

    num_dimensions = raw_data.shape[ 0 ]
    num_points     = raw_data.shape[ 1 ]

    # Shortcut so that small datasets aren't processed at all
    if num_points < ( dpi * gridsize[ 0 ] ):
        return np.copy( raw_data )

    # Calculate grid scaling
    for dimension in range( num_dimensions ):
        grid_points = cmath.round( dpi * gridsize[ dimension ] )
        scale[ dimension ] = grid_points / ( maxs[ dimension ] - mins[ dimension ] )
        
    # Generate the output array
    output_vals = np.full( ( num_dimensions, int( cmath.round( dpi * gridsize[ 0 ] ) ) ), np.nan, dtype=np.float64 )
    cdef double[:,::1] output_view = output_vals
    cdef Py_ssize_t output_index=0, output_size=int( cmath.round( dpi * gridsize[ 0 ] ) )

    # Keep track of previous point to avoid duplicates
    cdef double[3] last_point = [ np.nan, np.nan, np.nan ]
    cdef double[3] current_point = [ np.nan, np.nan, np.nan ]
    cdef bint should_continue = False

    # Now start processing the dataset
    with nogil:
        for i in range( num_points ):
            should_continue = False

            # Make sure point is in bounds
            for dimension in range( num_dimensions ):
                if raw_data[ dimension, i ] < mins[ dimension ] or raw_data[ dimension, i ] > maxs[ dimension ]:
                    should_continue = True
            if should_continue:
                continue

            # Shift the current point onto grid axes
            for dimension in range( num_dimensions ):
                current_point[ dimension ] = ( raw_data[ dimension, i ] - mins[ dimension ] ) * scale[ dimension ]
                current_point[ dimension ] = cmath.round( current_point[ dimension ] )
                current_point[ dimension ] /= scale[ dimension ]
                current_point[ dimension ] += mins[ dimension ]

            # Skip this round if the point is the same as the previous point
            should_continue = True
            for dimension in range( num_dimensions ):
                if last_point[ dimension ] != current_point[ dimension ]:
                    should_continue = False
            if should_continue:
                continue

            # Add this point to the output array, and keep track of it
            for dimension in range( num_dimensions ):
                output_view[ dimension, output_index ] = current_point[ dimension ]
                last_point[ dimension ] = current_point[ dimension ]
            output_index += 1
            
            # Grow output array if necessary
            if output_size == output_index:
                with gil:
                    print( "Growing" )
                    output_size += int( cmath.round( dpi * gridsize[ 0 ] ) )
                    output_vals = np.append( output_vals, np.full( ( num_dimensions, int( cmath.round( dpi * gridsize[ 0 ] ) ) ), np.nan, dtype=np.float64 ), axis=1 )
                    output_view = output_vals
    
    # Return total output
    return output_vals[ :, :output_index ]