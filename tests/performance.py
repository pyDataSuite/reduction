"""
This benchmarks the various modules that inhabit the reduction package. It
allows allows the performance impact of updates to be measured and reported.
"""

import sys
from pathlib import Path
sys.path.insert(0, str( Path(__file__).resolve().parents[ 1 ] ) )

from reduction.quant import native
import numpy as np
from timeit import Timer

# Large dataset
small_data = np.random.rand( 1_000_000 ) * 100
medium_data = np.random.rand( 10_000_000 ) * 100
big_data = np.random.rand( 100_000_000 ) * 100

# Test snap to grid
print( "Benchmark of snap_to_grid:" )
t_snapped_small = Timer( lambda: native.snap_to_grid( grid_start=0.5, grid_scale=1.1, data=small_data ) ).timeit( number=1 ) / 1
print( "  1,000,000 points:  ", t_snapped_small, "seconds per run" )
t_snapped_medium = Timer( lambda: native.snap_to_grid( grid_start=0.5, grid_scale=1.1, data=medium_data ) ).timeit( number=10 ) / 10
print( "  10,000,000 points: ", t_snapped_medium, "seconds per run" )
t_snapped_big = Timer( lambda: native.snap_to_grid( grid_start=0.5, grid_scale=1.1, data=big_data ) ).timeit( number=10 ) / 10
print( "  100,000,000 points:", t_snapped_big, "seconds per run" )