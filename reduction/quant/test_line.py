import numpy as np
import matplotlib.pyplot as plt

from . import Line

def test_line():
    data = np.zeros( ( 10_000, 2 ) )
    data[ :,0 ] = np.linspace( 0, np.pi * 2, 10_000 )
    data[ :,1 ] = np.sin( data[ :,0 ] )
    line = Line( data, dpi=200 )

    fig = plt.figure()
    ax = fig.add_subplot( 111 )
    line.plot( fig, ax, linestyle='--', linewidth=3 )
    plt.show()

if __name__ == '__main__':
    test_line()