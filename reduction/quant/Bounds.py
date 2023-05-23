import numpy as np
from reduction.quant.native import Bounds
# from reduction.quant.native._native import 

class Bounds():

    def __init__( self, *datasets, bounds=[], shading=[] ):

        # == No longer perform this method ==
        # Get a common time array between all the datasets
        # xvals = np.array([], dtype=np.float64)
        # for dataset in datasets:
        #     xs = dataset[ 0 ]
        #     xvals = np.append( xvals, xs )
        #     xvals = np.unique( xvals )
        # xvals = np.sort( xvals )

        # Generate the raw data
        # self.raw_data = np.zeros( ( len( datasets ) + 1, len( xvals ) ), dtype=np.float64 )
        # self.raw_data[ 0 ] = xvals
        # for i, dataset in enumerate( datasets ):
        #     self.raw_data[ i + 1 ] = np.interp( self.raw_data[ 0 ], dataset[ 0 ], dataset[ 1 ], left=np.nan, right=np.nan )

        # Store raw data in the class, but copy it so the original data is not modified
        self.raw_xs = []
        self.raw_ys = []
        for data_x, data_y in datasets:
            # Sort indices to make future operations faster
            sort_indices = np.argsort( data_x )

            # Add x list only if an identical one is not already stored
            for xlist in self.raw_xs:
                if np.all( xlist == data_x[ sort_indices ] ):
                    self.raw_xs.append( xlist )
                    break
            else:
                self.raw_xs.append( np.copy( data_x[ sort_indices ] ) )
            
            # Add all y lists
            self.raw_ys.append( np.copy( data_y[ sort_indices ] ) )

        
        # Set up the bounds objects
        self.lower_bounds = [ Bounds( btype="%"==b[ 0 ][-1], value=float( b[ 0 ][:-1] ) ) for b in bounds ]
        self.upper_bounds = [ Bounds( btype="%"==b[ 1 ][-1], value=float( b[ 1 ][:-1] ) ) for b in bounds ]

        # Some additional class stuff
        # self.lower_bounds = [ b[ 0 ] for b in bounds ]
        # self.upper_bounds = [ b[ 1 ] for b in bounds ]
        self.shading = shading

        # Process the smaller dataset
        self.reduce_data( )

    def reduce_data( self ):
        pass
        # self.data_small = np.zeros( ( 2*len( self.lower_bounds ) + 1, len( self.raw_data[ 0 ] ) ), dtype=np.float64 )
        # self.data_small[ 0 ] = self.raw_data[ 0 ]
        # for i, ( lower, upper ) in enumerate( zip( self.lower_bounds, self.upper_bounds ) ):
        #     if "s" == lower[ -1 ]:
        #         sigma = float( lower[ :-1 ] )
        #         self.data_small[ 2*i+1 ] = np.mean( self.raw_data[ 1: ], axis=0 ) + sigma * np.std( self.raw_data[ 1: ], axis=0 )
        #     elif "%" == lower[ -1 ]:
        #         percentile = float( lower[ :-1 ] )
        #         self.data_small[ 2*i+1 ] = np.percentile( self.raw_data[ 1: ], percentile, axis=0 )

        #     if "s" == upper[ -1 ]:
        #         sigma = float( upper[ :-1 ] )
        #         self.data_small[ 2*i+2 ] = np.mean( self.raw_data[ 1: ], axis=0 ) + sigma * np.std( self.raw_data[ 1: ], axis=0 )
        #     elif "%" == upper[ -1 ]:
        #         percentile = float( upper[ :-1 ] )
        #         self.data_small[ 2*i+2 ] = np.percentile( self.raw_data[ 1: ], percentile, axis=0 )

    def plot_lines( self, ax, fig, **plot_args ):
        for dataset in self.raw_data[ 1: ]:
            ax.plot( self.raw_data[ 0 ], dataset, **plot_args )

    def plot( self, ax, fig, **plot_args ):
        for i, ( lower, upper ) in enumerate( zip( self.lower_bounds, self.upper_bounds ) ):
            ax.fill_between( 
                self.data_small[ 0 ], 
                self.data_small[ 2*i+1 ], 
                self.data_small[ 2*i+2 ], 
                color=self.shading[ i ], 
                label=f"{ lower } to { upper }", 
                **plot_args 
            )