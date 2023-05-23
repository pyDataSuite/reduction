cimport numpy as np
cimport libc.math as cmath
cimport cython
import numpy as np

cdef double cnan = np.nan

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
    output_vals = np.full( ( num_dimensions, int( cmath.round( dpi * gridsize[ 0 ] ) ) ), cnan, dtype=np.float64 )
    cdef double[:,::1] output_view = output_vals
    cdef Py_ssize_t output_index=0, output_size=int( cmath.round( dpi * gridsize[ 0 ] ) )

    # Keep track of previous point to avoid duplicates
    cdef double[3] last_point = [ cnan, cnan, cnan ]
    cdef double[3] current_point = [ cnan, cnan, cnan ]
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
                    output_vals = np.append( output_vals, np.full( ( num_dimensions, int( cmath.round( dpi * gridsize[ 0 ] ) ) ), cnan, dtype=np.float64 ), axis=1 )
                    output_view = output_vals
    
    # Return total output
    return output_vals[ :, :output_index ]

cdef enum BoundsType:
    sigma = 0
    percentile = 1

cdef class Bounds:
    cdef int btype
    cdef double value

    def __init__( self, btype, value ):
        self.btype = btype
        self.value = value

    def __repr__(self) -> str:
        return f"Bounds({self.btype}, {self.value})"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    cdef double run_on( self, double[:] values ):
        if self.btype == BoundsType.sigma:
            return np.nanmean( values ) + self.value * np.nanstd( values )
        if self.btype == BoundsType.percentile:
            return np.nanpercentile( values, self.value )
        return np.nan

# @cython.boundscheck( False ) # Verified by inspection that this code can't go out of bounds
# @cython.wraparound( False )  # This function does not utilize negative indexing
# @cython.cdivision( True )    # This function won't divide by zero because the wrapper checks for invalid arguments
def bounds_reduce( raw_x, raw_y, lower_bounds not None, upper_bounds not None, double dpi, double[:] gridsize, double xmin, double xmax ):
    cdef Py_ssize_t d, i, j, grid_x_len=0, 
    cdef Py_ssize_t num_bounds=len( lower_bounds ), num_datasets=len( raw_y )

    # Create array of grid x coordinates
    grid_x_len = int( cmath.round( dpi * gridsize[ 0 ] + 1 ) )
    x_values = np.linspace( xmin, xmax, grid_x_len )
    cdef double[ ::1 ] x_values_view = x_values

    # Further grid definitions
    cdef double grid_spacing = x_values_view[ 1 ] - x_values_view[ 0 ]
    cdef double half_grid_spacing = grid_spacing / 2.0

    # Prepare output arrays
    agg_values = np.full( ( grid_x_len, 2*num_datasets ), cnan, dtype=np.float64 )
    cdef double[ :,::1 ] agg_values_view=agg_values #, min_values_view=min_values

    # Begin collecting upper and lower values
    cdef double[ : ] x_data_view, y_data_view
    cdef double current_min=-np.inf, current_max=cnan, current_grid_x=0
    for d in range( num_datasets ):
        x_data_view = raw_x[ d ]
        y_data_view = raw_y[ d ]
        for i in range( grid_x_len ):
            current_grid_x = x_values_view[ i ]
            for j in range( len( x_data_view ) ):
                if x_data_view[ j ] >= current_grid_x + half_grid_spacing:
                    # Since the x values are sorted, we don't have to keep checking
                    # once we have passed the maximum value
                    break
                if x_data_view[ j ] < current_grid_x - half_grid_spacing:
                    # Keep skipping x values until we have passed the minimum
                    # value
                    continue
                if agg_values_view[ i, 2*d ] < y_data_view[ j ] or cmath.isnan( agg_values_view[ i, 2*d ] ):
                    agg_values_view[ i, 2*d ] = y_data_view[ j ]
                if agg_values_view[ i, 2*d+1 ] > y_data_view[ j ] or cmath.isnan( agg_values_view[ i, 2*d+1 ] ):
                    agg_values_view[ i, 2*d+1 ] = y_data_view[ j ]
    print( agg_values )
    # Prepare the actual outputs
    upper_bound_output = np.zeros( ( num_bounds, grid_x_len ), dtype=np.float64 )
    lower_bound_output = np.zeros( ( num_bounds, grid_x_len ), dtype=np.float64 )
    cdef double[ :, ::1 ] upper_bound_output_view=upper_bound_output, lower_bound_output_view=lower_bound_output
    cdef Bounds lbound, ubound

    # Fill the upper and lower bounds
    for i in range( num_bounds ):
        lbound = lower_bounds[ i ]
        ubound = upper_bounds[ i ]
        for j in range( grid_x_len ):
            lower_bound_output_view[ i, j ] = lbound.run_on( agg_values_view[ j ] )
            upper_bound_output_view[ i, j ] = ubound.run_on( agg_values_view[ j ] )

    return x_values, lower_bound_output, upper_bound_output