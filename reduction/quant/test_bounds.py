import numpy as np
from reduction.quant.Bounds import Bounds
import matplotlib.pyplot as plt

def test_bounds():
    xs = []
    ys = []

    print( "starting test" )

    for i in range( 100 ):
        rand = np.random.uniform( 0, 10, 10000 )
        xs.append(
            rand
        )
        xs[ i ] = np.sort( xs[ i ] )
        ys.append(
            np.sin( xs[ i ] )+(rand-5)/10
        )
    
    # With sigma bounds
    bounds = Bounds( *[ ( x, y ) for x, y in zip( xs, ys ) ], bounds=[ ( "-3s", "3s" ), ( "-2s", "2s" ), ( "-1s", "1s" ) ], shading=[ '0.9', '0.7', '0.5' ] )

    fig = plt.figure()
    ax = fig.add_subplot( 111 )
    bounds.plot( ax, fig )
    plt.legend()
    plt.show()

    # With percentile bounds
    bounds = Bounds( *[ ( x, y ) for x, y in zip( xs, ys ) ], bounds=[ ( "0%", "100%" ), ( "4%", "96%" ), ( "20%", "80%" ) ], shading=[ '0.9', '0.7', '0.5' ] )
    fig = plt.figure()
    ax = fig.add_subplot( 111 )
    bounds.plot( ax, fig )
    plt.legend()
    plt.show()