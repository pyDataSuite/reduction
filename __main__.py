from reduction import quant
from reduction.quant import cmath, jmath, pmath
import numpy as np
from timeit import Timer

x = np.linspace( 0, 2*np.pi, 100_000_000 )

cmath_t = Timer( lambda: cmath.snap_to_grid( 0.1, 1.2, x ) ).timeit( number=10 )
print( "cmath:", cmath_t )

jmath_t = Timer( lambda: jmath.snap_to_grid( 0.1, 1.2, x ) ).timeit( number=10 )
print( "jmath:", jmath_t )

pmath_t = Timer( lambda: pmath.snap_to_grid( 0.1, 1.2, x ) ).timeit( number=10 )
print( "pmath:", pmath_t )