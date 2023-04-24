import numpy as np
import matplotlib.pyplot as plt

from reduction.quant import Line

data = np.zeros( ( 100_000_000, 2 ) )
data[ :,0 ] = np.linspace( 0, np.pi * 2, 100_000_000 )
data[ :,1 ] = np.sin( data[ :,0 ] )
line = Line( data, dpi=200 )

fig = plt.figure()
ax = fig.add_subplot( 111 )
line.plot( fig, ax, linestyle='--', linewidth=3 )
plt.show()