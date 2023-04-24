import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits import mplot3d
from threading import Thread

from reduction import Boundary
from .native import line_reduce

class Line:
    """
    A quantization reducer class that represents line plots. Can be used with
    one-dimensional or two-dimensional data.
    """

    def __init__( self, data: np.ndarray, dpi=100, gridsize=( 6.4, 4.8 ), boundary: Boundary=None ) -> None:
        """
        Args:
            data (np.ndarray): The data that makes up the line.
            .. warning:: data must be either 2 or 3 dimensions
            .. info:: data is supported in row form and column form. It internally will be converted to row form, but the input will not be affected.
        """
        
        # Copy input data and turn it into row data if it is not already
        if data.shape[ 0 ] > data.shape[ 1 ]:
            self.data = np.copy( np.transpose( data ) )
        else:
            self.data = np.copy( data )
        
        self.ndim = np.min( data.shape )
        self.dpi = dpi
        if not isinstance( gridsize, np.ndarray ):
            self.gridsize = np.array( gridsize )
        else:
            self.gridsize = gridsize
        self.data_small = np.array( [] )

        # Set default boundary
        if boundary is None:
            self.boundary = Boundary(
                xmin=np.min( self.data[ 0 ] ),
                xmax=np.max( self.data[ 0 ] ),
                ymin=np.min( self.data[ 1 ] ),
                ymax=np.max( self.data[ 1 ] ),
                zmin=np.min( self.data[ 2 ] ) if self.ndim == 3 else np.nan,
                zmax=np.max( self.data[ 2 ] ) if self.ndim == 3 else np.nan,
            )
        else:
            self.boundary = boundary

        # Process smaller dataset
        self.reduce_data( )

        # Final stuff
        self.updates = 0
        self.update_thread = Thread( )
        self.__plot__ = None
        self.redraw = True

    #
    # These functions facilitate working with the raw data
    #
    @property
    def raw_x( self ):
        """Returns the x values of the raw dataset"""
        return self.data[ 0 ]
    
    @raw_x.setter
    def raw_x( self, value ):
        """Sets the x values of the raw dataset"""
        self.data[ 0 ] = value
    
    @property
    def raw_y( self ):
        """Returns the y values of the raw dataset"""
        return self.data[ 1 ]
    
    @raw_y.setter
    def raw_y( self, value ):
        """Sets the y values of the raw dataset"""
        self.data[ 1 ] = value
    
    @property
    def raw_z( self ):
        """Returns the z values of the raw dataset"""
        return self.data[ 2 ]
    
    @raw_z.setter
    def raw_z( self, value ):
        """Sets the z values of the raw dataset"""
        self.data[ 2 ] = value
    
    #
    # These functions facilitate working with the reduced data
    #
    @property
    def x( self ):
        """Returns the x values of the reduced dataset"""
        return self.data_small[ 0 ]
    
    @x.setter
    def x( self, value ):
        """Sets the x values of the reduced dataset"""
        self.data_small[ 0 ] = value

    @property
    def y( self ):
        """Returns the y values of the reduced dataset"""
        return self.data_small[ 1 ]
    
    @y.setter
    def y( self, value ):
        """Sets the y values of the reduced dataset"""
        self.data_small[ 1 ] = value

    @property
    def z( self ):
        """Returns the z values of the reduced dataset"""
        return self.data_small[ 2 ]
    
    @z.setter
    def z( self, value ):
        """Sets the z values of the reduced dataset"""
        self.data_small[ 2 ] = value

    def reduce_data( self ):
        """
        Generates a small dataset that can be used to plot the line
        """
        self.data_small = line_reduce( self.data, self.dpi, self.gridsize, self.boundary )

    def plot( self, figure: Figure, axes: Axes, **plot_args ) -> None:
        """
        Add the Line dataset to a matplotlib figure.

        Args:
            figure (Figure): the figure to use for the plot
            axes (Axes): the axes to use for the plot
            **plot_args: additional arguments to pass to the plot function

        Example:
        ```
        fig, ax = plt.subplots()
        l = Line( np.arange( 20 ).reshape( 2, 10 ) )
        l.plot( fig, ax, color='red' )
        ```
        """        
        self.axes = axes
        self.figure = figure
        self.__plot__, = self.axes.plot( *self.data_small, **plot_args )

        # Update to match plot settings
        self.dpi = self.figure.dpi
        self.size = self.figure.get_size_inches()

        # Attach relevant callbacks
        self.axes.callbacks.connect( 'xlim_changed', self._update )
        self.axes.callbacks.connect( 'ylim_changed', self._update )

    def _update( self, _ ):

        # Update parameters to match plot
        self.boundary.xmin, self.boundary.xmax = self.axes.get_xlim( )
        self.boundary.ymin, self.boundary.ymax = self.axes.get_ylim( )
        if self.ndim == 3:
            self.boundary.zmin, self.boundary.zmax = self.axes.get_zlim( )

        self.dpi = self.figure.dpi
        self.size = self.figure.get_size_inches()

        # Log that we requested an update
        if self.updates <= 1:
            self.updates += 1
        
        # Ensure we aren't already updating
        if not self.update_thread.is_alive( ):
            try:
                self.update_thread.join( )
            except RuntimeError:
                pass

            # Generate new thread
            self.update_thread = Thread( target=self._reprocess )
            self.update_thread.start( )
    
    def _reprocess( self ):
        while self.updates > 0:
            self.updates -= 1

            self.reduce_data( )

            if self.__plot__ is not None:
                self.__plot__.set_xdata( self.data_small[ 0 ] )
                self.__plot__.set_ydata( self.data_small[ 1 ] )
                if self.ndim == 3:
                    self.__plot__.set_zdata( self.data_small[ 2 ] )
        
        # Finish by updating the drawing
        if self.__plot__ is not None and self.redraw:
            self.figure.canvas.draw( )